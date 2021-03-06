# -*- Mode: Python; py-indent-offset: 4 -*-
# pygobject - Python bindings for the GObject library
# Copyright (C) 2007 Johan Dahlin
#
#   gobject/propertyhelper.py: GObject property wrapper/helper
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301
# USA

import sys

from . import _gobject

from .constants import \
     TYPE_NONE, TYPE_INTERFACE, TYPE_CHAR, TYPE_UCHAR, \
     TYPE_BOOLEAN, TYPE_INT, TYPE_UINT, TYPE_LONG, \
     TYPE_ULONG, TYPE_INT64, TYPE_UINT64, TYPE_ENUM, TYPE_FLAGS, \
     TYPE_FLOAT, TYPE_DOUBLE, TYPE_STRING, \
     TYPE_POINTER, TYPE_BOXED, TYPE_PARAM, TYPE_OBJECT, \
     TYPE_PYOBJECT, TYPE_GTYPE, TYPE_STRV
from .constants import \
     G_MAXFLOAT, G_MAXDOUBLE, \
     G_MININT, G_MAXINT, G_MAXUINT, G_MINLONG, G_MAXLONG, \
     G_MAXULONG

if sys.version_info >= (3, 0):
    _basestring = str
    _long = int
else:
    _basestring = basestring
    _long = long


class Property(object):
    """
    Creates a new property which in conjunction with GObject subclass will
    create a property proxy:

    >>> class MyObject(GObject.GObject):
    >>> ... prop = GObject.Property(type=str)

    >>> obj = MyObject()
    >>> obj.prop = 'value'

    >>> obj.prop
    'value'

    The API is similar to the builtin property:

    class AnotherObject(GObject.GObject):
        @GObject.Property
        def prop(self):
            '''Read only property.'''
            return ...

        @GObject.Property(type=int)
        def propInt(self):
            '''Read-write integer property.'''
            return ...

        @propInt.setter
        def propInt(self, value):
            ...
    """

    class __metaclass__(type):
        def __repr__(self):
            return "<class 'GObject.Property'>"

    def __init__(self, getter=None, setter=None, type=None, default=None,
                 nick='', blurb='', flags=_gobject.PARAM_READWRITE,
                 minimum=None, maximum=None):
        """
        @param  getter: getter to get the value of the property
        @type   getter: callable
        @param  setter: setter to set the value of the property
        @type   setter: callable
        @param    type: type of property
        @type     type: type
        @param default: default value
        @param    nick: short description
        @type     nick: string
        @param   blurb: long description
        @type    blurb: string
        @param flags:    parameter flags, one of:
        - gobject.PARAM_READABLE
        - gobject.PARAM_READWRITE
        - gobject.PARAM_WRITABLE
        - gobject.PARAM_CONSTRUCT
        - gobject.PARAM_CONSTRUCT_ONLY
        - gobject.PARAM_LAX_VALIDATION
        @keyword minimum:  minimum allowed value (int, float, long only)
        @keyword maximum:  maximum allowed value (int, float, long only)
        """

        if type is None:
            type = object
        self.type = self._type_from_python(type)
        self.default = self._get_default(default)
        self._check_default()

        if not isinstance(nick, _basestring):
            raise TypeError("nick must be a string")
        self.nick = nick

        if not isinstance(blurb, _basestring):
            raise TypeError("blurb must be a string")
        self.blurb = blurb

        if flags < 0 or flags > 32:
            raise TypeError("invalid flag value: %r" % (flags,))
        self.flags = flags

        # Call after setting blurb for potential __doc__ usage.
        if getter and not setter:
            setter = self._readonly_setter
        elif setter and not getter:
            getter = self._writeonly_getter
        elif not setter and not getter:
            getter = self._default_getter
            setter = self._default_setter
        self.getter(getter)
        self.setter(setter)

        if minimum is not None:
            if minimum < self._get_minimum():
                raise TypeError(
                    "Minimum for type %s cannot be lower than %d" % (
                    self.type, self._get_minimum()))
        else:
            minimum = self._get_minimum()
        self.minimum = minimum
        if maximum is not None:
            if maximum > self._get_maximum():
                raise TypeError(
                    "Maximum for type %s cannot be higher than %d" % (
                    self.type, self._get_maximum()))
        else:
            maximum = self._get_maximum()
        self.maximum = maximum

        self.name = None

        self._exc = None

    def __repr__(self):
        return '<GObject Property %s (%s)>' % (
            self.name or '(uninitialized)',
            _gobject.type_name(self.type))

    def __get__(self, instance, klass):
        if instance is None:
            return self

        self._exc = None
        value = instance.get_property(self.name)
        if self._exc:
            exc = self._exc
            self._exc = None
            raise exc

        return value

    def __set__(self, instance, value):
        if instance is None:
            raise TypeError

        self._exc = None
        instance.set_property(self.name, value)
        if self._exc:
            exc = self._exc
            self._exc = None
            raise exc

    def __call__(self, fget):
        """Allows application of the getter along with init arguments."""
        return self.getter(fget)

    def getter(self, fget):
        """Set the getter function to fget. For use as a decorator."""
        if self.__doc__ is None:
            self.__doc__ = fget.__doc__
        if not self.blurb and fget.__doc__:
            self.blurb = fget.__doc__
        self.fget = fget
        return self

    def setter(self, fset):
        """Set the setter function to fset. For use as a decorator."""
        self.fset = fset
        return self

    def _type_from_python(self, type_):
        if type_ == _long:
            return TYPE_LONG
        elif type_ == int:
            return TYPE_INT
        elif type_ == bool:
            return TYPE_BOOLEAN
        elif type_ == float:
            return TYPE_DOUBLE
        elif type_ == str:
            return TYPE_STRING
        elif type_ == object:
            return TYPE_PYOBJECT
        elif (isinstance(type_, type) and
              issubclass(type_, (_gobject.GObject,
                                 _gobject.GEnum,
                                 _gobject.GFlags,
                                 _gobject.GBoxed))):
            return type_.__gtype__
        elif type_ in [TYPE_NONE, TYPE_INTERFACE, TYPE_CHAR, TYPE_UCHAR,
                       TYPE_INT, TYPE_UINT, TYPE_BOOLEAN, TYPE_LONG,
                       TYPE_ULONG, TYPE_INT64, TYPE_UINT64,
                       TYPE_FLOAT, TYPE_DOUBLE, TYPE_POINTER,
                       TYPE_BOXED, TYPE_PARAM, TYPE_OBJECT, TYPE_STRING,
                       TYPE_PYOBJECT, TYPE_GTYPE, TYPE_STRV]:
            return type_
        else:
            raise TypeError("Unsupported type: %r" % (type_,))

    def _get_default(self, default):
        ptype = self.type
        if default is not None:
            return default

        if ptype in [TYPE_INT, TYPE_UINT, TYPE_LONG, TYPE_ULONG,
                     TYPE_INT64, TYPE_UINT64]:
            return 0
        elif ptype == TYPE_STRING:
            return ''
        elif ptype == TYPE_FLOAT or ptype == TYPE_DOUBLE:
            return 0.0
        else:
            return None

    def _check_default(self):
        ptype = self.type
        default = self.default
        if (ptype == TYPE_BOOLEAN and (default not in (True, False))):
            raise TypeError(
                "default must be True or False, not %r" % (default,))
        elif ptype == TYPE_PYOBJECT:
            if default is not None:
                raise TypeError("object types does not have default values")
        elif ptype == TYPE_GTYPE:
            if default is not None:
                raise TypeError("GType types does not have default values")
        elif _gobject.type_is_a(ptype, TYPE_ENUM):
            if default is None:
                raise TypeError("enum properties needs a default value")
            elif not _gobject.type_is_a(default, ptype):
                raise TypeError("enum value %s must be an instance of %r" %
                                (default, ptype))
        elif _gobject.type_is_a(ptype, TYPE_FLAGS):
            if not _gobject.type_is_a(default, ptype):
                raise TypeError("flags value %s must be an instance of %r" %
                                (default, ptype))
        elif _gobject.type_is_a(ptype, TYPE_STRV) and default is not None:
            if not isinstance(default, list):
                raise TypeError("Strv value %s must be a list" % repr(default))
            for val in default:
                if type(val) not in (str, bytes):
                    raise TypeError("Strv value %s must contain only strings" % str(default))

    def _get_minimum(self):
        ptype = self.type
        if ptype in [TYPE_UINT, TYPE_ULONG, TYPE_UINT64]:
            return 0
        # Remember that G_MINFLOAT and G_MINDOUBLE are something different.
        elif ptype == TYPE_FLOAT:
            return -G_MAXFLOAT
        elif ptype == TYPE_DOUBLE:
            return -G_MAXDOUBLE
        elif ptype == TYPE_INT:
            return G_MININT
        elif ptype == TYPE_LONG:
            return G_MINLONG
        elif ptype == TYPE_INT64:
            return -2 ** 62 - 1

        return None

    def _get_maximum(self):
        ptype = self.type
        if ptype == TYPE_UINT:
            return G_MAXUINT
        elif ptype == TYPE_ULONG:
            return G_MAXULONG
        elif ptype == TYPE_INT64:
            return 2 ** 62 - 1
        elif ptype == TYPE_UINT64:
            return 2 ** 63 - 1
        elif ptype == TYPE_FLOAT:
            return G_MAXFLOAT
        elif ptype == TYPE_DOUBLE:
            return G_MAXDOUBLE
        elif ptype == TYPE_INT:
            return G_MAXINT
        elif ptype == TYPE_LONG:
            return G_MAXLONG

        return None

    #
    # Getter and Setter
    #

    def _default_setter(self, instance, value):
        setattr(instance, '_property_helper_' + self.name, value)

    def _default_getter(self, instance):
        return getattr(instance, '_property_helper_' + self.name, self.default)

    def _readonly_setter(self, instance, value):
        self._exc = TypeError("%s property of %s is read-only" % (
            self.name, type(instance).__name__))

    def _writeonly_getter(self, instance):
        self._exc = TypeError("%s property of %s is write-only" % (
            self.name, type(instance).__name__))

    #
    # Public API
    #

    def get_pspec_args(self):
        ptype = self.type
        if ptype in [TYPE_INT, TYPE_UINT, TYPE_LONG, TYPE_ULONG,
                     TYPE_INT64, TYPE_UINT64, TYPE_FLOAT, TYPE_DOUBLE]:
            args = self.minimum, self.maximum, self.default
        elif (ptype == TYPE_STRING or ptype == TYPE_BOOLEAN or
              ptype.is_a(TYPE_ENUM) or ptype.is_a(TYPE_FLAGS)):
            args = (self.default,)
        elif ptype in [TYPE_PYOBJECT, TYPE_GTYPE]:
            args = ()
        elif ptype.is_a(TYPE_OBJECT) or ptype.is_a(TYPE_BOXED):
            args = ()
        else:
            raise NotImplementedError(ptype)

        return (self.type, self.nick, self.blurb) + args + (self.flags,)
