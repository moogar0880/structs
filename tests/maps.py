# -*- coding: utf-8 -*-
import unittest

from structures.maps import Dict, BiDirectionalMap, MultiMap

__author__ = 'Jon Nappi'


class DictTest(unittest.TestCase):
    def setUp(self):
        self.dict = Dict(a=1, b=2)

    def tearDown(self):
        self.dict = None

    def test_iadd(self):
        self.dict += {'c': 3}
        self.assertEqual(self.dict, {'a': 1, 'b': 2, 'c': 3})


class BiDirectionalMapTest(unittest.TestCase):
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
        d = BiDirectionalMap(a=1, b=2)
        self.assertEqual(d.get('a'), 1)
        self.assertEqual(d.get('b'), 2)

    def test_assignment(self):
        d = BiDirectionalMap(a=1, b=2)
        self.assertEqual(d.get('a'), 1)
        d['a'] = 3
        self.assertEqual(d.get('a'), 3)
        d[3] = 'd'
        self.assertEqual(d.get(3), 'd')


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

    def test_update_kwargs(self):
        self.map.update(b=3, c=4)
        self.assertEqual(self.map, {'a': 1, 'b': [2, 3], 'c': 4})

    def test_setdefault(self):
        self.map.setdefault('d')
        self.assertIsNone(self.map.get('d'))
