from django.test import TestCase
from utils import utils


class UtilsTests(TestCase):
    def test_sanitize_name_on_clean_name(self):
        name = "JJamali"
        self.assertEqual(name, utils.sanitize_name(name))

    def test_sanitize_name_on_dirty_name(self):
        dirty_name = "J  J+am//%al#i"
        expected = "JJamali"
        self.assertEqual(expected, utils.sanitize_name(dirty_name))
