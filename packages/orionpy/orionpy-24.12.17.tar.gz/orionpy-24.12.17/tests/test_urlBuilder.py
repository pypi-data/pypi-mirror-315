# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

from orionpy.orioncore.UrlBuilder import UrlBuilder

# =============================================================================
# CLASS
# =============================================================================


class TestUrlBuilder(unittest.TestCase):
    """
    Unitary tests class for UrlBuilder
    """

    def setUp(self):
        self.urlBuilder = UrlBuilder("https://front.arcopole.fr", "portal")
        self.orionHeader = "https://front.arcopole.fr/Orion/orion"
        self.apiHeader = "https://front.arcopole.fr/Orion/orion/admin/tree"

    def test_singleton(self):
        url2 = UrlBuilder()
        self.assertIs(self.urlBuilder, url2)

    def test_api_header_url(self):
        url = self.urlBuilder._api_header_url()
        self.assertEqual(url, self.apiHeader)

    def test_aob_config_url(self):
        url = self.urlBuilder.aob_config_url()
        self.assertEqual(
            url, self.urlBuilder.base_url + "/aob-admin/app/aobconfig.json"
        )

    def test_user_info_url(self):
        url = self.urlBuilder.user_info_url(usr_login="login", usr_domain="domain")
        self.assertEqual(url, self.apiHeader + "/rightmanagement/users/login(domain)")

    def test_token_url(self):
        url = self.urlBuilder.token_url()
        self.assertEqual(
            url, "https://front.arcopole.fr/portal/sharing/rest/generateToken"
        )

    def test_filter_list_url(self):
        url = self.urlBuilder.filter_list_url()
        self.assertEqual(url, self.apiHeader + "/config/dimensions")

    def test_filter_config_url(self):
        url = self.urlBuilder.filter_config_url()
        self.assertEqual(url, self.apiHeader + "/config/dimensions/__configure")

    def test_right_management_profiles_url(self):
        url = self.urlBuilder.right_management_profiles_url("pId")
        self.assertEqual(
            url, self.apiHeader + "/rightmanagement/profiles/pId/aobrights"
        )

    # ----- Ressource urls -----
    def test_resource_definition_url(self):
        url = self.urlBuilder.resource_definition_url("Serv_MapServer")
        self.assertEqual(self.apiHeader + "/object/SERVICES/Serv_MapServer", url)
        url = self.urlBuilder.resource_definition_url("Serv_MapServer/0")
        self.assertEqual(self.apiHeader + "/object/SERVICES/Serv_MapServer/0", url)

    def test_resource_rights_url(self):
        url = self.urlBuilder.resource_rights_url("gId", "Serv_MapServer")
        self.assertEqual(
            self.apiHeader
            + "/rightmanagement/profiles/gId/aobrights/SERVICES/Serv_MapServer",
            url,
        )
        url = self.urlBuilder.resource_rights_url("gId", "Serv_MapServer/0")
        self.assertEqual(
            self.apiHeader
            + "/rightmanagement/profiles/gId/aobrights/SERVICES/Serv_MapServer/0",
            url,
        )

    def test_resource_resolved_permissions_url(self):
        url = self.urlBuilder.resource_resolved_permissions_url("gId", "Serv_MapServer")
        self.assertEqual(
            self.apiHeader
            + "/rightmanagement/groups/gId/authorizedResources/SERVICES/Serv_MapServer",
            url,
        )

    def test_resource_configuration_group_url(self):
        url = self.urlBuilder.resource_configuration_url("gId", "Serv_MapServer")
        self.assertEqual(
            self.apiHeader
            + "/rightmanagement/profiles/gId/aobrights/SERVICES/Serv_MapServer/__configure",
            url,
        )
        url = self.urlBuilder.resource_configuration_url("gId", "Serv_MapServer/0")
        self.assertEqual(
            self.apiHeader
            + "/rightmanagement/profiles/gId/aobrights/SERVICES/Serv_MapServer/0/__configure",
            url,
        )

    def test_resource_management_url(self):
        url = self.urlBuilder.resource_management_url("Serv_MapServer")
        self.assertEqual(
            url, self.apiHeader + "/object/SERVICES/Serv_MapServer/__managing"
        )
        url = self.urlBuilder.resource_management_url("Serv_MapServer/0")
        self.assertEqual(
            url, self.apiHeader + "/object/SERVICES/Serv_MapServer/0/__managing"
        )

    def test_resource_shared_with_url(self):
        url = self.urlBuilder.resource_sharing_url("rId")
        self.assertEqual(
            url,
            "https://front.arcopole.fr/portal/sharing/rest/content/users/admin_aob/items/rId",
        )

    # ----- Cadastre resource urls -----

    def test_cadastre_definition_url(self):
        url = self.urlBuilder.cadastre_definition_url()
        self.assertEqual(self.apiHeader + "/object/BUSINESS/Cadastre", url)

    def test_cadastre_configuration_url(self):
        url = self.urlBuilder.cadastre_configuration_url("gId")
        self.assertEqual(
            self.apiHeader
            + "/rightmanagement/profiles/gId/aobrights/BUSINESS/Cadastre/__configure",
            url,
        )

    def test_cadastre_rights_url(self):
        url = self.urlBuilder.cadastre_rights_url("gId")
        self.assertEqual(
            self.apiHeader
            + "/rightmanagement/profiles/gId/aobrights/BUSINESS/Cadastre",
            url,
        )

    # ----- Service urls -----
    def test_managed_services_url(self):
        url = self.urlBuilder.managed_services_url()
        self.assertEqual(url, self.orionHeader + "/federatedLink/managedServiceList")

    def test_main_services_url(self):
        url = self.urlBuilder.main_services_url()
        self.assertEqual(url, self.apiHeader + "/object/SERVICES")

    # ----- Layer urls -----
    def test_layer_list_url(self):
        url = self.urlBuilder.layer_list_url("Cannes/EspacesVerts/FeatureServer")
        self.assertEqual(
            self.apiHeader + "/rest/services/Cannes/EspacesVerts/FeatureServer/layers",
            url,
        )

    def test_main_group_url(self):
        url = self.urlBuilder._main_group_url()
        self.assertEqual(url, self.apiHeader + "/rightmanagement/groups")

    # def test_group_list_url(self):
    #     url = self.urlBuilder.group_list_url()
    #     self.assertEqual(self.apiHeader + '/rightmanagement/groups/__children', url)

    def test_group_information_url(self):
        url = self.urlBuilder.group_information_url(group_id="groupId")
        self.assertEqual(self.apiHeader + "/rightmanagement/groups/groupId", url)

    def test_group_configure_url(self):
        url = self.urlBuilder.group_configure_url(group_id="groupId")
        self.assertEqual(
            self.apiHeader + "/rightmanagement/groups/groupId/__configure", url
        )

    def test_profile_information_url(self):
        url = self.urlBuilder.profile_information_url("pId")
        self.assertEqual(url, self.apiHeader + "/rightmanagement/profiles/pId")

    # ----- Features urls -----
    def test_base_feature_url(self):
        url_g = self.urlBuilder.base_feature_url("Feature Collection")
        self.assertEqual(self.orionHeader + "/geonote", url_g)

        url_p = self.urlBuilder.base_feature_url("Document Link")
        self.assertEqual(self.orionHeader + "/project", url_p)

    def test_search_feature_url(self):
        url_g = self.urlBuilder.search_feature_url("Feature Collection")
        self.assertEqual(self.orionHeader + "/geonote/search", url_g)

        url_p = self.urlBuilder.search_feature_url("Document Link")
        self.assertEqual(self.orionHeader + "/project/search", url_p)

    def test_search_all_feature_url(self):
        url_g = self.urlBuilder.search_all_feature_url("Feature Collection")
        self.assertEqual(self.orionHeader + "/geonote/searchAll", url_g)

        url_p = self.urlBuilder.search_all_feature_url("Document Link")
        self.assertEqual(self.orionHeader + "/project/searchAll", url_p)

    def test_data_feature_url(self):
        self.itemId = "itemId"

        url_g = self.urlBuilder.data_feature_url(self.itemId, "Feature Collection")
        self.assertEqual(
            self.orionHeader + "/geonote/content/items/" + self.itemId + "/data", url_g
        )

        url_p = self.urlBuilder.data_feature_url(self.itemId, "Document Link")
        self.assertEqual(
            self.orionHeader + "/project/content/items/" + self.itemId + "/data", url_p
        )

    def test_main_feature_url(self):
        self.user = "user"

        url_g = self.urlBuilder._main_feature_url("Feature Collection", self.user)
        self.assertEqual(
            self.orionHeader + "/geonote/content/users/" + self.user, url_g
        )

        url_p = self.urlBuilder._main_feature_url("Document Link", self.user)
        self.assertEqual(
            self.orionHeader + "/project/content/users/" + self.user, url_p
        )

    def test_update_del_rea_feature(self):
        self.user = "user"
        self.itemId = "itemId"

        url_g = self.urlBuilder._update_del_rea_feature(
            "Feature Collection", self.user, self.itemId
        )
        self.assertEqual(
            self.orionHeader
            + "/geonote/content/users/"
            + self.user
            + "/items/"
            + self.itemId,
            url_g,
        )

        url_p = self.urlBuilder._update_del_rea_feature(
            "Document Link", self.user, self.itemId
        )
        self.assertEqual(
            self.orionHeader
            + "/project/content/users/"
            + self.user
            + "/items/"
            + self.itemId,
            url_p,
        )

    def test_add_item_feature_url(self):
        self.user = "user"

        url_g = self.urlBuilder.add_item_feature_url("Feature Collection", self.user)
        self.assertEqual(
            self.orionHeader + "/geonote/content/users/" + self.user + "/addItem", url_g
        )

        url_p = self.urlBuilder.add_item_feature_url("Document Link", self.user)
        self.assertEqual(
            self.orionHeader + "/project/content/users/" + self.user + "/addItem", url_p
        )

    def test_update_item_feature_url(self):
        self.user = "user"
        self.itemId = "itemId"

        url_g = self.urlBuilder.update_item_feature_url(
            "Feature Collection", self.user, self.itemId
        )
        self.assertEqual(
            url_g,
            self.orionHeader
            + "/geonote/content/users/"
            + self.user
            + "/items/"
            + self.itemId
            + "/update",
        )

        url_p = self.urlBuilder.update_item_feature_url(
            "Document Link", self.user, self.itemId
        )
        self.assertEqual(
            url_p,
            self.orionHeader
            + "/project/content/users/"
            + self.user
            + "/items/"
            + self.itemId
            + "/update",
        )

    def test_delete_feature_url(self):
        self.user = "user"
        self.itemId = "itemId"

        url_g = self.urlBuilder.delete_feature_url(
            "Feature Collection", self.user, self.itemId
        )
        self.assertEqual(
            url_g,
            self.orionHeader
            + "/geonote/content/users/"
            + self.user
            + "/items/"
            + self.itemId
            + "/delete",
        )

        url_p = self.urlBuilder.delete_feature_url(
            "Document Link", self.user, self.itemId
        )
        self.assertEqual(
            url_p,
            self.orionHeader
            + "/project/content/users/"
            + self.user
            + "/items/"
            + self.itemId
            + "/delete",
        )

    def test_reassign_feature_url(self):
        self.user = "user"
        self.itemId = "itemId"

        url_g = self.urlBuilder.reassign_feature_url(
            "Feature Collection", self.user, self.itemId
        )
        self.assertEqual(
            url_g,
            self.orionHeader
            + "/geonote/content/users/"
            + self.user
            + "/items/"
            + self.itemId
            + "/reassign",
        )

        url_p = self.urlBuilder.reassign_feature_url(
            "Document Link", self.user, self.itemId
        )
        self.assertEqual(
            url_p,
            self.orionHeader
            + "/project/content/users/"
            + self.user
            + "/items/"
            + self.itemId
            + "/reassign",
        )

    def test_stats_status_url(self):
        url = self.urlBuilder.stats_status_url()
        self.assertEqual(url, self.orionHeader + "/stats/status")

    def test_stats_push_url(self):
        url = self.urlBuilder.stats_push_url()
        self.assertEqual(url, self.orionHeader + "/stats/push")

    def test_stats_heartBeat_url(self):
        url = self.urlBuilder.stats_heartBeat_url()
        self.assertEqual(url, self.orionHeader + "/stats/heartBeat")

    def test_stats_newSession_url(self):
        url = self.urlBuilder.stats_newSession_url()
        self.assertEqual(url, self.orionHeader + "/stats/newSession")

    def test_stats_synthesis_url(self):
        url = self.urlBuilder.stats_synthesis_url()
        self.assertEqual(url, self.orionHeader + "/stats/synthesis")

    def test_stats_clean_url(self):
        url = self.urlBuilder.stats_clean_url()
        self.assertEqual(url, self.orionHeader + "/stats/clean")
