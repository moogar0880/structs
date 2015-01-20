# -*- coding: utf-8 -*-

__author__ = 'Jon Nappi'
__all__ = ['Dict', 'BiDirectionalMap', 'MultiMap']


class Dict(dict):
    """Overriden :const:`dict` type with iadd functionality which will allow
    you to append two dictionaries together. ie::

    >>> d = Dict(a=1, b=2)
    >>> d += {'c': 3, 'd': 4}
    >>> d
    ... {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    """
    def __iadd__(self, other):
        if not isinstance(other, dict):
            msg = 'Can not concatenate Dict and {}'.format(type(other))
            raise TypeError(msg)
        for key, val in other.items():
            self[key] = val
        return self


class BiDirectionalMap(Dict):
    """a bidirectional map, or hash bag, is an associative data structure in
    which the (key, value) pairs form a one-to-one correspondence. Thus the
    binary relation is functional in each direction: value can also act as a
    key to key. A pair (a, b) thus provides a unique coupling between a and b
    so that b can be found when a is used as a key and a can be found when b is
    used as a key.
    """
    def __init__(self, iterable=None, **kwargs):
        """Create a new instance of a :class:`bidirectionaldict`

        :param iterable: An iterable of 2-tuples
        :param kwargs: Explitily specified key value pairs for this
            :class:`bidirectionaldict`
        """
        super(BiDirectionalMap, self).__init__()
        self.__keys = []
        self.__vals = []
        if iterable:
            self.__keys = [k for (k, v) in iterable]
            self.__vals = [v for (k, v) in iterable]
        for key, val in kwargs.items():
            self.__keys.append(key)
            self.__vals.append(val)

    def __contains__(self, item):
        """Contains method determines if *item* is in this
        :class:`bidirectionaldict`'s keys or values

        :param item: An arbitrary key or value to search for
        :return: :const:`True` if *item* is in this :class:`bidirectionaldict`,
            :const:`False` otherwise
        """
        return item in self.__keys or item in self.__vals

    def get(self, k, d=None):
        """Return self[k] if k is in this :class:`bidirectionaldict`, otherwise
        return *d*

        :param k: A key to return from this :class:`bidirectionaldict`
        :param d: The default value to return if *k* is not in this
            :class:`bidirectionaldict`
        :return: The value mapped to by *k* or *d* if *k* is not in this
            :class:`bidirectionaldict`
        """
        try:
            return self[k]
        except KeyError:
            return d

    def __setitem__(self, key, value):
        """Set self[key] to value."""
        try:
            index = self.__keys.index(key)
            self.__vals[index] = value
        except ValueError:
            try:
                index = self.__vals.index(key)
                self.__keys[index] = value
            except ValueError:
                self.__keys.append(key)
                self.__vals.append(value)

    def __getitem__(self, y):
        """x.__getitem__(y) <==> x[y]"""
        try:
            index = self.__keys.index(y)
            return self.__vals[index]
        except ValueError:
            try:
                index = self.__vals.index(y)
                return self.__keys[index]
            except ValueError:
                raise KeyError(y)

    def __str__(self):
        """Overriden str representation that iterates through all keys and
        values contained in this :class:`bidirectionaldict`
        """
        if len(self.__keys) == 0:
            return '{}'
        output = '{'
        fmt = '{}: {}, '
        for key, val in zip(self.__keys, self.__vals):
            output += fmt.format(str(key), str(val))
        return output[:-2] + '}'
    __repr__ = __str__

    def __len__(self):
        """__keys and __values will always be the same length, so return the
        length of __keys to be somewhat consistent with the default
        :const:`dict`'s __len__ method
        """
        return len(self.__keys)


class MultiMap(Dict):
    """A :class:`MultiMap` is a generalization of a :const:`dict` type in which
    more than one value may be associated with and returned for a given key
    """
    def update(self, other=None, **kwargs):
        """Update this :class:`MultiMap` with either the

        :param other: Another :const:`dict` to merge into this
            :class:`MultiMap` or an iterable of (key, value) 2-tuples
        :param kwargs: Arbitrary keyword args to merge into this
            :class:`MultiMap`
        """
        if other is not None and hasattr(other, 'keys'):
            for key in other:
                self[key] = other[key]
        elif other is not None and hasattr(other, '__iter__'):
            for key, val in other:
                self[key] = val
        for key, val in kwargs.items():
            self[key] = val

    def setdefault(self, k, d=None):
        """If *k* is not contained in this :class:`MultiMap` then store the
        value *d* in it.

        :param k: The key to set the value for
        :param d: The default value to assign to key *k*
        :return: The value stored at key *k*
        """
        if k not in self:
            self[k] = d
        return self[k]

    def _append_key(self, key, value):
        """Handle either adding the *key*, *value* pair to the :const:`dict` or
        appending *value* to the list stored at *key*
        """
        if isinstance(self[key], list):
            self[key].append(value)
        else:
            super(MultiMap, self).__setitem__(key, [self.get(key), value])

    def __iadd__(self, other):
        """Overriden __iadd__ functionality that will append values from
        *other* if any of the keys match

        :param other: Another :const:`dict` type to merge into this
            :class:`MultiMap`
        """
        if not isinstance(other, dict):
            msg = 'Can not concatenate Dict and {}'.format(type(other))
            raise TypeError(msg)
        for key, val in other.items():
            if key in self:
                self._append_key(key, val)
            else:
                self[key] = val

    def __setitem__(self, key, value):
        """If *key* is in this :class:`MultiMap` then

        :param key: The key to assign *value* to
        :param value: The *value* to assign to *key*
        """
        if key in self:
            self._append_key(key, value)
        else:
            super(MultiMap, self).__setitem__(key, value)
