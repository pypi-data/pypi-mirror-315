# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

# from .context import src
from orionpy.orioncsv.csvrightsmanagement import CSVRightsManagement

# =============================================================================
# CLASS
# =============================================================================


class SimplifiedService:
    def __init__(self):
        self._is_managed = True

    def is_managed(self):
        return self._is_managed


# =============================================================================
# CLASS
# =============================================================================


class SimplifiedGroup:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


# =============================================================================
# CLASS
# =============================================================================


class TestCSVRightsManagement(unittest.TestCase):
    def setUp(self):
        self.csv_rights = CSVRightsManagement(None)
        self.service = SimplifiedService()
        self.group1 = SimplifiedGroup("g1")
        self.group2 = SimplifiedGroup("g2")
        self.group3 = SimplifiedGroup("g3")

    def test_generate(self):  # TODO tests
        pass

    def test_is_service_valid(self):
        # Error cases
        self.assertFalse(self.csv_rights._is_service_valid(None))
        self.service._is_managed = False
        self.assertFalse(self.csv_rights._is_service_valid(self.service))

        # Good case
        self.service._is_managed = True
        self.assertTrue(self.csv_rights._is_service_valid(self.service))

    def test_add_groups_header(self):  # TODO tests
        # Error case
        self.assertFalse(self.csv_rights._add_groups_header([], []))

        # Test with empty headers
        groups = [self.group1, self.group2, None, self.group3]
        # header = []
        self.assertListEqual(groups, self.csv_rights._add_groups_header(groups, []))

    def test_write_resource_information(self):  # TODO tests
        pass

    def test_read_and_apply(self):  # TODO tests
        pass

    def test_update_resource_right(self):  # TODO tests
        pass

    def test_update_good_rigt(self):  # TODO tests
        pass
