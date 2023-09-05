from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

# django >= 4.2
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage"
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage"
    }
}
