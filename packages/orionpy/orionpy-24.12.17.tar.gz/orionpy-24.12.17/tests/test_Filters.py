# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import json
import unittest

from orionpy.orioncore.Exceptions import BuildFilterError
from orionpy.orioncore.Filters import Filters

# =============================================================================
# CLASS
# =============================================================================


class TestFilters(unittest.TestCase):
    def setUp(self):
        self.filters = Filters()

    def test_update(self):  # TODO test
        pass

    def test_label_already_used(self):
        filtering_names = [{"name": "label"}, {"name": "titi"}, {"name": "toto"}]
        self.assertTrue(self.filters._label_already_used(filtering_names, "label"))
        self.assertFalse(self.filters._label_already_used(filtering_names, "NOT HERE"))

    def test_build_partition_1_attr(self):
        model = [
            {"name": "val1", "properties": {"attr": "val1"}},
            {"name": "val2", "properties": {"attr": "val2"}},
        ]
        res = self.filters._build_partition_1_attr("attr", ["val1", "val2", "val2"])
        for expected, received in zip(model, res):
            self.assertDictEqual(expected, received)

    def test_build_partitions_attributes(self):
        model = [
            {"name": "v11", "properties": {"a1": "v11", "a2": "v12"}},
            {"name": "v21", "properties": {"a1": "v21", "a2": "v22"}},
            {"name": "v31", "properties": {"a1": "v31", "a2": "v32"}},
        ]

        res = self.filters._build_partitions_attributes(
            ["a1", "a2"],
            [["v11", "v12"], ["v21", "v22"], ["v21", "v22"], ["v31", "v32"]],
        )
        for expected, received in zip(model, res):
            self.assertDictEqual(expected, received)

        self.assertIsNone(
            self.filters._build_partitions_attributes(["a"], [["a", "b"]])
        )

    def test__build_list_filtering_values(self):
        self.assertIsNone(self.filters._build_list_filtering_values([], []))
        self.assertIsNotNone(
            self.filters._build_list_filtering_values(
                ["a1", "a2"], [["v11", "v12"], ["v21", "v22"], ["v31", "v32"]]
            )
        )
        self.assertIsNotNone(
            self.filters._build_list_filtering_values("attr", ["val1", "val2"])
        )

    def test_add_FDU_filter(self):
        self.filters.add_FDU_filter("fname", ["attr", "atr2"], ["val2"])
        self.assertRaisesRegex(
            BuildFilterError, "[ERROR FDU] Error while creating partition"
        )

    def test_add_SQL_filter(self):
        self.filters.add_SQL_filter("fname", "")
        self.assertRaises(BuildFilterError)

    def _apply_update_on_fdu_fv(self):  # TODO tests
        pass

    def test_update_sql_filter_value(self):
        pass

    def test_create_filter(self):
        self.filters.create_filter()

    def test_remove_filter(self):
        pass

    def test_add_list(self):  # TODO tests
        pass

    def test_add_to_filter_dict(self):
        class AD:
            def __init__(self):
                self.el = "a"
                self.el2 = 1

        a = AD()
        expected = {"el": "a", "el2": 1}
        self.filters._filters_as_dic = []
        self.filters._add_to_filter_dict(a)
        self.assertDictEqual(expected, self.filters._filters_as_dic[-1])

    def test_rmv_from_filter_dict(self):
        class AD:
            def __init__(self):
                self.name = "el2"

        test_filter = {"name": "el2"}
        model = [{"name": "el1"}, {"name": "el3", "test": "value"}]
        self.filters._filters_as_dic = model + [test_filter]
        self.filters._rmv_from_filter_dict(AD())
        self.assertListEqual(model, self.filters._filters_as_dic)
        for expected, received in zip(model, self.filters._filters_as_dic):
            self.assertDictEqual(expected, received)

    def test_update_fsql_on_filter_dict(self):
        expected = [
            {"name": "el1"},
            {"name": "el3", "whereClause": "test"},
            {"name": "el2", "whereClause": "wc new"},
        ]
        self.filters._filters_as_dic = [
            {"name": "el1"},
            {"name": "el2", "whereClause": "wc1"},
            {"name": "el3", "whereClause": "test"},
        ]
        self.filters._update_fsql_on_filter_dict("el2", "wc new")

        self.assertListEqual(expected, self.filters._filters_as_dic)
        for e, received in zip(expected, self.filters._filters_as_dic):
            self.assertDictEqual(e, received)

    def test_update_fdu_on_filter_dict(self):
        class AD:
            def __init__(self, fields, partitions):
                self.name = "el1"
                self.fields = fields
                self.partitions = partitions

            def get_name(self):
                return self.name

            def get_fields(self):
                return self.fields

        f_1 = AD(
            ["a"],
            [
                [
                    {"name": "l1", "properties": {"a": "v1"}},
                    {"name": "l2", "properties": {"a": "v2"}},
                ]
            ],
        )
        expected = [
            {"name": "el2", "whereClause": "wc1"},
            {"name": "el3", "whereClause": "test"},
            {
                "name": "el1",
                "attributeName": ["a"],
                "partitions": [
                    [
                        {"name": "l1", "properties": {"a": "v1"}},
                        {"name": "l2", "properties": {"a": "v2"}},
                    ]
                ],
            },
        ]
        self.filters._filters_as_dic = [
            {"name": "el1"},
            {"name": "el2", "whereClause": "wc1"},
            {"name": "el3", "whereClause": "test"},
        ]
        self.filters._update_fdu_on_filter_dict(f_1)
        self.assertListEqual(expected, self.filters._filters_as_dic)
        for e, received in zip(expected, self.filters._filters_as_dic):
            self.assertDictEqual(e, received)

    def test_filters_formatted(self):
        self.filters._filters_as_dic = [{"el": "a", "el2": 1}]
        expected = {"dimensions": [{"el": "a", "el2": 1}]}
        self.assertDictEqual(expected, json.loads(self.filters._filters_formatted()))

    def test_apply_changes(self):
        pass

    def test_filter_exist_already(self):
        self.assertTrue(self.filters._filter_exist_already("here", ["a", "here", "g"]))
        self.assertFalse(self.filters._filter_exist_already("wrong", ["a", "f"]))
