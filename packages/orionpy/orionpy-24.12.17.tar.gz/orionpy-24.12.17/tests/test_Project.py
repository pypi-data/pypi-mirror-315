# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

from orionpy.orioncore.features.Project import Project

# =============================================================================
# CLASS
# =============================================================================


class TestProject(unittest.TestCase):
    def setUp(self):
        self.testKey = "testKey"
        self.testValue = "testValue"
        self.itemId = "itemId"
        self.theOwner = "theOwner"
        self.project = Project(
            {"id": self.itemId, "owner": self.theOwner, self.testKey: self.testValue}
        )

    def test_get_id(self):
        self.assertEqual(self.project.get_id(), self.itemId)

    def test_get_owner(self):
        self.assertEqual(self.project.get_owner(), self.theOwner)

    def test_get(self):
        self.assertEqual(self.project.get(self.testKey), self.testValue)
