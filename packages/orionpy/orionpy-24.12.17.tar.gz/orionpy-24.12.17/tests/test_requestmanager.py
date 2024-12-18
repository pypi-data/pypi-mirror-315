# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

import unittest

import requests
import responses

from orionpy.orioncore.Exceptions import RequestError
from orionpy.orioncore.RequestManager import RequestManager

# =============================================================================
# CLASS
# =============================================================================


class TestRequestManager(unittest.TestCase):
    # TODO : when test_group called before, creates bugs in this file
    """
    Unitary tests class for RequestManager
    """

    def setUp(self):
        self.requestMgr = RequestManager(
            output_format="json", token="token_value", verify=False
        )
        self.requestMgr.set_token(token="token_value")

    def test_singleton(self):
        req2 = RequestManager()
        self.assertIs(self.requestMgr, req2)

    def test_get_basedata(self):
        baseModel = {"f": "json", "token": "token_value"}
        self.assertDictEqual(baseModel, self.requestMgr.get_basedata())

    def test_set_token(self):
        self.requestMgr.set_token(token="new_token")
        self.assertEqual("new_token", self.requestMgr.get_basedata()["token"])

    def test_merge_data(self):
        expected = {"key1": "val1", "key2": "val2", "f": "json", "token": "token_value"}
        answer = self.requestMgr._merge_data(
            params={"key1": "val1", "key2": "val2"}, keep_base_parameters=True
        )
        self.assertDictEqual(expected, answer)

    @responses.activate
    def test_get(self):
        expected = {"test": "all is good"}
        responses.add(
            responses.GET, "http://url.fr/Orion/1/foobar", json=expected, status=200
        )
        self.assertDictEqual(
            self.requestMgr.get("http://url.fr/Orion/1/foobar").json(), expected
        )
        responses.add(
            responses.GET, "http://url.fr/Orion/wrong", json=expected, status=400
        )
        with self.assertRaises(RequestError):
            self.assertRaises(requests.exceptions.HTTPError)
            self.requestMgr.get("http://url.fr/Orion/wrong")

    @responses.activate
    def test_post(self):
        # NB no need to tests for param. As work for get and same method
        expected = {"test": "all is good"}
        responses.add(
            responses.POST, "http://url.fr/Orion/1/post", json=expected, status=200
        )
        self.assertDictEqual(
            self.requestMgr.post("http://url.fr/Orion/1/post").json(), expected
        )
        responses.add(
            responses.POST,
            "http://url.fr/Orion/1/post/wrong",
            json=expected,
            status=400,
        )
        with self.assertRaises(RequestError):
            self.assertRaises(requests.exceptions.HTTPError)
            self.requestMgr.post("http://url.fr/Orion/1/post/wrong")

    @responses.activate
    def test_post_in_python(self):
        expected = {"test": "all is good"}
        responses.add(
            responses.POST, "http://url.fr/Orion/1/post", json=expected, status=200
        )
        self.assertDictEqual(
            self.requestMgr.post_in_python("http://url.fr/Orion/1/post"), expected
        )

        expected["error"] = "error message in struct"
        responses.add(
            responses.POST,
            "http://url.fr/Orion/1/post/wrong",
            json=expected,
            status=200,
        )
        with self.assertRaises(RequestError):
            self.requestMgr.post_in_python("http://url.fr/Orion/1/post/wrong")

    @responses.activate
    def test_get_python_answer(self):
        expected = {"test": "all is good"}
        responses.add(
            responses.GET, "http://url.fr/Orion/1/get", json=expected, status=200
        )
        req = self.requestMgr.get("http://url.fr/Orion/1/get")
        self.assertDictEqual(self.requestMgr.get_python_answer(req), expected)
        expected["error"] = "error message in struct"
        responses.add(
            responses.GET, "http://url.fr/Orion/1/get/wrong", json=expected, status=200
        )
        with self.assertRaises(RequestError):
            req = self.requestMgr.get("http://url.fr/Orion/1/get/wrong")
            self.requestMgr.get_python_answer(req)

    @responses.activate
    def test_get_in_python(self):
        expected = {"test": "all is good"}
        responses.add(
            responses.GET, "http://url.fr/Orion/1/get", json=expected, status=200
        )
        self.assertDictEqual(
            self.requestMgr.get_in_python("http://url.fr/Orion/1/get"), expected
        )

        expected["error"] = "error message in struct"
        responses.add(
            responses.GET, "http://url.fr/Orion/1/get/wrong", json=expected, status=200
        )
        with self.assertRaises(RequestError):
            self.requestMgr.get_in_python("http://url.fr/Orion/1/get/wrong")
