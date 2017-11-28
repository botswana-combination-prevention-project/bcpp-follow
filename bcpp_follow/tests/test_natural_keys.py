from django.test import TestCase

from edc_sync.tests import SyncTestHelper

from .worklist_test_helper import WorkListTestHelper


class TestNaturalKey(TestCase):

    sync_helper = SyncTestHelper()
    worklist_helper = WorkListTestHelper()

    def test_natural_key_attrs(self):
        self.sync_helper.sync_test_natural_key_attr('bcpp_follow')

    def test_get_by_natural_key_attr(self):
        self.sync_helper.sync_test_get_by_natural_key_attr('bcpp_follow')
