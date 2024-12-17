from django.core.management.base import BaseCommand
from hubaxle.cfgstore.models import ConfigEntry

class Command(BaseCommand):
    help = 'Sync configuration entries from the database to the filesystem'

    def handle(self, *args, **options):
        ConfigEntry.save_all()
        ConfigEntry.reload_all()