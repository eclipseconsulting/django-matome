from django.core.management.base import BaseCommand

import os
from collections import OrderedDict

from ._code_stats import SummaryPresenter


class Command(BaseCommand):

    help = "Report something nice for you."

    def handle(self, *args, **options):

        targets = self.sniff()
        output = SummaryPresenter.summarize(targets)
        self.stdout.write(output)

    def sniff(self):
        targets = OrderedDict()
        targets['Models'] = []
        targets['Views'] = []
        targets['Filters'] = []
        targets['Forms'] = []
        targets['Routes'] = []
        targets['Helpers'] = []
        targets['Signals'] = []
        targets['Management Commands'] = []
        targets['Tests'] = []
        targets['Other Modules'] = []
        targets['HTML Templates'] = []


        for dname, subdirs, fnames in os.walk('.'):
            for fname in fnames:
                path = os.path.join(dname, fname)
                if os.path.isfile(path):
                    category = self.categorize(path)
                    if category:
                        if not category in targets:
                            targets[category] = []
                        targets[category].append(path)
        return targets

    def categorize(self, fname):
        ignored_directory = 'node_modules'
        if ignored_directory in fname:
            return ''
        if fname.endswith('views.py'):
            return 'Views'
        elif fname.endswith('models.py'):
            return 'Models'
        elif fname.endswith('urls.py'):
            return 'Routes'
        if fname.endswith('forms.py'):
            return 'Forms'
        if fname.endswith('filters.py'):
            return 'Filters'
        if fname.endswith('helpers.py'):
            return 'Helpers'
        if fname.endswith('signals.py'):
            return 'Signals'
        if 'test' in fname:
            return 'Test'
        if 'management' in fname and 'commands' in fname:
            return 'Management Commands'
        if fname.endswith('.html'):
            return 'HTML Templates'
        elif fname.endswith('.py'):
            return 'Other Modules'
        else:
            return ''
