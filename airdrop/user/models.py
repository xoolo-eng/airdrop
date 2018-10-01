from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime
from airdrop import libs
import sys
import multiprocessing as mp
from django.conf import settings


class User(models.Model):
    login = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Login name user (email)")
    )
    password = models.TextField(
        verbose_name=_("Password hash")
    )
    date_registration = models.DateTimeField(
        default=datetime.now(),
        verbose_name=_("User registration date")
    )
    active = models.BooleanField(
        default=False,
        verbose_name=_("Activated account")
    )
    label = models.CharField(
        max_length=64,
        verbose_name=_("Name salt file")
    )

    class Meta:
        db_table = "user"
        verbose_name = _("User")

    def __str__(self):
        return "login - {0}, date of registration: {1}".format(
            self.login,
            self.date_registration
        )

    def save(self):
        self.label = libs.rand(32)
        salt = libs.generate_salt(self.label)
        self.password = libs.get_hash(self.password, salt=salt)
        super(User, self).save()
        settings.LOG.info("Create user: {}".format(self))
        head = "Email activation"
        message = """
            http://airdrop.tt/user/activate/{}/
        """.format(self.label)
        email = mp.Process(target=libs.send_email, args=[self.login, head, message])
        email.start()

    def delete(self):
        libs.remove_salt(self.label)
        super(User, self).delete()
        settings.LOG.info("Delete user: {}".format(self))
