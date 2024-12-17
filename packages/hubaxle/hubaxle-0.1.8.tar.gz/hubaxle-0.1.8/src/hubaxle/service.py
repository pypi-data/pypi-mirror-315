import django 
from django.core.management import call_command
import os 
import logging 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hubaxle.settings')

# TODO: turn this off when we serve static files through nginx
os.environ["DJANGO_DEBUG"] = "True"
django.setup()

logger = logging.getLogger(__name__)


def launch() -> None:
    """This is the entry point for the "launch-service" command,
    as configured in `pyproject.toml`.  This command will start
    the hubaxle service, which is a Django web server that provides
    a REST API for interacting with the GLHub.
    """
    database_path = os.environ.get("DB_PATH")
    if not database_path:
        raise ValueError("DB_PATH environment variable must be set")
    DB_FILENAME = os.path.join(database_path, "db.sqlite3")
    
    if not os.path.isfile(DB_FILENAME):
        logger.info(f"SQLite database not found. Creating an empty file at {DB_FILENAME}")
        database_dir = os.path.dirname(DB_FILENAME) 
        os.makedirs(database_dir, exist_ok=True)
        open(DB_FILENAME, "w").close()
                
    # Setup stuff 
    logger.info("Running migrations and setting up hub logins")
    call_command("migrate")
    call_command("setup_hub_logins")
    call_command("sync_config_entries")
    
    # Start the server
    port = int(os.environ.get("HUBAXLE_PORT", 8000))
    logger.info(f"Starting the hubaxle server on port {port}")
    call_command("runserver", f"0.0.0.0:{port}")
