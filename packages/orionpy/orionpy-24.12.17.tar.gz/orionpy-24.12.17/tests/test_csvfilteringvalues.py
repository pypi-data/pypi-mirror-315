# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

from orionpy.orioncsv.csvfilteringvalues import CSVFilteringValues

# =============================================================================
# CLASS
# =============================================================================


class SimplifiedGroup:
    def __init__(self):
        self.add_called = False
        self.rmv_called = False

    def add_filtering_values(self, fdu_filter, labels):
        self.add_called = True
        self.rmv_called = False

    def remove_filtering_values(self, fdu_filter, labels):
        self.add_called = False
        self.rmv_called = True


class TestCsvFilteringValues(unittest.TestCase):
    def setUp(self):
        self.csv_filtering_values = CSVFilteringValues(None)
        self.group = SimplifiedGroup()

    def test_generate(self):  # TODO tests
        pass

    def test_read_and_apply(self):  # TODO tests
        pass

    def test_change_group_filtering_value(self):  # TODO tests
        self.csv_filtering_values._change_group_filtering_value(
            self.group, None, None, 0
        )
        self.assertFalse(self.group.add_called)
        self.assertTrue(self.group.rmv_called)

        self.csv_filtering_values._change_group_filtering_value(
            self.group, None, None, 1
        )
        self.assertTrue(self.group.add_called)
        self.assertFalse(self.group.rmv_called)
