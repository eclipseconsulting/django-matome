from django.core.management.base import BaseCommand

import os

from ._code_stats import CodeStats


class Command(BaseCommand):

    help = "Report something nice for you."

    def handle(self, *args, **options):

        targets = [
            ('ALL', self._listup())
        ]

        self.stdout.write(CodeStats(targets).result)

    def _listup(self):
        targets = []
        for dname, subdirs, fnames in os.walk('.'):
            for fname in fnames:
                path = os.path.join(dname, fname)
                if os.path.isfile(path):
                    targets.append(path)
        return targets
