# -*- coding: utf-8 -*-
import unittest

from structs.arrays import BitArray, SortedList, CircularArray

__author__ = 'Jon Nappi'


class BitArrayTest(unittest.TestCase):
    def setUp(self):
        self.arr = BitArray([True, False, False])
        self.second = BitArray([False, True, True])

    def tearDown(self):
        self.arr = None
        self.second = None

    def test_init(self):
        self.assertEqual(str(self.arr), '100')

    def test_append(self):
        self.arr.append(True)
        self.assertEqual(str(self.arr), '1001')

    def test_extend(self):
        self.arr.extend(self.second)
        self.assertEqual(str(self.arr), '100011')

    def test_or(self):
        res = self.arr | self.second
        self.assertEqual(res, '0b111')

    def test_and(self):
        res = self.arr & self.second
        self.assertEqual(res, '0b0')

    def test_xor(self):
        res = self.arr ^ self.second
        self.assertEqual(res, '0b111')

    def test_invert(self):
        res = str(~self.arr)
        self.assertEqual(res, '011')
        res = -self.arr
        self.assertEqual(res, 3)

    def test_lshift(self):
        res = self.arr << 2
        self.assertEqual(str(res), '010')

    def test_rshift(self):
        res = self.arr >> 2
        self.assertEqual(str(res), '001')

    def test_int(self):
        self.assertEqual(int(self.arr), 4)

    def test_float(self):
        self.assertEqual(float(self.arr), 4.0)

    def test_complex(self):
        self.assertEqual(complex(self.arr), (4+0j))

    def test_octal(self):
        self.assertEqual(oct(self.arr), '0o4')

    def test_hex(self):
        self.assertEqual(hex(self.arr), '0x4')

    def test_bool(self):
        self.assertTrue(bool(self.arr))


class SortedListTest(unittest.TestCase):
    def setUp(self):
        self.list = SortedList(('c', 'b', 'a'))

    def tearDown(self):
        self.list = None

    def test_is_ordered(self):
        self.assertEqual(self.list, ['a', 'b', 'c'])

    def test_insert(self):
        self.list.insert('d')
        self.assertEqual(self.list, ['a', 'b', 'c', 'd'])

    def test_iadd(self):
        self.list += ['e', 'd', 'f']
        self.assertEqual(self.list, ['a', 'b', 'c', 'd', 'e', 'f'])


class CircularArrayTest(unittest.TestCase):
    def setUp(self):
        self.list = CircularArray([0, 1, 2])

    def tearDown(self):
        self.list = None

    def test_iteration(self):
        count = 0
        for item in self.list:
            if item == 2:
                count += 1
            if count == 2:
                break
        self.assertEqual(count, 2)
