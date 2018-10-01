from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django import forms
from airdrop import libs
from user import models
import re


EMAIL = re.compile('([\w]+)((.?|-?|_?)[\w]+)?@([\w-]{2,15}\.)+([\w]{2,6})')
PASSWORD = re.compile('((?=.*[\d])(?=.*[a-zA-Z])[a-zA-Z0-9*/<>_-]{8,100})')


class RegistrationUser(forms.Form):
    email = forms.EmailField(
        max_length=100,
        label=_("Your email"),
        widget=forms.EmailInput(
            attrs={
                "id": "user_email",
                "class": "form-control"
            }
        ),
        error_messages={
            "required": _("'Email' field is required")
        }
    )
    password = forms.CharField(
        max_length=100,
        label=_("Your password"),
        widget=forms.PasswordInput(
            attrs={
                "id": "user_password",
                "class": "form-control"
            }
        ),
        error_messages={
            "required": _("'Password' field is required")
        }
    )
    password_repeat = forms.CharField(
        max_length=100,
        label=_("Your password"),
        widget=forms.PasswordInput(
            attrs={
                "id": "user_password_repeat",
                "class": "form-control"
            }
        ),
        error_messages={
            "required": _("'Password' field is required")
        }
    )
    agreement = forms.BooleanField(
        label=mark_safe(
            _(
                "{0} <a href=\"/license/\">{1}</a>".format(
                    _("I agree with the"),
                    _("rules")
                )
            )
        ),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "id": "agreement_rules",
                "class": "form-check-input"
            }
        )
    )

    def save(self):
        new_user = models.User(
            login=self.data["email"],
            password=self.data["password"]
        )
        new_user.save()

    def clean(self):
        try:
            models.User.objects.get(
                login=self.cleaned_data.get("email")
            )
        except models.User.DoesNotExist:
            pass
        else:
            self.add_error("email", _("This email is already registered!"))
            raise forms.ValidationError(_("Data entry error"))
        errors = False
        if not re.match(EMAIL, self.cleaned_data.get("email")):
            errors = True
            self.add_error("email", _("Invalid characters entered!"))
        if not re.match(PASSWORD, self.cleaned_data.get("password")):
            errors = True
            self.add_error("password", _("Enter a more complex password!"))

        if self.cleaned_data.get("password_repeat") != self.cleaned_data.get("password"):
            errors = True
            self.add_error("password_repeat", _("The passwords you entered do not match!"))
        if not self.cleaned_data.get("agreement"):
            errors = True
            self.add_error("agreement", _("For registration, agree with the rules!"))

        if errors:
            raise forms.ValidationError(_("Data entry error"))

        return self.cleaned_data


class SigninUser(forms.Form):
    email = forms.EmailField(
        max_length=100,
        label=_("Your email"),
        widget=forms.EmailInput(
            attrs={
                "id": "user_email",
                "class": "form-control"
            }
        ),
        error_messages={
            "required": _("'Email' field is required")
        }
    )
    password = forms.CharField(
        max_length=100,
        label=_("Your password"),
        widget=forms.PasswordInput(
            attrs={
                "id": "user_password",
                "class": "form-control"
            }
        ),
        error_messages={
            "required": _("'Password' field is required")
        }
    )
    # saved = forms.BooleanField(
    #     label=_("Save"),
    #     required=False,
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             "id": "user_saved",
    #             "class": "form-check-input"
    #         }
    #     )
    # )

    def clean(self):
        try:
            user = models.User.objects.get(login=self.cleaned_data.get("email"))
        except models.User.DoesNotExist:
            self.add_error("email", _("The user with this email was not found!"))
            raise forms.ValidationError(_("Data entry error"))
        if not user.active:
            self.add_error(
                None,
                mark_safe(
                    "<a href=\"/user/send_message/{0}/\">{1}</a>".format(
                        user.label,
                        _("Send a second letter")
                    )
                )
            )
            # self.add_error(
            #     None,
            #     mark_safe(
            #         "<a href=\"/user/change_email/{0}/\">{1}</a>".format(
            #             user.label,
            #             _("Change email")
            #         )
            #     )
            # )
            self.add_error("email", _("Your account has not been activated"))
            raise forms.ValidationError(_("Data entry error"))
        salt = libs.get_salt(user.label)
        hash_password = libs.get_hash(self.cleaned_data.get("password"), salt)
        if hash_password != user.password:
            self.add_error("password", _("You entered the wrong password!"))
        self.cleaned_data["id"] = user.id
        return self.cleaned_data
