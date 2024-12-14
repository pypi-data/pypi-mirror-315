from __future__ import annotations

import copy
from dataclasses import _MISSING_TYPE, dataclass, field, fields
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from slugify import slugify

from .exceptions import InvalidConfiguration


class LogLevel(Enum):
    info = "INFO"
    debug = "DEBUG"
    warning = "WARNING"


class MountPointType(Enum):
    HOSTPATH = "HOSTPATH"
    SECRET = "SECRET"
    CONFIGMAP = "CONFIGMAP"
    EMPTYDIR = "EMPTYDIR"


@dataclass
class MountPoint:
    local_path: str
    mount_path: str
    read_only: bool = True
    type: MountPointType = MountPointType.HOSTPATH
    size_limit: Optional[str] = None  # Only valid for emptydir

    @property
    def name(self) -> str:
        return slugify(self.local_path)


def create_klass(cls, settings, prefix: str):
    """
    Create cls from config parameters in settings.


    The fields of cls should be present in upper-case prefixed with the prefix and "_".
    """
    kwargs = {}

    for cls_field in fields(cls):
        attr_name = f"{prefix}_{cls_field.name.upper()}"

        if (
            isinstance(cls_field.default, _MISSING_TYPE)
            and isinstance(cls_field.default_factory, _MISSING_TYPE)
            and not hasattr(settings, attr_name)
        ):
            raise InvalidConfiguration(f"{attr_name} is a mandatory setting")

        if hasattr(settings, attr_name):
            kwargs[cls_field.name] = getattr(settings, attr_name)

    # [['api', 'CLUSTER', 'v3'], ]
    if "constraints" in kwargs and isinstance(kwargs["constraints"], list):
        kwargs["constraints"] = [MarathonConstraint(*x) for x in kwargs["constraints"]]

    return cls(**kwargs)


@dataclass
class DockerBackendConfig:
    client_url: str  # URL to docker or marathon
    network_name: str  # network to use
    debug: bool = False

    @classmethod
    def from_settings(cls, settings, prefix="CONTAINER_HUB") -> "DockerBackendConfig":
        """
        Populate DockerBackendConfig from simple-settings, Django settings
        or similair object.
        """
        return create_klass(cls, settings, prefix)


@dataclass
class MarathonConstraint:
    param: str
    operator: str
    value: str


@dataclass
class MarathonBackendConfig(DockerBackendConfig):
    constraints: List[MarathonConstraint] = field(default_factory=list)

    @classmethod
    def from_settings(cls, settings, prefix="CONTAINER_HUB") -> "MarathonBackendConfig":
        """
        Populate MarathonBackendConfig from simple-settings, Django settings
        or similair object.
        """
        return create_klass(cls, settings, prefix)


@dataclass
class KubernetesBackendConfig:
    client_url: str  # URL to docker or marathon
    # Kubernetes namespace to deploy to
    namespace: str = "default"

    @classmethod
    def from_settings(
        cls, settings, prefix="CONTAINER_HUB"
    ) -> "KubernetesBackendConfig":
        """
        Populate KubernetesBackendConfig from simple-settings, Django settings
        or similair object.
        """
        return create_klass(cls, settings, prefix)


@dataclass
class EnvVar:
    name: str
    value: str


@dataclass
class Label:
    name: str
    value: str


@dataclass
class ContainerConfig:
    image_name: str  # threedicore image name
    base_result_path: Path  # path for results
    sim_uid: str
    sim_ref_datetime: datetime
    end_time: int
    duration: int
    pause_timeout: int
    start_mode: str
    model_config: str
    max_cpu: int  # max CPU's to use
    session_memory: int  # max memory
    envs: List[EnvVar]
    labels: List[Label]
    max_rate: float = 0.0
    clean_up_files: bool = False
    gridadmin_download_url: Optional[str] = None
    tables_download_url: Optional[str] = None
    mount_points: List[MountPoint] = field(default_factory=list)
    redis_host: str = "redis"  # Local redis host
    container_log_level: LogLevel = LogLevel.info
    debugpy_port: Optional[int] = None


# Kubernetes dataclasses.
# These are much more generic than the Docker/Marathon ContainerConfig


@dataclass
class ResourceSpec:
    cpu: str
    memory: str

    @classmethod
    def from_dict(cls, values: Dict) -> "ResourceSpec":
        # Make (deep) copy to keep original defaults
        values = copy.deepcopy(values)

        return ResourceSpec(cpu=values["cpu"], memory=values["memory"])

    def to_dict(self):
        return {"cpu": self.cpu, "memory": self.memory}


@dataclass
class NodeAffinityConfig:
    key: str
    operator: str
    values: List[str]

    @classmethod
    def from_dict(cls, values: Dict) -> "NodeAffinityConfig":
        # Make (deep) copy to keep original defaults
        values = copy.deepcopy(values)

        return NodeAffinityConfig(
            key=values["key"], operator=values["operator"], values=values["values"]
        )


@dataclass
class Resources:
    limits: ResourceSpec
    requests: ResourceSpec

    @classmethod
    def from_dict(cls, values: Dict) -> "Resources":
        # Make (deep) copy to keep original defaults
        values = copy.deepcopy(values)

        return Resources(
            limits=ResourceSpec.from_dict(values.get("limits", {})),
            requests=ResourceSpec.from_dict(values.get("requests", {})),
        )


@dataclass
class KubernetesContainer:
    name: str
    image: str  # Docker image
    args: List[str]  # command start up args
    envs: List[EnvVar] = field(default_factory=list)
    labels: List[Label] = field(default_factory=list)
    mount_points: List[MountPoint] = field(default_factory=list)
    ports: List[int] = field(default_factory=list)
    resources: Optional[Resources] = None

    @classmethod
    def from_dict(cls, values: Dict) -> "KubernetesContainer":
        # Make (deep) copy to keep original defaults
        values = copy.deepcopy(values)

        return KubernetesContainer(
            name=values.get("name"),
            image=values.get("image"),
            args=values.get("args"),
            envs=[EnvVar(key, value) for key, value in values.get("envs", {}).items()],
            labels=[
                Label(key, value) for key, value in values.get("labels", {}).items()
            ],
            mount_points=[
                MountPoint(
                    key,
                    value["bind"],
                    value["ro"],
                    MountPointType(value.get("type", MountPointType.HOSTPATH.value)),
                    size_limit=value.get("size_limit", None),
                )
                for key, value in values.get("mounts", {}).items()
            ],
            ports=values.get("ports", []),
            resources=Resources.from_dict(values["resources"])
            if "resources" in values
            else None,
        )


@dataclass
class HostAlias:
    ip_address: str
    hostnames: List[str]


@dataclass
class KubernetesJobConfig:
    name: str
    redis_config: KubernetesContainer
    scheduler_config: KubernetesContainer
    simulation_config: KubernetesContainer
    annotations: List[Label] = field(default_factory=list)
    labels: List[Label] = field(default_factory=list)
    host_aliases: List[HostAlias] = field(default_factory=list)
    service_account_name: str = "simulation-service-account"
    regcred_secret_name: Optional[str] = None  # Registry credentials secret
    node_affinity: Optional[NodeAffinityConfig] = None

    @property
    def mount_points(self) -> List[MountPoint]:
        """
        Combined list of mount_points
        """
        mount_points = []
        for mount_point in (
            self.redis_config.mount_points
            + self.scheduler_config.mount_points
            + self.simulation_config.mount_points
        ):
            if mount_point not in mount_points:
                mount_points.append(mount_point)
        return mount_points

    @classmethod
    def from_settings(
        cls, name: str, settings, prefix="CONTAINER_HUB"
    ) -> "KubernetesJobConfig":
        """
        Load KubernetesJobConfig from supplied values in `CONTAINER_HUB_KUBERNETES_CONTAINER_DEFAULTS`
        """
        cfg = getattr(settings, f"{prefix}_KUBERNETES_CONTAINER_DEFAULTS")

        return KubernetesJobConfig(
            name=name,
            redis_config=KubernetesContainer.from_dict(cfg["REDIS"]),
            scheduler_config=KubernetesContainer.from_dict(cfg["SCHEDULER"]),
            simulation_config=KubernetesContainer.from_dict(cfg["SIMULATION"]),
            host_aliases=[
                HostAlias(ip_address, hostnames)
                for ip_address, hostnames in cfg.get("HOST_ALIASES", {}).items()
            ],
            annotations=[
                Label(name, value) for name, value in cfg.get("ANNOTATIONS", {}).items()
            ],
            regcred_secret_name=cfg.get("regcred_secret_name", None),
            node_affinity=NodeAffinityConfig(**cfg["node_affinity"])
            if "node_affinity" in cfg
            else None,
        )
