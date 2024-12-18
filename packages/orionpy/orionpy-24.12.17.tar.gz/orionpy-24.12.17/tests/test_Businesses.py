# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.resources.Businesses import Businesses
from orionpy.orioncore.resources.CadastreResource import CadastreResource
from orionpy.orioncore.resources.StatsResource import StatsResource
from orionpy.orioncore.resources.StorageResource import StorageResource

# =============================================================================
# CLASS
# =============================================================================


class TestServices(unittest.TestCase):
    def setUp(self):
        self.businesses = Businesses()

        # Requests preparation
        mockResourceList = [
            {
                "name": "rights",
                "nodeType": "ResourceProfileRightNode",
                "title": "Droits associés",
            },
            {
                "name": "catalogProperties",
                "nodeType": "ResourceAssociatedConfigNode",
                "title": "Proprietes associées au catalogue",
            },
            {
                "name": "Cadastre",
                "nodeInformationData": "cadastre",
                "nodeType": "ResourceNode",
                "title": "Cadastre",
            },
            {
                "name": "Stats",
                "nodeInformationData": "stats",
                "nodeType": "ResourceNode",
                "title": "Stats",
            },
        ]

        mockCadastre = {
            "_id": "AW-QT7J35pcaUHil1S0q",
            "definition": {
                "filterByCommunesId": "",
                "parcellesLayerReferenceIds": [],
                "serviceReference": "Monserver/0",
            },
            "description": "Données cadastrales",
            "module": "cadastre",
            "name": "Cadastre",
            "type": "business",
            "version": "1.0",
        }

        mockStats = {
            "description": "Définition du module de statistique",
            "module": "stats",
            "name": "Stats",
            "storageIds": ["standard"],
        }

        mockStorage = {
            "dimensionId": "",
            "id": "standard",
            "service": {"url": "Hosted/StatService/FeatureServer"},
            "tables": [],
            "type": "service",
        }

        # Prepares responses
        responses.add(
            responses.GET,
            "https://front.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/__children",
            json=mockResourceList,
            status=200,
        )

        responses.add(
            responses.GET,
            "https://front.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/Cadastre",
            json=mockCadastre,
            status=200,
        )

        responses.add(
            responses.GET,
            "https://front.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/Stats",
            json=mockStats,
            status=200,
        )

        responses.add(
            responses.GET,
            "https://front.arcopole.fr/Orion/orion/admin/tree/object/BUSINESS/Stats/hosted",
            json=mockStorage,
            status=200,
        )

    @responses.activate
    def test_all(self):
        resources = self.businesses.all()
        self.assertEqual(2, len(resources))

    @responses.activate
    def test_get(self):
        resource = self.businesses.get("Cadastre")
        self.assertIsNotNone(resource)
        self.assertTrue(isinstance(resource, CadastreResource))

        resource = self.businesses.get("Stats")
        self.assertIsNotNone(resource)
        self.assertTrue(isinstance(resource, StatsResource))

        resource = self.businesses.get("Unknow")
        self.assertIsNone(resource)

    @responses.activate
    def test_get_cadastre_resource(self):
        resource = self.businesses.get_cadastre_resource()
        self.assertIsNotNone(resource)
        self.assertTrue(isinstance(resource, CadastreResource))

    @responses.activate
    def test_get_stats_resource(self):
        resource = self.businesses.get_stats_resource()
        self.assertIsNotNone(resource)
        self.assertTrue(isinstance(resource, StorageResource))

        resource = self.businesses.get_stats_resource("Unknow")
        self.assertIsNone(resource)
