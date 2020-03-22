from django.core.management.base import BaseCommand
from Base.models import CustomGroup
from Base.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import PasswordChangeForm
import json
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Migrate users and groups'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--file',
            action='store',
            default=False,
            help='exemp arg user.json'
        )
    
    def handle(self, *args, **options):
        if options['file']:
            with open(options['file'], "r") as read_file:
                gr, users = json.load(read_file).values()
                users     = [[str(i[0]).lower(),i[1],i[2]] for i in users]
                self.saveGroups(gr)
                self.saveUsers(users)
                self.addGroupsUser(users)

    def saveGroups(self, gr):
        for i in gr:
            try:
                CustomGroup.objects.get(name=i)
            except ObjectDoesNotExist:
                log.warning(f" group {i} does not.Create...  ")
                gN = CustomGroup(name=i)
                gN.save()
        log.info(f"Groups: {gr}")

    def saveUsers(self, users):
        for user in users:
            try:
                CustomUser.objects.get(username=user[0])
            except ObjectDoesNotExist:
                u = CustomUser(username=str(user[0]).lower(),full_name=user[1],is_active=True)
                u.set_password("test_password_123")
                u.save()
        log.info(f"Users:{users}")

    def addGroupsUser(self, users):
        for user in users:
            user_name=user[0]
            user_group=user[2]
            try:
                gr = CustomGroup.objects.get(name=user_group)
                u  = CustomUser.objects.get(username=user_name)
                u.groups.add(gr)
                log.info(f"user {u.username} add in group {gr.name}")
            except ObjectDoesNotExist:
                log.warn("users {} not add group {} ".format(user_name,user_group))