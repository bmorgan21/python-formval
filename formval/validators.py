from PIL import Image
from werkzeug import FileStorage

from validation import *


class File(Validator):
    def is_empty(self, value):
        if isinstance(value, FileStorage):
            empty = value.content_length == 0
        else:
            empty = (value.file.read(1) == '')
            value.file.seek(0)
            return empty

    def _to_python(self, value):
        if not isinstance(value, FileStorage):
            if not hasattr(value, 'file') or not hasattr(value, 'name') or not hasattr(value, 'type'):
                raise RuntimeError('Submitted data is not a cgi.FieldStorage or werkzeug.FileStorage')

            inp = value.file
            if not hasattr(inp, 'read') or \
                    not hasattr(inp, 'readline') or \
                    not hasattr(inp, 'readlines') or \
                    not hasattr(inp, 'seek'):
                raise ValidationException('Submitted data is not a file')

        return Validator._to_python(self, value)


class ImageFile(File):
    def _to_python(self, value):
        value = File._to_python(self, value)

        if isinstance(value, FileStorage):
            file = value
        else:
            file = value.file

        try:
            im = Image.open(file)
            im.verify()
        except BaseException as e:
            raise ValidationException(getattr(e, 'message', 'Unknown image error'))

        file.seek(0)
        return Image.open(file)
