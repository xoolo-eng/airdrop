from django.utils.translation import ugettext as _
# from django.shortcuts import redirect
from django.contrib import messages
from django.utils.safestring import mark_safe
from airdrop import libs


def login(request):
    data = {}
    if libs.is_signin(request):
        data["login"] = True
    return data


def check_alarm(request):
    data = {}
    if request.session.get("alarm"):
        messages.info(request, _("Maybe your cookies were stolen. Check your computer."))
        messages.info(
            request,
            mark_safe(
                _("For normal operation, clean the cookies on the site and go to the \
                    <a href=\"/\">main page</a> of the site."))
        )
    return data
