from .settings import *  # noqa

import os

DEBUG = False

ALLOWED_HOSTS = [
    "briangaudino.dev",
    "www.briangaudino.dev",
    "briangaudino-b57112662916.herokuapp.com",
]

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": os.getenv("AWS_STORAGE_BUCKET_NAME"),
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDISCLOUD_URL"),
    }
}
