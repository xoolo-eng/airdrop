from django.db import models
from django.utils.translation import ugettext as _
from user import models as um
from datetime import datetime


class SenderOrder(models.Model):
    # STATUS = [(0, _("created")),(1, _("in the work")),(2, _("finished")),]

    user = models.ForeignKey(
        um.User,
        on_delete=models.CASCADE,
        related_name="order_user",
        verbose_name=_("User")
    )
    date_additions = models.DateTimeField(
        default=datetime.now(),
        verbose_name=_("Date additions")
    )
    address = models.CharField(
        max_length=40,
        null=True,
        unique=True,
        verbose_name=_("Address wallet for order")
    )
    contract = models.CharField(
        max_length=40,
        verbose_name=_("Smart contract address")
    )
    work_contract = models.CharField(
        max_length=40,
        null=True,
        verbose_name=_("Address work contract")
    )
    payment = models.BooleanField(
        default=False,
        verbose_name=_("Payment for services")
    )
    tokens = models.BooleanField(
        default=False,
        verbose_name=_("Ready for launch")
    )
    status = models.SmallIntegerField(
        default=-1,
        # choices=STATUS,
        verbose_name=_("Status order")
    )
    cost = models.CharField(
        max_length=64,
        verbose_name=_("Service cost")
    )
    amount = models.CharField(
        max_length=64,
        verbose_name=_("Count all tokens")
    )

    class Meta:
        db_table = "sender_order"

    def __str__(self):
        return "Date create: {}, address: {}".format(self.date_additions, self.address)


class RecipientData(models.Model):
    order = models.ForeignKey(
        SenderOrder,
        on_delete=models.CASCADE,
        related_name="recipient_odrer",
        verbose_name=_("Order")
    )
    address = models.CharField(
        max_length=40,
        verbose_name=_("Address to")
    )
    amount = models.ImageField(
        verbose_name=_("Amount of tokens"),
    )
    status = models.BooleanField(
        default=False,
        verbose_name=_("Status")
    )

    class Meta:
        db_table = "sender_data"
        verbose_name = _("Sender data")

    def __str__(self):
        return "address: {0}, amount: {1} ".format(
            self.address,
            self.amount
        )
