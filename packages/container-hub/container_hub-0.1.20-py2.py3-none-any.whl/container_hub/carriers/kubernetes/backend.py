from functools import cached_property
from typing import Any, Dict, List, Union

from hikaru.model.rel_1_20 import (
    Affinity,
    ConfigMapVolumeSource,
    Container,
    ContainerPort,
    EmptyDirVolumeSource,
    EnvVar,
    HostAlias,
    HostPathVolumeSource,
    Job,
    JobSpec,
    LocalObjectReference,
    NodeAffinity,
    NodeSelector,
    NodeSelectorRequirement,
    NodeSelectorTerm,
    ObjectMeta,
    PodSpec,
    PodTemplateSpec,
    ResourceRequirements,
    SecretVolumeSource,
    Volume,
    VolumeMount,
)
from kubernetes import config as client_config
from kubernetes.client import (
    ApiClient,
    ApiException,
    BatchV1Api,
    Configuration,
    CoreV1Api,
)
from kubernetes.client.models import V1DeleteOptions, V1Job, V1JobList, V1JobStatus

from container_hub.exceptions import CarrierError
from container_hub.models import (
    KubernetesBackendConfig,
    KubernetesContainer,
    KubernetesJobConfig,
    MountPointType,
    NodeAffinityConfig,
)

# Accessing host (laptop) from within k8s cluster
K3S_HOST_DNS_NAME = "host.k3d.internal"
MINIKUBE_HOST_DNS_NAME = "host.minikube.internal"


class KubernetesBackend:
    """
    Backend for starting Docker instances via Docker
    """

    def __init__(self, config: KubernetesBackendConfig, in_cluster=True):
        self.config = config
        self.in_cluster = in_cluster

    @cached_property
    def configuration(self) -> Configuration:
        configuration = Configuration(host=self.config.client_url)
        if self.in_cluster:
            client_config.load_incluster_config(configuration)

        return configuration

    def container_hosts(self) -> Dict[str, str]:
        return {}

    def get_job_status(self, job_name: str) -> Dict[str, Any]:
        """
        Get a specific pod ip, based on job_name (simulation-xxx)
        """
        job: Union[V1Job, None] = None
        with ApiClient(self.configuration) as api_client:
            api = BatchV1Api(api_client)
            try:
                job: V1Job = api.read_namespaced_job(
                    job_name, namespace=self.config.namespace
                )
            except ApiException:
                job = None

        if job is None:
            raise CarrierError("unknown Job")

        if job.status is None:
            raise CarrierError("Job has no status")

        job_status: V1JobStatus = job.status
        return job_status.to_dict()

    def pod_ip(self, job_name: str) -> str:
        """
        Get a specific pod ip, based on job_name (simulation-xxx)
        """
        with ApiClient(self.configuration) as api_client:
            api = CoreV1Api(api_client)
            results = api.list_namespaced_pod(
                namespace=self.config.namespace, label_selector=f"job-name={job_name}"
            )
            if len(results.items) != 1:
                raise CarrierError(f"Incorrect number of pods returned: {results}")
            return results.items[0].status.pod_ip

    def container_ips(self) -> Dict[str, str]:
        return {}

    def container_list(self) -> List[str]:
        with ApiClient(self.configuration) as api_client:
            jobs: List[Job] = []
            api = BatchV1Api(api_client)
            job_list = None
            while job_list is None or job_list.metadata._continue is not None:
                job_list: V1JobList = api.list_namespaced_job(
                    namespace=self.config.namespace
                )
                jobs += [x for x in job_list.items]
        return [
            job.metadata.name.lstrip("simulation-")
            for job in jobs
            if job.metadata.name.startswith("simulation-")
        ]

    def up(self, job_config: KubernetesJobConfig) -> str:
        """
        Create Kubernetes job for simulation
        """
        job = get_simulation_job(job_config)
        with ApiClient(self.configuration) as api_client:
            job = job.create(namespace=self.config.namespace, client=api_client)
        return job_config.name

    def down(self, sim_uid: str):
        """Remove the given app."""
        name = f"simulation-{sim_uid}"
        with ApiClient(self.configuration) as api_client:
            api = BatchV1Api(api_client)
            api.delete_namespaced_job(
                namespace=self.config.namespace,
                name=name,
                grace_period_seconds=0,
                propagation_policy="Background",
                body=V1DeleteOptions(propagation_policy="Background"),
            )


def get_node_affinity(node_affinity_cfg: NodeAffinityConfig) -> Affinity:
    return Affinity(
        nodeAffinity=NodeAffinity(
            requiredDuringSchedulingIgnoredDuringExecution=NodeSelector(
                nodeSelectorTerms=[
                    NodeSelectorTerm(
                        matchExpressions=[
                            NodeSelectorRequirement(
                                key=node_affinity_cfg.key,
                                operator=node_affinity_cfg.operator,
                                values=node_affinity_cfg.values,
                            )
                        ]
                    )
                ]
            )
        )
    )


def get_simulation_job(cfg: KubernetesJobConfig) -> Job:
    return Job(
        apiVersion="batch/v1",
        kind="Job",
        metadata=ObjectMeta(
            name=cfg.name,
            annotations={x.name: x.value for x in cfg.annotations},
            labels={"app": cfg.name},
        ),
        spec=JobSpec(
            template=PodTemplateSpec(
                metadata=ObjectMeta(
                    annotations={x.name: x.value for x in cfg.annotations},
                    labels={"app": cfg.name},
                ),
                spec=PodSpec(
                    affinity=get_node_affinity(cfg.node_affinity)
                    if cfg.node_affinity is not None
                    else None,
                    serviceAccountName=cfg.service_account_name,
                    imagePullSecrets=[
                        LocalObjectReference(name=cfg.regcred_secret_name)
                    ]
                    if cfg.regcred_secret_name is not None
                    else None,
                    hostAliases=[
                        HostAlias(x.ip_address, x.hostnames) for x in cfg.host_aliases
                    ],
                    containers=[
                        get_container(cfg.redis_config),
                        get_container(cfg.scheduler_config),
                        get_container(cfg.simulation_config),
                    ],
                    volumes=[
                        Volume(
                            name=mount.name,
                            hostPath=HostPathVolumeSource(
                                path=mount.local_path, type="Directory"
                            ),
                        )
                        for mount in cfg.mount_points
                        if mount.type == MountPointType.HOSTPATH
                    ]
                    + [
                        Volume(
                            name=mount.name,
                            emptyDir=EmptyDirVolumeSource(sizeLimit=mount.size_limit),
                        )
                        for mount in cfg.mount_points
                        if mount.type == MountPointType.EMPTYDIR
                    ]
                    + [
                        Volume(
                            name=mount.name,
                            configMap=ConfigMapVolumeSource(name=mount.local_path),
                        )
                        for mount in cfg.mount_points
                        if mount.type == MountPointType.CONFIGMAP
                    ]
                    + [
                        Volume(
                            name=mount.name,
                            secret=SecretVolumeSource(secretName=mount.local_path),
                        )
                        for mount in cfg.mount_points
                        if mount.type == MountPointType.SECRET
                    ],
                    restartPolicy="Never",
                ),
            ),
            backoffLimit=1,
            completions=1,
        ),
    )


def get_container(cfg: KubernetesContainer) -> Container:
    """
    Get k8s container API resource
    """
    # Might ne needed for local dev:
    #   hostAliases=[HostAlias(f"{HOST_IP}", ["minio"])],

    return Container(
        name=cfg.name,
        image=cfg.image,
        imagePullPolicy="IfNotPresent",
        resources=ResourceRequirements(
            limits=cfg.resources.limits.to_dict(),
            requests=cfg.resources.requests.to_dict(),
        )
        if cfg.resources is not None
        else ResourceRequirements(),
        args=cfg.args,
        env=[
            EnvVar(
                name=envvar.name,
                value=envvar.value,
            )
            for envvar in cfg.envs
        ],
        volumeMounts=[
            VolumeMount(
                mountPath=mount.mount_path, name=mount.name, readOnly=mount.read_only
            )
            for mount in cfg.mount_points
        ],
        ports=[ContainerPort(containerPort=port) for port in cfg.ports],
    )
