from pathlib import Path

from configurations import values
from wbcore.configurations import DevBaseConfiguration, ProductionBaseConfiguration
from wbcore.configurations.configurations import (
    Base,
    LocalMedia,
    S3Staticfiles,
    SSLNetwork,
    Uvicorn,
)
from wbcore.contrib.gleap.configurations import Gleap


class Dev(Gleap, DevBaseConfiguration):
    BASE_DIR = Path(__file__).parent.parent

    DATABASES = values.DatabaseURLValue(f"postgres://root:root@localhost:5432/db_wbcore")
    AWS_STORAGE_BUCKET_NAME = values.Value("wbcore", environ_prefix=None)

    WSGI_APPLICATION = "wbcore_config.wsgi.application"

    ROOT_URLCONF = "wbcore_config.urls"
    BOOTSTRAP_FIXTURES = ["currency", "geography", "directory", "authentication", "workflow", "example_app"]

    ADDITIONAL_APPS = ["wbcore.contrib.gleap", "wbcore.contrib.example_app"]
    AUTH_USER_MODEL = "authentication.User"
    INTERNAL_IPS = ["127.0.0.1"]

    @property
    def DEV_USERS(self):
        return [f"xue-bai@stainly.com:dev", "rodney-collins@stainly.com:dev", "admin@stainly.com:admin"]


class Test(LocalMedia, Dev):
    ADDITIONAL_APPS = ["wbcore.contrib.gleap"]


class Production(Uvicorn, SSLNetwork, S3Staticfiles, Dev):
    DEBUG = values.BooleanValue(False, environ_prefix=None)
