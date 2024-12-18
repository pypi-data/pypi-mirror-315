# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import responses

# TODO why not ..src. here ??
from orionpy.orioncore.Exceptions import FilteringValuesError
from orionpy.orioncore.Filter import _FDUFilter, _SQLFilter
from orionpy.orioncore.Group import Group

# =============================================================================
# CLASS
# =============================================================================


class TestGroup(unittest.TestCase):
    """
    Unitary tests class for Group
    """

    def setUp(self):
        self.group = Group(title="title", group_id="group_id")
        partitions = [{"name": "val1"}, {"name": "val2"}, {"name": "val3"}]
        # TODO use FilterFactory instead
        self.fdu_filter = _FDUFilter(
            name="filter_fdu",
            attributeName=["attr"],
            partitions=partitions,
            filter_id="fdu_id",
        )
        self.sql_filter = _SQLFilter(
            name="filter_sql", whereClause="whereClause", filter_id="sql_id"
        )

        group_info_url = self.group._url_builder.group_information_url(
            self.group.get_id()
        )
        self.group_info = {
            "title": self.group.get_name(),
            "name": self.group.get_id(),
            "perimeters": [
                {"dimension": "fid", "valeures": "a,b"},
                {"dimension": self.fdu_filter.id, "valeures": "c,d"},
            ],
        }
        responses.add(responses.GET, group_info_url, json=self.group_info, status=200)

    def test_update_filters_values(self):  # TODO tests
        pass

    def test_reset_all_filters_values(self):  # TODO tests
        pass

    def test_set_filter_values(self):
        # Error cases tests
        # Test with a sql filter
        self.group.set_filter_values(fdu_filter=self.sql_filter, labels=["val"])
        self.assertRaisesRegex(
            FilteringValuesError,
            "[ERROR] Only possible to defined filtering values on a FDU filter",
        )

        # Test with no value set
        self.group.set_filter_values(fdu_filter=self.fdu_filter)
        self.assertRaisesRegex(
            FilteringValuesError,
            "[ERROR] If add_all is False, you must set selected_filtering_values !",
        )
        # Test with an empty list
        self.group.set_filter_values(fdu_filter=self.fdu_filter, labels=[])
        self.assertRaisesRegex(
            FilteringValuesError,
            "[ERROR] selected_filtering_values must not be an empty list",
        )

    def test_add_filtering_values(self):  # TODO tests
        pass

    def test_remove_filtering_values(self):  # TODO tests
        pass

    def test_apply_filtering_values(self):  # TODO tests
        pass

    def test_get_filter_index(self):  # TODO tests
        pass

    @responses.activate
    def test_get_filter_values(self):
        # error case test
        self.assertIsNone(self.group._get_filter_values("fake"))

        # Test with a filter defined
        vals = self.group._get_filter_values(self.fdu_filter.get_id())
        self.assertEqual(self.group_info["perimeters"][1]["valeures"], vals)

    @responses.activate
    def test_apply_configuration(self):
        group_conf_url = self.group._url_builder.group_configure_url(
            self.group.get_id()
        )
        responses.add(responses.GET, group_conf_url, json=self.group_info, status=200)
        self.group._apply_configuration(self.group_info)

    @responses.activate
    def test_group_information_minus_filter(self):
        expected = {
            "title": self.group.get_name(),
            "name": self.group.get_id(),
            "perimeters": [{"dimension": "fid", "valeures": "a,b"}],
        }
        self.assertDictEqual(
            expected, self.group._subject_information_minus_filter(self.fdu_filter)
        )

    def test_get_group_informations(self):  # TODO tests
        pass

    def test_build_perimeters(self):
        dict_tmp = self.group._build_perimeters(
            self.fdu_filter, ["val1", "ERR", "val2"]
        )
        self.assertDictEqual(dict_tmp, {"dimension": "fdu_id", "valeures": "val1,val2"})

    def test_remove_current_filter_val(self):
        list1 = [{"dimension": "id1"}, {"dimension": "id2"}]
        list2 = list(list1)
        # Tries to remove an element not defined in the list
        self.group._remove_current_filter_value(list1, "NOT_DEFINED")
        self.assertListEqual(list1, list2)

        # Removes an element already defined in the list
        self.group._remove_current_filter_value(list1, "id2")
        self.assertListEqual(list1, [{"dimension": "id1"}])

    # ----- Test methods -----

    @responses.activate
    def test_has_defined_filter_values(self):
        self.assertTrue(self.group.has_defined_filter_values(self.fdu_filter))

    def test_has_label_set_for_filter(self):  # TODO tests
        pass

    # ----- Access methods -----
    def test_get_name(self):
        self.assertEqual(self.group.get_name(), self.group.title)

    def test_get_id(self):
        self.assertEqual(self.group.get_id(), self.group.id)

    def test_get_activated_labels(self):  # TODO tests
        pass

    def test_print_defined_filtering_values(self):  # TODO tests
        pass

    def test_toStr(self):
        self.assertEqual('Group "title"; id group_id', self.group.__str__())
