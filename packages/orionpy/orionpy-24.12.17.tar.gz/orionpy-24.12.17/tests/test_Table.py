# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

from orionpy.orioncore.resources.Fields import Fields
from orionpy.orioncore.resources.Table import Table

# =============================================================================
# CLASS
# =============================================================================


class TestTable(unittest.TestCase):
    def setUp(self):
        description = {"id": "tid", "name": "tname"}
        self.table = Table(
            description=description, parent_service_url="serv", is_managed=True
        )

    def test_fields(self):
        self.assertIsInstance(self.table.fields, Fields)

    def test_can_activate_FDU(self):  # TODO test
        # First test will exit at super can_activate_fdu
        self.assertFalse(self.table._can_activate_FDU(None, None, None))

    def test_str(self):
        self.assertEqual(
            "Table tid; name tname; for Service serv", self.table.__str__()
        )
