# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

from orionpy.orioncore.features.Geonote import Geonote

# =============================================================================
# CLASS
# =============================================================================


class TestGeonote(unittest.TestCase):
    def setUp(self):
        self.testKey = "testKey"
        self.testValue = "testValue"
        self.itemId = "itemId"
        self.theOwner = "theOwner"
        self.geonote = Geonote(
            {"id": self.itemId, "owner": self.theOwner, self.testKey: self.testValue}
        )

    def test_get_id(self):
        self.assertEqual(self.geonote.get_id(), self.itemId)

    def test_get_owner(self):
        self.assertEqual(self.geonote.get_owner(), self.theOwner)

    def test_get(self):
        self.assertEqual(self.geonote.get(self.testKey), self.testValue)
