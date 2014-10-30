from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Report something nice for you."

    def handle(self, *args, **options):
        self.stdout.write("Yo! Not implemented anything.")