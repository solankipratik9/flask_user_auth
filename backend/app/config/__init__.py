import os
from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(config_name=None):
    config_name = config_name or os.environ.get("CONFIG_NAME", "development")
    return CONFIG_MAP.get(config_name.lower(), DevelopmentConfig)
