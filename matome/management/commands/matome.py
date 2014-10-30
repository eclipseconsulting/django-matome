from django.core.management.base import BaseCommand

from ._code_stats import CodeStats


class Command(BaseCommand):

    help = "Report something nice for you."

    def handle(self, *args, **options):

        self.stdout.write(str(CodeStats(['ALL', '.'])))