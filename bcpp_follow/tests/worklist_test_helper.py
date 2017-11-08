from model_mommy import mommy

from unittest.case import TestCase

from edc_base.utils import get_utcnow

from ..models import WorkList


class WorkListTestHelper(TestCase):

    """A TestMixin class that adds methods specific to WorkList processes.
    """

    def make_worklist(self, **options):
        """Returns a worklist instance as would be made initially by
        the server."""
        opts = {}
        for field in WorkList._meta.get_fields():
            if field.name in options:
                opts.update({field.name: options.get(field.name)})
        opts['report_datetime'] = options.get(
            'report_datetime', get_utcnow())
        opts['subject_identifier'] = options.get(
            'subject_identifier')
        opts['map_area'] = options.get(
            'map_area')
        worklist = WorkList.objects.create(**opts)
        return worklist
