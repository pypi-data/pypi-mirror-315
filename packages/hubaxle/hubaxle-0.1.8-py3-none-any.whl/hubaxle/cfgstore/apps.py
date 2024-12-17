import logging
import os
from pathlib import Path

from django.apps import AppConfig

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class CfgstoreConfig(AppConfig):
    """Class for configuring the configstore.
    (So meta!)
    """

    name = "hubaxle.cfgstore"
    verbose_name = "Configuration Store"
    storage_path = os.environ.get("GLHUB_CONFIG_PATH", "/opt/glhub/config")

    def ready(self):
        self.ensure_storage_path_exists()

    def ensure_storage_path_exists(self):
        storage_path = Path(self.storage_path)
        if not storage_path.exists():
            logger.info(f"Creating storage path at {storage_path}")
        storage_path.mkdir(parents=True, exist_ok=True)
