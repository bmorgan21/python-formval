from werkzeug.datastructures import MultiDict

from . import conditions
from . import validators as vv


class FormValResult(object):
    def __init__(self, handled, strings, values=None, errors=None):
        self.handled = handled
        self.strings = strings
        self.values = values
        self.errors = errors
        self.errors_as_string = {k: str(v) for k, v in errors.items()} if errors else self.errors

    def success(self):
        return self.handled and not self.errors

    def error(self):
        return self.handled and self.errors


class FormValMeta(type):
    def __new__(cls, name, bases, dct):
        _fields = {}
        for k, v in dct.iteritems():
            if callable(getattr(v, 'string_to_python', None)) and callable(getattr(v, 'python_to_string', None)):
                _fields[k] = v

        dct.setdefault('_fields', {})
        for base in bases:
            if hasattr(base, '_fields'):
                dct['_fields'].update(base._fields)

        dct['_fields'].update(_fields)
        dct.setdefault('ALLOW_UNDEFINED', False)

        return type.__new__(cls, name, bases, dct)


def to_mixed(values, fields=None):
    result = {}
    if isinstance(values, MultiDict):
        for k in values.keys():
            if fields and k in fields:
                field = fields[k]
                if field.is_list:
                    result[k] = values.getlist(k)
                else:
                    result[k] = values.get(k)
            else:
                list_value = values.getlist(k)
                if len(list_value) > 1:
                    result[k] = list_value
                else:
                    result[k] = values.get(k)
    else:
        result = values

    return result


class FormVal(object):
    __metaclass__ = FormValMeta

    def __init__(self, success=None, failure=None):
        self.success = success
        self.failure = failure

    def process_python(self, values):
        """Turn raw python values back to strings"""
        values = self._to_strings(values)
        results = MultiDict()
        for k, v in values.iteritems():
            if k in self._fields:
                results.add(k, self._fields[k].python_to_string(v))

        return to_mixed(results)

    def process_strings(self, strings):
        """Turn input strings into python values"""
        result = self._process_strings(strings)
        result = self.to_python(result)

        if result.errors:
            if callable(self.failure):
                self.failure(result)
            return result
        if callable(self.success):
            self.success(result)
        return result

    def to_python(self, result):
        return self._to_python(result)

    def _to_python(self, result):
        return result

    def _to_strings(self, values):
        return values

    def _process_strings(self, values):
        errors = MultiDict()
        results = MultiDict()

        items = to_mixed(values).items()

        for k, v in items:
            if k in self._fields:
                try:
                    results.add(k, self._fields[k].string_to_python(k, v))
                except vv.ValidationException as e:
                    results.add(k, v)
                    errors.add(k, e)
            elif self.ALLOW_UNDEFINED:
                results.add(k, v)

        for k, v in self._fields.iteritems():
            if k not in values:
                if not v.optional:
                    errors.add(k, vv.ValidationException('Undefined Error', field=k))
                try:
                    results.add(k, v.default)
                except AttributeError:
                    pass

        return FormValResult(True, values, values=to_mixed(results), errors=to_mixed(errors))


class ConditionalVal(FormVal):
    def __init__(self, **kwargs):
        if not getattr(self, '__condition__', None):
            raise RuntimeError('Must specify __condition__ attribute')
        FormVal.__init__(self, **kwargs)

    def process_strings(self, values, force=False):
        if force or self.__condition__.should_process(values):
            return FormVal.process_strings(self, values)
        return FormValResult(False, values)


class KeyConditionalVal(ConditionalVal):
    def __init__(self, key='_', **kwargs):
        ConditionalVal.__init__(self, **kwargs)
        self.__condition__ = conditions.KeyCondition(key, self.__condition__)
