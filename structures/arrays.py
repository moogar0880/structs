# -*- coding: utf-8 -*-
from bisect import bisect
from collections import deque, Iterable

__author__ = 'Jon Nappi'
__all__ = ['prev', 'BaseList', 'BitArray', 'SortedList', 'CircularArray']


def prev(iterable):
    """Iterate in reverse over an iterable type supporting the __prev__ API"""
    if not hasattr(iterable, '__prev__'):
        msg = '{} does not support the prev interface'.format(type(iterable))
        raise TypeError(msg)
    return iterable.__prev__()


class BaseList(list):
    """Custom :const:`list` subclass with some additional iteration
    functionality
    """
    def __init__(self, *args, **kwargs):
        super(BaseList, self).__init__(*args, **kwargs)
        self._iter_index = 0

    def __iter__(self, *args, **kwargs):
        self._iter_index = 0
        return self

    def __prev__(self):
        """Add basic implementation of the prev API"""
        try:
            result = self[self._iter_index]
            self._iter_index -= 1
        except IndexError:
            raise StopIteration
        return result
    prev = __prev__

    def __next__(self):
        """Handle next iteration functionality"""
        try:
            result = self[self._iter_index]
            self._iter_index += 1
        except IndexError:
            raise StopIteration
        return result
    next = __next__


class BitArray(list):
    """A bit array (also known as bitmap, bitset, bit string, or bit vector) is
    an array data structure that compactly stores bits. It can be used to
    implement a simple set data structure. A bit array is effective at
    exploiting bit-level parallelism in hardware to perform operations quickly.
    """
    def __init__(self, iterable=()):
        """Create a new :class:`BitArray` instance"""
        # Force binary integer values
        super(BitArray, self).__init__([int(bool(item)) for item in iterable])

    def append(self, p_object):
        """Append the logical bitwise representation of *p_object*"""
        super(BitArray, self).append(int(bool(p_object)))

    def extend(self, iterable):
        """Append the logical bitwise representation of the objects in
        *iterable*
        """
        super(BitArray, self).extend([int(bool(item)) for item in iterable])

    def insert(self, index, p_object):
        """Append the logical bitwise representation of *p_object* to *index*
        """
        super(BitArray, self).insert(index, int(bool(p_object)))

    def __or__(self, other):
        """Perform a logical or on the bits in this :class:`BitArray`"""
        if not isinstance(other, BitArray):
            raise ValueError
        return bin(int(self) | int(other))

    def __and__(self, other):
        """Perform a logical and on the bits in this :class:`BitArray`"""
        if not isinstance(other, BitArray):
            raise ValueError
        return bin(int(self) & int(other))

    def __xor__(self, other):
        """Perform a logical xor on the bits in this :class:`BitArray`"""
        if not isinstance(other, BitArray):
            raise ValueError
        return bin(int(self) ^ int(other))

    def __invert__(self):
        """Return a new :class:`BitArray` instance with the opposite bit
        arrangement. Ie::
        >>> b = BitArray([True, False, False])
        >>> str(b)
        ... '100'
        >>> str(~b)
        ... '001'
        """
        return BitArray([0 if x == 1 else 1 for x in self])

    def __neg__(self):
        """Return the integer value of the :class:`BitArray` returned from a
        call to :meth:`BitArray.__invert__`
        """
        return int(self.__invert__())

    def __lshift__(self, other):
        """Perform an arithmetic left shift *other* bits to the left

        :returns: A new :class:`BitArray` with the shifted bits
        """
        if other < 0:
            other = -other
        dq = deque(self)
        dq.rotate(-other)
        return BitArray(dq)

    def __rshift__(self, other):
        """Perform an arithmetic right shift *other* bits to the right

        :returns: A new :class:`BitArray` with the shifted bits
        """
        if other < 0:
            other = -other
        dq = deque(self)
        dq.rotate(other)
        return BitArray(dq)

    def __int__(self):
        """Returns the integer representation of this :class:`BitArray`'s
        :const:`int` representation
        """
        return int(str(self), 2)

    def __float__(self):
        """Returns the float representation of this :class:`BitArray`'s
        :const:`int` representation
        """
        return float(int(self))

    def __complex__(self):
        """Returns the complex number representation of this
        :class:`BitArray`'s :const:`int` representation
        """
        return complex(int(self))

    def __oct__(self):
        """Returns the octal representation of this :class:`BitArray`'s
        :const:`int` representation
        """
        return oct(int(self))

    def __hex__(self):
        """Returns the hexadecimal representation of this :class:`BitArray`'s
        :const:`int` representation
        """
        return hex(int(self))

    def __bool__(self):
        """Returns the truthy-ness of this :class:`BitArray`'s :const:`int`
        representation
        """
        return bool(int(self))
    __nonzero__ = __bool__  # py2-3 compatability

    def __str__(self):
        """:const:`str` method. Returns a :const:`str` bitmap representation of
        this :class:`BitArray`
        """
        return ''.join(map(str, self))
    __repr__ = __str__

    def __iadd__(self, other):
        """Add bitwise representations of *other* to this :class:`BitArray`"""
        if isinstance(other, Iterable):
            self.extend(other)
        else:
            self.append(other)

    def __eq__(self, other):
        """Custom Equivalence operator"""
        if isinstance(other, BitArray):
            return int(self) == int(other)
        elif isinstance(other, int):
            return int(self) == other
        return False

    def __ne__(self, other):
        """Return the opposite of __eq__"""
        return not self.__eq__(other)

    def __hash__(self):
        """Return the integer representation of this :class:`BitArray`"""
        return int(self)


class SortedList(list):
    """A list implementation that always maintains a sorted order"""
    def __init__(self, iterable=(), key=None, reverse=False):
        """Create a new :class:`SortedList`. If *iterable* is specified, it
        will be sorted using *key* and added like a sequence passed to a normal
        :const:`list` constructor.

        :param iterable: An iterable to be sorted and inserted into this list
        :param key: *key* specifies a function of one argument that is used to
            extract a comparison key from each list element: ie, key=str.lower.
            The default value is None (compare the elements directly).
        :param reverse: A boolean value. If set to :const:`True`, then the
            :const:`list` elements are sorted as if each comparison were
            reversed.
        """
        super(SortedList, self).__init__(
            sorted(iterable, key=key or (lambda x: x), reverse=reverse)
        )
        self.key = key or (lambda x: x)
        self._reverse = reverse

    def append(self, p_object):
        """Add *p_object* into ordered place in the :const:`list`"""
        self.insert(p_object)

    def extend(self, iterable):
        """Append each item in *iterable* into it's sorted location in the
        :const:`list`
        """
        [self.insert(x) for x in iterable]

    def insert(self, p_object, *args):
        """Insert *p_object* at it's calculated index"""
        index = bisect(self, self.key(p_object))
        print(index)
        if self._reverse and index == 0:
            index = -1
        elif self._reverse:
            index *= -1
        super(SortedList, self).insert(index, p_object)

    def __iadd__(self, other):
        if not isinstance(other, list):
            raise TypeError
        self.extend(other)
        return self


class CircularArray(BaseList):
    """A :const:`list` subclass that will continually iterate until explicitly
    broken out of. ie, you're probably going to want a :const:`return` or
    :const:`break` in a loop over a :class:`CircularArray`
    """
    def __next__(self):
        """Keep looping forever, if we hit an IndexError, reset index to 0"""
        try:
            result = self[self._iter_index]
        except IndexError:
            if self._iter_index == 0:
                raise StopIteration  # Don't continually loop over empty lists
            self._iter_index = 0
            result = self[self._iter_index]
        self._iter_index += 1
        return result

    def __prev__(self):
        """Keep looping backwards forever, if we hit an IndexError, reset index
        to -1
        """
        try:
            result = self[self._iter_index]
        except IndexError:
            if self._iter_index == 0:
                raise StopIteration  # Don't continually loop over empty lists
            self._iter_index = -1
            result = self[self._iter_index]
        self._iter_index -= 1
        return result
