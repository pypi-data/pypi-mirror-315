CONTAINER_HUB_CARRIER = "kubernetes"
CONTAINER_HUB_CLIENT_URL = "http://kubernetes_url/"
CONTAINER_HUB_NAMESPACE = "threedi"


# Note: Below are defaults that can always be overriden in code before
# sending it to Kubernetes
CONTAINER_HUB_KUBERNETES_CONTAINER_DEFAULTS = {
    "HOST_ALIASES": {
        "127.0.0.1": ["minio"],
    },
    "REDIS": {
        "name": "redis",
        "image": "redis:5.0.3-alpine",
        "args": ["sh", "-c", "rm -rf /data/dump.rdb && redis-server --save " ""],
        "ports": [
            6379,
        ],
    },
    "SCHEDULER": {
        "name": "scheduler",
        "image": "harbor.lizard.net/threedi/scheduler:latest",
        "args": ["python3", "/code/scheduler.py", "localhost"],
        "envs": {
            "DJANGO_SETTINGS_MODULE": "threedi_scheduler.developmentsettings",
            "REDIS_HOST": "localhost",
        },
        "mounts": {
            "/local/path/one": {"bind": "mount_path_1", "ro": True},
            "/local/path/two": {"bind": "mount_path_2", "ro": False},
            "scheduler-config": {
                "bind": "/etc/config/config.yaml",
                "ro": True,
                "type": "CONFIGMAP",
            },
            "scheduler-secret": {"bind": "/etc/secrets/", "ro": True, "type": "SECRET"},
            "shared-data": {
                "bind": "/mnt/results/",
                "ro": False,
                "type": "EMPTYDIR",
                "size_limit": "10Gi",
            },
        },
        "resources": {
            "limits": {
                "cpu": "1",
                "memory": "2Gi",
            },
            "requests": {"cpu": "250m", "memory": "128Mi"},
        },
    },
    "SIMULATION": {
        "name": "simulation",
        "image": "harbor.lizard.net/threedi/threedicore:2.16.1-2.2.5",
        "args": ["python", "service.py", "localhost"],
        "envs": {"RESULTS_PATH": "/results"},
        "mounts": {
            "/local/path/one": {"bind": "mount_path_1", "ro": True},
            "/local/path/two": {"bind": "mount_path_2", "ro": False},
            "shared-data": {
                "bind": "/mnt/results/",
                "ro": False,
                "type": "EMPTYDIR",
                "size_limit": "10Gi",
            },
        },
        "resources": {
            "limits": {
                "cpu": "1",
                "memory": "5Gi",
            },
            "requests": {"cpu": "1", "memory": "512Mi"},
        },
    },
    "regcred_secret_name": "regcred",
    "node_affinity": {
        "key": "is_compute",
        "operator": "in",
        "values": ["true"],
    },
}
