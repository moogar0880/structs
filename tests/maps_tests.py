# -*- coding: utf-8 -*-
import unittest

from structs.maps import Dict, BiDirectionalMap, MultiMap

__author__ = 'Jon Nappi'


class DictTest(unittest.TestCase):
    def setUp(self):
        self.dict = Dict(a=1, b=2)

    def tearDown(self):
        self.dict = None

    def test_iadd(self):
        self.dict += {'c': 3}
        self.assertEqual(self.dict, {'a': 1, 'b': 2, 'c': 3})

        with self.assertRaises(TypeError):
            self.dict += 12


class BiDirectionalMapTest(unittest.TestCase):
    def setUp(self):
        self.dict = BiDirectionalMap(a=1, b=2)

    def tearDown(self):
        self.dict = None

    def test_empty_init(self):
        d = BiDirectionalMap()
        d['a'] = 1
        self.assertIn('a', d)
        self.assertIn(1, d)

    def test_seq_init(self):
        d = BiDirectionalMap([('a', 1), ('b', 2)])
        self.assertIn('a', d)
        self.assertIn(1, d)
        self.assertIn('b', d)
        self.assertIn(2, d)

    def test_kwargs_init(self):
        d = BiDirectionalMap(a=1, b=2)
        self.assertIn('a', d)
        self.assertIn(1, d)
        self.assertIn('b', d)
        self.assertIn(2, d)

    def test_mixed_init(self):
        d = BiDirectionalMap([('a', 1)], b=2)
        self.assertIn('a', d)
        self.assertIn(1, d)
        self.assertIn('b', d)
        self.assertIn(2, d)

    def test_get(self):
        self.assertEqual(self.dict.get('a'), 1)
        self.assertEqual(self.dict.get('b'), 2)
        self.assertEqual(self.dict.get('c', d=3), 3)

    def test_assignment(self):
        self.assertEqual(self.dict.get('a'), 1)
        self.dict['a'] = 3
        self.assertEqual(self.dict.get('a'), 3)
        self.dict[3] = 'd'
        self.assertEqual(self.dict.get(3), 'd')

    def test_set_item(self):
        self.dict['a'] = 5
        self.dict[5] = 'A'
        self.assertEqual(self.dict['A'], 5)
        self.assertEqual(self.dict[5], 'A')

        self.dict['d'] = 20
        self.assertEqual(self.dict.get(20), 'd')

    def test_get_item(self):
        with self.assertRaises(KeyError):
            v = self.dict['c']

        self.assertEqual(self.dict.get(2), 'b')

    def test_str(self):
        empty = BiDirectionalMap()
        self.assertEqual(str(empty), '{}')
        self.assertEqual(repr(empty), '{}')

        for expected in ["'a': 1", "'b': 2"]:
            self.assertIn(expected, str(self.dict))
            self.assertIn(expected, repr(self.dict))

    def test_len(self):
        self.assertEqual(len(self.dict), 2)

    def test_gens(self):
        res = list(self.dict.keys())
        for key in ['a', 'b']:
            self.assertIn(key, res)

        res = list(self.dict.values())
        for val in [1, 2]:
            self.assertIn(val, res)

        res = list(self.dict.items())
        expected = [
            ('a', 1),
            ('b', 2)
        ]
        for tup in expected:
            self.assertIn(tup, res)


class MultiMapTest(unittest.TestCase):
    def setUp(self):
        self.map = MultiMap(a=1, b=2)

    def tearDown(self):
        self.map = None

    def test_overwrite(self):
        self.assertEqual(self.map.get('a'), 1)
        self.map['a'] = 3
        self.assertEqual(self.map.get('a'), [1, 3])

    def test_update_other(self):
        self.map.update({'b': 3, 'c': 4})
        self.assertEqual(self.map, {'a': 1, 'b': [2, 3], 'c': 4})

        self.map.update([('d', 5)])
        self.assertEqual(self.map, {'a': 1, 'b': [2, 3], 'c': 4, 'd': 5})

    def test_update_kwargs(self):
        self.map.update(b=3, c=4)
        self.assertEqual(self.map, {'a': 1, 'b': [2, 3], 'c': 4})

    def test_setdefault(self):
        self.map.setdefault('d')
        self.assertIsNone(self.map.get('d'))

    def test_append_key(self):
        self.map._append_key('a', 3)
        self.map._append_key('a', 4)
        self.assertEqual(self.map.get('a'), [1, 3, 4])

    def test_iadd(self):
        with self.assertRaises(TypeError):
            self.map += 12
        map2 = MultiMap(b=12, c=3, d=4)
        self.map += map2

        expected = dict(a=1, b=[2, 12], c=3, d=4)
        self.assertEqual(self.map, expected)
