from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'recive db fields'

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
            myapp, mybase = options['label'].split(".")
            model = apps.get_model(app_label=myapp, model_name=mybase)
            listi = [i.name for i in model._meta.get_fields()]
            print(listi)
