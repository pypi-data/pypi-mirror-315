from dataclasses import asdict

import pytest
from simple_settings import LazySettings

from container_hub import get_backend
from container_hub.carriers.docker.backend import DockerBackend
from container_hub.carriers.kubernetes.backend import KubernetesBackend
from container_hub.models import KubernetesJobConfig, MountPointType


@pytest.fixture
def docker_simple_settings():
    # os.environ.update({"SIMPLE_SETTINGS": "tests.test_files.docker_settings"})
    yield LazySettings("tests.test_files.docker_settings")


@pytest.fixture
def kubernetes_simple_settings():
    yield LazySettings("tests.test_files.kubernetes_settings")


def test_loading_docker_backend(docker_simple_settings):
    backend = get_backend(docker_simple_settings)
    assert isinstance(backend, DockerBackend)


def test_loading_kubernetes_backend(kubernetes_simple_settings):
    backend = get_backend(kubernetes_simple_settings)
    assert backend.config.namespace == "threedi"
    assert isinstance(backend, KubernetesBackend)


# Test loading kubernetes container defaults
def test_loading_kubernetes_defaults(kubernetes_simple_settings):
    config = KubernetesJobConfig.from_settings("sim4234", kubernetes_simple_settings)
    assert asdict(config) == {
        "host_aliases": [{"hostnames": ["minio"], "ip_address": "127.0.0.1"}],
        "name": "sim4234",
        "redis_config": {
            "name": "redis",
            "image": "redis:5.0.3-alpine",
            "args": ["sh", "-c", "rm -rf /data/dump.rdb && redis-server --save "],
            "envs": [],
            "labels": [],
            "mount_points": [],
            "ports": [6379],
            "resources": None,
        },
        "scheduler_config": {
            "name": "scheduler",
            "image": "harbor.lizard.net/threedi/scheduler:latest",
            "args": ["python3", "/code/scheduler.py", "localhost"],
            "envs": [
                {
                    "name": "DJANGO_SETTINGS_MODULE",
                    "value": "threedi_scheduler.developmentsettings",
                },
                {"name": "REDIS_HOST", "value": "localhost"},
            ],
            "labels": [],
            "mount_points": [
                {
                    "local_path": "/local/path/one",
                    "mount_path": "mount_path_1",
                    "read_only": True,
                    "size_limit": None,
                    "type": MountPointType.HOSTPATH,
                },
                {
                    "local_path": "/local/path/two",
                    "mount_path": "mount_path_2",
                    "read_only": False,
                    "size_limit": None,
                    "type": MountPointType.HOSTPATH,
                },
                {
                    "local_path": "scheduler-config",
                    "mount_path": "/etc/config/config.yaml",
                    "read_only": True,
                    "size_limit": None,
                    "type": MountPointType.CONFIGMAP,
                },
                {
                    "local_path": "scheduler-secret",
                    "mount_path": "/etc/secrets/",
                    "read_only": True,
                    "size_limit": None,
                    "type": MountPointType.SECRET,
                },
                {
                    "local_path": "shared-data",
                    "mount_path": "/mnt/results/",
                    "read_only": False,
                    "size_limit": "10Gi",
                    "type": MountPointType.EMPTYDIR,
                },
            ],
            "resources": {
                "limits": {
                    "cpu": "1",
                    "memory": "2Gi",
                },
                "requests": {"cpu": "250m", "memory": "128Mi"},
            },
            "ports": [],
        },
        "simulation_config": {
            "name": "simulation",
            "image": "harbor.lizard.net/threedi/threedicore:2.16.1-2.2.5",
            "args": ["python", "service.py", "localhost"],
            "envs": [{"name": "RESULTS_PATH", "value": "/results"}],
            "labels": [],
            "mount_points": [
                {
                    "local_path": "/local/path/one",
                    "mount_path": "mount_path_1",
                    "read_only": True,
                    "size_limit": None,
                    "type": MountPointType.HOSTPATH,
                },
                {
                    "local_path": "/local/path/two",
                    "mount_path": "mount_path_2",
                    "read_only": False,
                    "size_limit": None,
                    "type": MountPointType.HOSTPATH,
                },
                {
                    "local_path": "shared-data",
                    "mount_path": "/mnt/results/",
                    "read_only": False,
                    "size_limit": "10Gi",
                    "type": MountPointType.EMPTYDIR,
                },
            ],
            "resources": {
                "limits": {
                    "cpu": "1",
                    "memory": "5Gi",
                },
                "requests": {"cpu": "1", "memory": "512Mi"},
            },
            "ports": [],
        },
        "service_account_name": "simulation-service-account",
        "regcred_secret_name": "regcred",
        "node_affinity": {"key": "is_compute", "operator": "in", "values": ["true"]},
        "annotations": [],
        "labels": [],
    }
