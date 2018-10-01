from django.conf import settings
from airdrop import libs
import os


def get_salt(name):
    file_name = "{0}/{1}".format(settings.SALT_PATH, name)
    with open(file_name, "r") as salt_file:
        return salt_file.read()


def generate_salt(name):
    file_name = "{0}/{1}".format(settings.SALT_PATH, name)
    salt = libs.rand(512)
    with open(file_name, "w") as salt_file:
        salt_file.write(salt)
    salt_file.close()
    return salt


def remove_salt(name):
    file_name = "{0}/{1}".format(settings.SALT_PATH, name)
    os.unlink(file_name)
