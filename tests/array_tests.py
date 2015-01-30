# -*- coding: utf-8 -*-
import unittest

from structs.arrays import (prev, BaseList, BitArray, SortedList,
                            CircularArray, ParallelArray)

__author__ = 'Jon Nappi'


class TestBaseList(unittest.TestCase):
    """Basic tests for structs.arrays.BaseList"""

    def setUp(self):
        self.list = BaseList([0, 1])

    def tearDown(self):
        self.list = None

    def test_prev(self):
        """Verify prev function behavior"""
        with self.assertRaises(TypeError):
            prev([])
        p = prev(self.list)
        self.assertEqual(p, 0)

    def test_next(self):
        """Verify next function behavior over BaseList"""
        n = next(self.list)
        self.assertEqual(n, 0)

    def test_stop_iter(self):
        """Verify that StopIteration is raised when expected"""
        with self.assertRaises(StopIteration):
            prev(BaseList())
        with self.assertRaises(StopIteration):
            next(BaseList())


class BitArrayTest(unittest.TestCase):
    """Unit level structs.arrays.BitArray tests"""

    def setUp(self):
        self.arr = BitArray([True, False, False])
        self.second = BitArray([False, True, True])

    def tearDown(self):
        self.arr = None
        self.second = None

    def test_init(self):
        """Verify that our BitArray was accurately created"""
        self.assertEqual(str(self.arr), '100')

    def test_append(self):
        """Verify that we appropriately cast data when appending"""
        self.arr.append(True)
        self.assertEqual(str(self.arr), '1001')

    def test_extend(self):
        """Verify that we appropriately cast data when extending"""
        self.arr.extend(self.second)
        self.assertEqual(str(self.arr), '100011')

    def test_insert(self):
        self.arr.insert(0, True)
        self.arr.insert(-1, False)
        self.assertEqual(str(self.arr), '11000')

    def test_or(self):
        with self.assertRaises(ValueError):
            self.arr | 12
        res = self.arr | self.second
        self.assertEqual(res, '0b111')

    def test_and(self):
        with self.assertRaises(ValueError):
            self.arr & 12
        res = self.arr & self.second
        self.assertEqual(res, '0b0')

    def test_xor(self):
        with self.assertRaises(ValueError):
            self.arr ^ 12
        res = self.arr ^ self.second
        self.assertEqual(res, '0b111')

    def test_negative(self):
        self.assertEqual(-self.arr, 3)

    def test_invert(self):
        res = str(~self.arr)
        self.assertEqual(res, '011')
        res = -self.arr
        self.assertEqual(res, 3)

    def test_lshift(self):
        res = self.arr << 2
        self.assertEqual(str(res), '010')
        res = self.arr << -2
        self.assertEqual(str(res), '001')

    def test_rshift(self):
        res = self.arr >> 2
        self.assertEqual(str(res), '001')
        res = self.arr >> -2
        self.assertEqual(str(res), '010')

    def test_int(self):
        self.assertEqual(int(self.arr), 4)

    def test_float(self):
        self.assertEqual(float(self.arr), 4.0)

    def test_complex(self):
        self.assertEqual(complex(self.arr), (4+0j))

    def test_octal(self):
        self.assertEqual(self.arr.__oct__(), '0o4')
        self.assertEqual(oct(self.arr), '0o4')

    def test_hex(self):
        self.assertEqual(self.arr.__hex__(), '0x4')
        self.assertEqual(hex(self.arr), '0x4')

    def test_bool(self):
        self.assertTrue(bool(self.arr))
        self.assertTrue(self.arr.__nonzero__())

    def test_str(self):
        self.assertEqual(str(self.arr), '100')
        self.assertEqual(repr(self.arr), '100')

    def test_iadd(self):
        self.arr += self.second
        self.assertEqual(str(self.arr), '100011')
        self.arr += False
        self.assertEqual(str(self.arr), '1000110')

    def test_eq(self):
        self.assertTrue(self.arr == self.arr)
        self.assertTrue(self.arr == 4)
        self.assertFalse(self.arr == 4.0)

    def test_neq(self):
        self.assertFalse(self.arr != self.arr)
        self.assertFalse(self.arr != 4)

    def test_hash(self):
        self.assertEqual(hash(self.arr), 4)


class SortedListTest(unittest.TestCase):
    def setUp(self):
        self.list = SortedList(('c', 'b', 'a'))
        self.revd = SortedList(('c', 'a', 'b'), reverse=True)

    def tearDown(self):
        self.list = None

    def test_is_ordered(self):
        self.assertEqual(self.list, ['a', 'b', 'c'])

    def test_insert(self):
        self.list.insert('d')
        self.assertEqual(self.list, ['a', 'b', 'c', 'd'])

    def test_insert_reversed(self):
        self.revd.insert('d')
        self.assertEqual(self.revd, ['d', 'c', 'b', 'a'])

    def test_iadd(self):
        with self.assertRaises(TypeError):
            self.list += 12
        self.list += ['e', 'd', 'f']
        self.assertEqual(self.list, ['a', 'b', 'c', 'd', 'e', 'f'])

    def test_append(self):
        self.list.append('aa')
        self.assertEqual(self.list, ['a', 'aa', 'b', 'c'])


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

    def test_next(self):
        n = next(self.list)
        self.assertEqual(n, 0)
        with self.assertRaises(StopIteration):
            next(CircularArray())

    def test_prev(self):
        p = prev(self.list)
        self.assertEqual(p, 0)
        with self.assertRaises(StopIteration):
            prev(CircularArray())

    def test_prev_cont(self):
        count = 0
        while True:
            p = prev(self.list)
            if p == 2:
                count += 1
            if count == 2:
                break
        self.assertEqual(count, 2)

    def test_next_cont(self):
        count = 0
        while True:
            p = next(self.list)
            if p == 2:
                count += 1
            if count == 2:
                break
        self.assertEqual(count, 2)


class ParallelArrayTest(unittest.TestCase):
    def setUp(self):
        self.list = ParallelArray('names', 'ages')
        self.list.append('John Smith', 25)
        self.list.append('James Bond', 50)

        self.second = ParallelArray('names', 'ages')
        self.second.append('Jane Smith', 23)

    def tearDown(self):
        self.list = None

    def test_iter(self):
        for name, age in self.list:
            self.assertIsInstance(name, str)
            self.assertIsInstance(age, int)

    def test_reversed(self):
        for name, age in reversed(self.list):
            self.assertIsInstance(name, str)
            self.assertIsInstance(age, int)

    def test_items(self):
        expected = ('John Smith', 25)
        self.assertEqual(self.list[0], expected)

        new = ('Jane Smith', 23)
        self.list[0] = new
        self.assertEqual(self.list[0], new)

        with self.assertRaises(TypeError):
            self.list[0] = 12

    def test_contains(self):
        self.assertTrue(self.list.__contains__('James Bond'))
        self.assertFalse(self.list.__contains__('Jane Bond'))

    def test_append(self):
        new = ('Jane Smith', 23)
        self.list.append('Jane Smith', 23)
        self.assertEqual(self.list[-1], new)

    def test_extend(self):
        self.list.extend(self.second)
        self.assertEqual(len(self.list), 3)

    def test_insert(self):
        with self.assertRaises(TypeError):
            self.list.insert((0, 15))

        self.list.insert(0, ('Jane Smith', 23))

    def test_pop(self):
        res = self.list.pop()
        self.assertEqual(res, ('James Bond', 50))

        res = self.list.pop(0)
        self.assertEqual(res, ('John Smith', 25))

    def test_clear(self):
        self.list.clear()
        self.assertEqual(len(self.list), 0)

    def test_copy(self):
        copied = self.list.copy()
        self.assertEqual(copied, self.list)

    def test_count(self):
        count = self.list.count('James Bond')
        self.assertEqual(count, 1)

    def test_remove(self):
        self.list.remove('James Bond')
        self.assertEqual(len(self.list), 1)
        self.assertNotIn('James Bond', self.list)

    def test_reverse(self):
        self.list.reverse()
        expected = [
            ('James Bond', 50),
            ('John Smith', 25)
        ]
        self.assertEqual(self.list, expected)

    def test_len(self):
        self.assertEqual(len(self.list), len(self.list.names))

    def test_eq(self):
        expected = [
            ('John Smith', 25),
            ('James Bond', 50)
        ]
        self.assertEqual(self.list, expected)

        self.list.reverse()
        self.assertNotEqual(self.list, expected)

    def test_str(self):
        expected = "[('John Smith', 25), ('James Bond', 50)]"
        self.assertEqual(str(self.list), expected)
        self.assertEqual(repr(self.list), expected)

        empty = ParallelArray('names')
        self.assertEqual(str(empty), '[]')
        self.assertEqual(repr(self.list), expected)

    def test_converters(self):
        expected_list = [
            ('John Smith', 25),
            ('James Bond', 50)
        ]
        expected_tuple = tuple(expected_list)
        expected_dict = {'names': ['John Smith', 'James Bond'],
                         'ages': [25, 50]}
        self.assertEqual(self.list.as_list(), expected_list)
        self.assertEqual(self.list.as_tuple(), expected_tuple)
        self.assertEqual(self.list.as_dict(), expected_dict)

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            ParallelArray.append(self.list)
