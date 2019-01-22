from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load Apache log.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='Link to Apache log file')

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        print(url)