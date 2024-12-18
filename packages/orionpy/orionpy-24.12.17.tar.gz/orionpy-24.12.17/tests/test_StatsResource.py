# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

from orionpy.orioncore.resources.StatsResource import StatsResource

# =============================================================================
# CLASS
# =============================================================================


class TestStatsResource(unittest.TestCase):
    def test_instance(self):
        resource = StatsResource(
            {
                "description": "Définition du module de statistique",
                "module": "stats",
                "name": "Stats",
                "storageIds": ["standard"],
            }
        )
        self.assertTrue("Stats" in str(resource))
