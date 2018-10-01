import hashlib
from django.conf import settings


def get_hash(data, salt=""):
    bytes_string = "{0}{1}".format(
        str(salt).join(list(data)),
        settings.GLOBAL_SALT
    ).encode("utf-8")
    result = hashlib.sha512()
    result.update(bytes_string)
    return str(result.hexdigest())
