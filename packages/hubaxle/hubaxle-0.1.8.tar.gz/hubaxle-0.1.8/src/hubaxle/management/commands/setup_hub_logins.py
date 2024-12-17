from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Setup hub logins from HUB_LOGINS environment variable'

    #TODO: allow passing in hashed passwords instead of / in addition to plaintext
    # For this to be practical, we'll need a tool to easily hash the passwords
    # in a way that django accepts - probably using django itself.
    # We could also use the `hashers` module directly.

    def handle(self, *args, **options):
        logins = os.environ.get("HUB_LOGINS", "")
        login_lines = logins.split("\n")
        logger.info(f"Found {len(login_lines)} logins in HUB_LOGINS")
        for line_number, line in enumerate(login_lines, 1):
            line = line.strip()  # remove leading/trailing whitespace
            if (not line) or (line.startswith("#")):
                continue
            try:
                username, password = line.split(":", maxsplit=1)
            except ValueError:
                logger.error(f"Ignoring invalid HUB_LOGINS line#{line_number}")
                continue
            if not User.objects.filter(username=username).exists():
                logger.info(f"Created new user {username} from HUB_LOGINS line#{line_number}")
                user = User.objects.create_user(username, password=password)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            else:
                user = User.objects.get(username=username)
                if not user.check_password(password):
                    user.set_password(password)
                    user.save()
                    logger.info(f"Password updated for user {username} from HUB_LOGINS line#{line_number}")