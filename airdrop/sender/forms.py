from django.contrib import messages
from django.utils.translation import ugettext as _
from django import forms
from sender import models as sm
from airdrop import libs
from django.conf import settings
import os
import re
import csv


ADDRESS = re.compile("([0-9a-fA-F]{40})")


class AirdropForm(forms.Form):
    contract = forms.CharField(
        label=_("Smart contract address"),
        widget=forms.TextInput(
            attrs={
                "id": "contract_address",
                "class": "form-control"
            }
        ),
        error_messages={
            "requered": _("'Contract address' field is required")
        }
    )
    amount = forms.CharField(
        label=_("Amount of tokens"),
        widget=forms.TextInput(
            attrs={
                "id": "amount_token",
                "class": "form-control"
            }
        ),
        error_messages={
            "required": _("'Amont' field is required")
        }
    )
    file = forms.FileField(
        label=_("Address file"),
        widget=forms.FileInput(
            attrs={
                "id": "sender_file",
                "class": "form-control-file"
            }
        ),
        error_messages={
            "requered": _("'Address file' field is required")
        }
    )

    def save(self, request):
        errors = []
        normal_addresses = []
        file_name = libs.rand(16)
        file = open("{0}/{1}".format(settings.TMP_ROOT, file_name), "wb")
        file.write(self.files["file"].read())
        file.close()
        with open("{0}/{1}".format(settings.TMP_ROOT, file_name), "r") as file:
            csv_file = csv.reader(file)
            for row in csv_file:
                try:
                    address = row[0]
                except IndexError:
                    continue
                else:
                    address = address.strip()[:-41:-1][::-1]
                    if re.match(ADDRESS, address):
                        if address not in normal_addresses:
                            normal_addresses.append(address)
                        else:
                            messages.info(request, _("Duplicate the value: ")+"{}".format(address))
                    else:
                        errors.append(", ".join(row))
        if normal_addresses:
            data = {
                "command": "cost",
                "count":
                [
                    len(normal_addresses),
                    settings.COUNT_ADDRESSES
                ],
                "call": settings.COST_CALL
            }
            order = sm.SenderOrder(
                user_id=libs.who_signin(request)[0],
                contract=self.data["contract"][:-41:-1][::-1],
                cost=str(libs.get_data(data, "cost")),
                amount=str(int(self.data["amount"])*len(normal_addresses))
            )
            order.save()
            data = {"command": "create", "order": order.id}
            order.address = libs.get_data(data, "address")
            order.save()
            for address in normal_addresses:
                recipient = sm.RecipientData(
                    order=order,
                    address=address,
                    amount=self.data["amount"]
                )
                recipient.save()
        if errors:
            for error in errors:
                messages.info(request, _("Error string: ")+error)
        os.remove("{0}/{1}".format(settings.TMP_ROOT, file_name))

    def clean(self):
        errors = False
        if not re.match(ADDRESS, self.cleaned_data.get("contract")[:-41:-1][::-1]):
            errors = True
            self.add_error("contract", _("Invalid smart address address format"))
        data = {"command": "contract", "contract": self.cleaned_data.get("contract")}
        if not libs.get_data(data, "contract"):
            errors = True
            self.add_error("contract", _("Not smart contract"))
        if int(self.cleaned_data.get("amount")) <= 0:
            errors = True
            self.add_error("amount", _("Only positive number is greater than zero"))
        if errors:
            raise forms.ValidationError(_("Data entry error"))
        else:
            return self.cleaned_data
