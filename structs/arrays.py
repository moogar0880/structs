# -*- coding: utf-8 -*-
"""An assorted collection of array and list data structures"""
import inspect

from bisect import bisect
from textwrap import dedent
from collections import deque, Iterable, Sized

__author__ = 'Jon Nappi'
__all__ = ['prev', 'BaseList', 'BitArray', 'SortedList', 'CircularArray',
           'ParallelArray', 'OrganizedList']


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

    def __next__(self):
        """Handle next iteration functionality"""
        try:
            result = self[self._iter_index]
            self._iter_index += 1
        except IndexError:
            raise StopIteration
        return result


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
            return self.__rshift__(-other)
        dq = deque(self)
        dq.rotate(-other)
        return BitArray(dq)

    def __rshift__(self, other):
        """Perform an arithmetic right shift *other* bits to the right

        :returns: A new :class:`BitArray` with the shifted bits
        """
        if other < 0:
            return self.__lshift__(-other)
        dq = deque(self)
        dq.rotate(other)
        return BitArray(dq)

    def __int__(self):
        """Returns the integer representation of this :class:`BitArray`'s
        :const:`int` representation
        """
        return int(str(self), 2)

    def __index__(self):
        """Returns the integer representation of this :class:`BitArray`"""
        return self.__int__()

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
        return self

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


class ParallelArray(Iterable, Sized):
    """A parallel array is a list-like data structure used for representing
    arrays of records. It keeps a separate array for each field of the record,
    each having the same number of elements. Thus, objects located at the same
    index in each array are implicitly linked together to form a single record
    """

    def __init__(self, *args, keys=()):
        """Create a new :class:`ParallelArray` instance

        :param args: Arbitrary key names
        :param keys: Explicitly declared key names. Can be mixed with args
        """
        self._keys = tuple(keys) + args
        for key in self._keys:
            setattr(self, key, [])
        self.__generate_append()

    def __generate_append(self):
        """Handle the dynamic generation of this ParallelArray instance's
        append method, which will be exec'd into the instances __dict__, thus
        allowing for a per-basis append signature to be used.
        """
        append = dedent(r"""
        def append(self, {args}):
            '''Add the specified arguments to the underlying parallel lists.
            Actual signature will vary depending on usage
            '''
            arg_list = [{args}]
            for key, arg in zip(self._keys, arg_list):
                getattr(self, key).append(arg)
                    """
        ).strip().format(args=', '.join(self._keys))
        exec(append, self.__dict__)

        # exec dumps a function into our dict which means it will expect `self`
        # to be passed as an explicit arg. Since functions are "technically"
        # descriptors, use the function's `__get__` method to bind it to our
        # instance
        self.append = self.append.__get__(self, self.__class__)

    def __iter__(self):
        """Return a tuple generator, which concurrently iterates over all of
        our internal lists
        """
        return zip(*[getattr(self, key) for key in self._keys])

    def __reversed__(self):
        """Generate a reversed tuple generator which will concurrently iterate
        over our internal lists backwards
        """
        return zip(*[getattr(self, key).__reversed__() for key in self._keys])

    def __getitem__(self, index):
        """Return the tuple of concurrent items stored at *index* across each
        of our lists

        :param index: The index into the array
        :return: A tuple of the items from each internal list at *index*
        """
        return tuple([getattr(self, key)[index] for key in self._keys])

    def __setitem__(self, key, value):
        """Overwrite the

        :param key: The index in the arrays to overrwrite
        :param value: The values to insert across each of our arrays. Must be
            provided as a :const:`tuple`
        :type: tuple
        """
        if not isinstance(value, tuple):
            raise TypeError
        for k, v in zip(self._keys, value):
            getattr(self, k).__setitem__(key, v)

    def __contains__(self, item):
        """Determine if *item* is contained in any of our internal arrays"""
        for tuple_data in self:
            if item in tuple_data:
                return True
        return False

    def append(self, *args, **kwargs):
        """Add the specified arguments to the underlying parallel lists. Actual
        signature will vary depending on usage
        """
        raise NotImplementedError

    def extend(self, iterable):
        """Extend this :class:`ParallelArray` with an *iterable* of
        :const:`tuple`s

        :param iterable: Any iterable of tuples (can be another
            :class:`ParallelArray`) that can be merged with this
            :class:`ParallelArray`
        """
        for args in iterable:
            self.append(*args)

    def insert(self, index, p_object):
        """Insert *p_object* at *index* across each of our internal arrays

        :param index: The index to insert into
        :param p_object: A :const:`tuple` to be insertted into this
            :class:`ParallelArray`
        :type: tuple
        """
        if not isinstance(p_object, tuple):
            raise TypeError

        for key, obj in zip(self._keys, p_object):
            getattr(self, key).insert(index, obj)

    def pop(self, index=-1):
        """Pop the provided *index* out of all underlying arrays, and return
        a :const:`tuple` of the values that were removed

        :param index: The index to pop from each internal array. Defaults to
            the last item
        :return: a :const:`tuple` of the values that were removed
        """
        return tuple([getattr(self, key).pop(index) for key in self._keys])

    def clear(self):
        """Clear all of our internal arrays"""
        for key in self._keys:
            getattr(self, key).clear()

    def copy(self):
        """Create a shallow copy of this :class:`ParallelArray`

        :return: A new :class:`ParallelArray` with all of the same data
        """
        new = ParallelArray(*self._keys)
        for key in self._keys:
            setattr(new, key, getattr(self, key).copy())
        return new

    def count(self, value):
        """Return a count of the number of times that *value* appears in our
        arrays

        :param value: The value to search for
        :return: The count of the number of times *value* appears in our arrays
        """
        return sum([getattr(self, key).count(value) for key in self._keys])

    def remove(self, value):
        """Remove the first entery in which *value* is found in our arrays

        :param value: The value to remove
        """
        to_delete = None
        for index, container in enumerate(self):
            if value in container:
                to_delete = index
                break
        if to_delete is not None:
            self.pop(to_delete)

    def reverse(self):
        """Reverse this :class:`ParallelArray` in place"""
        [getattr(self, key).reverse() for key in self._keys]

    def __len__(self):
        """Return the length of this :class:`ParallelArray`

        :return: The number of records contained in this :class:`ParallelArray`
        """
        return len(getattr(self, self._keys[0]))

    def __eq__(self, other):
        """Determine equivalence between this :class:`ParallelArray` and
        *other*

        :param other: Another :class:`ParallelArray` or iterable of iterables
        :return: :const:`True` if this :class:`ParallelArray` is equivalent to
            *other*, otherwise :const:`False`
        """
        for data, other_data in zip(self, other):
            if data != other_data:
                return False
        return True

    def __ne__(self, other):
        """Determine non-equivalence between this :class:`ParallelArray` and
        *other*

        :param other: Another :class:`ParallelArray` or iterable of iterables
        :return: :const:`False` if this :class:`ParallelArray` is equivalent to
            *other*, otherwise :const:`True`
        """
        return not self.__eq__(other)

    def __str__(self):
        """str representation of this :class:`ParallelArray`"""
        if len(self) == 0:
            return '[]'
        out = '['
        for item in self:
            out += '{}, '.format(item)
        return out[:-2] + ']'
    __repr__ = __str__

    def as_list(self):
        """Return this :class:`ParallelArray` as a :const:`list`"""
        return list(self)

    def as_tuple(self):
        """Return this :class:`ParallelArray` as a :const:`tuple`"""
        return tuple(self)

    def as_dict(self):
        """Return this :class:`ParallelArray` as a :const:`dict`"""
        return {k: getattr(self, k) for k in self._keys}


class OrganizedList(SortedList):
    """https://en.wikipedia.org/wiki/Self-organizing_list"""
    class Container:
        def __init__(self, data=None, count=0):
            self.data, self.count = data, count

        def __str__(self):
            return '{}:{}'.format(str(self.data), self.count)
        __repr__ = __str__

    def __init__(self, iterable=()):
        iterable = [self.Container(x) for x in iterable]
        super().__init__(iterable, (lambda x: x.count), reverse=True)

    def insert(self, p_object, *args):
        if not isinstance(p_object, self.Container):
            contained = self.Container(data=p_object, count=0)
        else:
            contained = p_object
        super().insert(contained)

    def __setitem__(self, key, value):
        contained = self.Container(data=value, count=0)
        super().__setitem__(key, contained)

    def __getitem__(self, item):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        contained = super().__getitem__(item)
        if calframe[1][3] != 'insert':
            contained.count += 1
        super().pop(self.index(contained))
        super().insert(contained)
        return contained.data

    def pop(self, index=None):
        contained = super(OrganizedList, self).pop(index)
        return contained.data
