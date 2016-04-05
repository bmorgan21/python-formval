import decimal

from . import validators as vv


UNDEF = ()


class BaseType(object):
    def __init__(self, validator=None, optional=False, empty=True, default=UNDEF, default_when_empty=False, is_list=False, is_dict=False, name=None):
        self.validator = validator
        self.optional = optional
        self.empty = empty
        self._default = default
        self.default_when_empty = default_when_empty
        self.is_list = is_list
        self.is_dict = is_dict
        self.name = name
        if self.default_when_empty and self._default == UNDEF:
            raise RuntimeError('No default specified when required')

    def _as_list(self, value):
        if not isinstance(value, (list, tuple)):
            value = [value]
        return value

    def python_to_string(self, value):
        if self.is_list:
            return [self.validator.from_python(x) for x in self._as_list(value)]
        else:
            return self.validator.from_python(value)

    def string_to_python(self, name, value):
        if self._is_empty(value):
            if not self.empty:
                raise vv.ValidationException('Please fill out this field.', field=name)

            return self.default

        try:
            if self.is_list:
                return [self.validator.to_python(x) for x in self._as_list(value)]
            else:
                return self.validator.to_python(value)
        except vv.ValidationException as exc:
            exc.field = name
            raise

    @property
    def default(self):
        if self._default == UNDEF:
            raise AttributeError('No default specified')
        return self._default

    def _is_empty(self, value):
        if self.is_list:
            return len([x for x in self._as_list(value) if not self.validator.is_empty(x)]) == 0
        else:
            return self.validator.is_empty(value)


class File(BaseType):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validator', vv.File())
        BaseType.__init__(self, *args, **kwargs)


class ImageFile(File):
    def __init__(self, max_size=None, *args, **kwargs):
        kwargs.setdefault('validator', vv.ImageFile(max_size=max_size))
        File.__init__(self, *args, **kwargs)


class Unicode(BaseType):
    def __init__(self, min_length=None, max_length=None, *args, **kwargs):
        kwargs.setdefault('default', '')
        kwargs.setdefault('validator', vv.Unicode(min_length=min_length, max_length=max_length))
        BaseType.__init__(self, *args, **kwargs)


class Integer(BaseType):
    def __init__(self, min=None, max=None, *args, **kwargs):
        kwargs.setdefault('validator', vv.Integer(min=min, max=max))
        BaseType.__init__(self, *args, **kwargs)


class Decimal(BaseType):
    def __init__(self, min=None, max=None, rounding=decimal.ROUND_HALF_EVEN, scale=2, *args, **kwargs):
        kwargs.setdefault('validator', vv.Decimal(min=min, max=max, rounding=rounding, scale=scale))
        BaseType.__init__(self, *args, **kwargs)


class Enum(BaseType):
    def __init__(self, choices, *args, **kwargs):
        kwargs.setdefault('validator', vv.Enum(choices))
        BaseType.__init__(self, *args, **kwargs)


class Type(BaseType):
    def __init__(self, choices, *args, **kwargs):
        kwargs.setdefault('validator', vv.Type(choices))
        BaseType.__init__(self, *args, **kwargs)


class Email(Unicode):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validator', vv.Email(max_length=256))
        Unicode.__init__(self, *args, **kwargs)


class Boolean(BaseType):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validator', vv.Boolean())
        BaseType.__init__(self, *args, **kwargs)
