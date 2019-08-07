'''
Created on June 3, 2019
@author: Andrew Habib
'''

import unittest

from jsonsubschema.api import isSubschema


class TestMixedTypes(unittest.TestCase):

    def test_t_t_1(self):
        s1 = {"type": "number"}
        s2 = {"type": "array"}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_t_t_2(self):
        s1 = {"type": "number"}
        s2 = {"type": ["number"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_t_t_3(self):
        s1 = {"type": "integer"}
        s2 = {"type": ["number"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_t_t_4(self):
        s1 = {"type": "integer"}
        s2 = {"type": ["number", "string"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_t_t_5(self):
        s1 = {"type": ["string", "array"]}
        s2 = {"type": ["number", "string"]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_str_int(self):
        s1 = {"type": "string", "pattern": "a+",
              "allOf": [{"type": "string", "pattern": "b+"}, {"allOf": [{"type": "string", "maxLength": 10}]}]
              }
        s2 = {"type": "integer", "maxLength": 1}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_str_bool_any(self):
        s1 = {"type": ["string", "boolean"]}
        s2 = {"anyOf": [{"type": "string"}, {"type": "boolean"}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_allany_any(self):
        s1 = {"allOf": [{"type": ["string", "boolean"]}],
              "type": ["string", "boolean"]}
        s2 = {"anyOf": [{"type": "string"}, {"type": "boolean"}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_enum1(self):
        s1 = {"enum": [1, 2, "test", False]}
        s2 = {"type": ["integer", "string"], "minimum": 10, "enum": [1, 2]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_enum2(self):
        s1 = {"allOf": [{"enum": [1, 2, 3]}, {
            "type": "integer"}], "enum": [3, 4, 5]}
        s2 = {"type": "integer", "enum": [1, 2, 3]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_enum3(self):
        s1 = {"enum": [3, 4, 5]}
        s2 = {"enum": [1, 2, 3]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_enum4(self):
        s1 = {"enum": [3, 4, 5]}
        s2 = {"enum": [4, 5, 3]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_enum5(self):
        s1 = {"enum": [3, 4, 5], "allOf": [{"enum": [1, 2]}]}
        s2 = {"enum": [4, 5, 3]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_top_nottop(self):
        s1 = {}
        s2 = {"type": "string"}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_top_bot(self):
        s1 = {}
        s2 = {"type": "string", "enum": [1, 2, 3]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))