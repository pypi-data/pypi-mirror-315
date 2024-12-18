# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

from orionpy.orioncore.resources.Service import Service
from orionpy.orioncore.resources.Services import Services

# =============================================================================
# CLASS
# =============================================================================


class TestServices(unittest.TestCase):
    def setUp(self):
        self.services = Services()

        # Requests preparation
        self.managed_service_list = ["Serv1/MapServer", "Path/to/serv2/FeatureServer"]
        serv1_definition = {
            "definition": {
                "capabilities": "Create,Query,Update",
                "portalItemId": "servid",
                "isManaged": True,
            }
        }
        serv2_definition = {
            "definition": {
                "capabilities": "Create",
                "portalItemId": "serv2id",
                "isManaged": True,
            }
        }
        serv_wrongtype_def = {
            "definition": {
                "capabilities": "Create",
                "portalItemId": "servWT",
                "isManaged": True,
            }
        }

        # Prepares responses
        responses.add(
            responses.GET,
            self.services.url_manager.managed_services_url(),
            json=self.managed_service_list,
            status=200,
        )
        responses.add(
            responses.GET,
            self.services.url_manager.resource_definition_url(
                "Path/to/serv2_FeatureServer"
            ),
            json=serv2_definition,
            status=200,
        )
        responses.add(
            responses.GET,
            self.services.url_manager.resource_definition_url("Serv1_MapServer"),
            json=serv1_definition,
            status=200,
        )
        responses.add(
            responses.GET,
            self.services.url_manager.resource_definition_url("Serv_WrongType"),
            json=serv_wrongtype_def,
            status=200,
        )

    def test_rreplace(self):
        s = "1232425"
        self.assertEqual("123 4 5", self.services._rreplace(s, "2", " ", 2))
        self.assertEqual(self.services._rreplace(s, "2", " ", 3), "1 3 4 5")
        self.assertEqual(self.services._rreplace(s, "2", " ", 4), "1 3 4 5")
        self.assertEqual(self.services._rreplace(s, "2", " ", 0), "1232425")

    def test_update(self):  # TODO test
        pass

    # def test_all_managed(self):  # TODO test
    #     pass

    def test_build_all(self):  # TODO test
        pass

    @responses.activate
    def test_create_service(self):
        # Test preparation
        service_url = "Serv1_MapServer"

        # TestNormalCase
        self.services._add_service_to_list(service_url, for_managed=False)
        expected = Service(
            "servid", service_url, capabilities="Create,Query,Update", is_managed=True
        )
        self.assertEqual(
            expected.__str__(), self.services._elements[service_url].__str__()
        )
        self.services._add_service_to_list(service_url, for_managed=True)
        self.assertEqual(
            expected.__str__(), self.services._managed_services[service_url].__str__()
        )

        self.services._add_service_to_list("Serv_WrongType")

    def test_good_service_type(self):
        self.services.handled_service_types = ["Type1", "Type2"]
        self.assertTrue(self.services._good_service_type("test_Type1"))
        # test case insensitive
        self.assertTrue(self.services._good_service_type("test_type1"))
        self.assertFalse(self.services._good_service_type("test_typeFAL"))
        self.assertFalse(self.services._good_service_type("Type1_"))

    @responses.activate
    def test_update_managed(self):
        self.services._update_managed()
        expected1 = Service(
            "servid", "Serv1_MapServer", "Create,Query,Update", is_managed=True
        )
        expected2 = Service(
            "serv2id", "Path/to/serv2_FeatureServer", "Create", is_managed=True
        )
        self.assertEqual(
            expected1.__str__(),
            self.services._managed_services["Serv1_MapServer"].__str__(),
        )
        self.assertEqual(
            expected2.__str__(),
            self.services._managed_services["Path/to/serv2_FeatureServer"].__str__(),
        )
        self.assertIsInstance(
            self.services._managed_services["Serv1_MapServer"], Service
        )
        self.assertEqual(
            len(self.services._managed_services), len(self.managed_service_list)
        )

    @responses.activate
    def test_get_in_managed(
        self,
    ):  # Does the test here so we don't have to redefine all responses
        self.assertIsInstance(
            self.services.get_in_managed("Serv1_MapServer  "), Service
        )
        self.assertIsNone(self.services.get_in_managed("WRONG"))

    @responses.activate
    def test_all_managed(self):
        self.assertEqual(
            len(self.managed_service_list), len(self.services.all_managed())
        )

    def test_urls(self):  # TODO test
        pass
