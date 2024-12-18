# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import csv
import unittest

from orionpy.orioncsv.orioncsv import OrionCSV

# =============================================================================
# CLASS
# =============================================================================


class TestOrionCSV(unittest.TestCase):
    def setUp(self):
        self.orioncsv = OrionCSV(None)
        self.csv_path = "./csv_test"

    def test_get_csv_writer(self):
        with open(self.csv_path, "w+", encoding="utf-8-sig", newline="") as csv_file:
            self.assertIsInstance(
                self.orioncsv.get_csv_writer(csv_file, []), csv.DictWriter
            )

    def test_get_csv_reader(self):  # TODO tests
        # with open(self.csv_path, "r+") as csv_file:
        # self.assertIsNotNone(self.orioncsv.get_csv_reader(None))
        pass
