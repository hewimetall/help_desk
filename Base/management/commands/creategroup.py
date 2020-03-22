from django.core.management.base import BaseCommand
from autch.models import CustomGroup
from django.core.management.base import BaseCommand

from autch.models import CustomGroup


class Command(BaseCommand):
    help = 'Create Group'

    def add_arguments(self, parser):
        parser.add_argument(
            '-l',
            '--label',
            action='store',
            default=False,
            help='exemp arg myapp.mybd'
        )

    def handle(self, *args, **options):
        if options['label']:
            CustomGroup
