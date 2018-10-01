from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from airdrop import libs
from user import forms
from user import models
import multiprocessing as mp


def registration(request):
    if not libs.is_signin(request):
        data = {"title": _("Register new user")}
        if request.method == "POST":
            form_registration = forms.RegistrationUser(request.POST)
            if form_registration.is_valid():
                form_registration.save()
                messages.info(
                    request,
                    _("An email has been sent to the specified email address."),
                )
                messages.info(
                    request,
                    _("To complete the registration, click on the link in the email.")
                )
                return redirect("user_signin")
        else:
            form_registration = forms.RegistrationUser()
        data["form_registration"] = form_registration
        return render(
            request,
            "registration.html",
            data
        )
    else:
        return redirect("user_page")


def sign_in(request):
    if not libs.is_signin(request):
        data = {"title": _("Sign in"), "account": "active"}
        if request.method == "POST":
            form_signin = forms.SigninUser(request.POST)
            if form_signin.is_valid():
                fields = form_signin.cleaned_data
                libs.signin(request, fields.get("email"))
                return redirect("user_page")
        else:
            form_signin = forms.SigninUser()
        data["form_signin"] = form_signin
        return render(
            request,
            "signin.html",
            data
        )
    else:
        return redirect("user_page")


def sign_out(request):
    if libs.is_signin(request):
        libs.signout(request)
        return redirect("user_signin")
    else:
        return redirect("user_signin")


def user(request):
    if libs.is_signin(request):
        data = {"title": "User page", "account": "active"}
        user_id = libs.who_signin(request)[0]
        try:
            data["user"] = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            raise Http404()
        else:
            if libs.is_signin(request, user_id=data["user"].id):
                return render(request, "user_page.html", data)
            else:
                raise Http404()
    else:
        messages.info(request, _("You need to be logged in to view this page."))
        return redirect("user_signin")


def activate(request, key):
    user = models.User.objects.filter(label=key)
    if not user:
        messages(request, _("User not found!"))
        return redirect("home")
    else:
        if user[0].active:
            raise Http404
        user.update(active=True)
        return redirect("user_page")


def send_message(request, key):
    try:
        user = models.User.objects.get(label=key)
    except models.User.DoesNotExist:
        messages(request, _("User not found!"))
        return redirect("home")
    else:
        if user.active:
            raise Http404
        message = "http://http://airdrop.tt/user/activate/{}/".format(user.label)
        email = mp.Process(target=libs.send_email, args=[user.login, "Email activation", message])
        email.start()
        messages.info(
            request,
            _("An email has been sent to the specified email address."),
        )
        messages.info(
            request,
            _("To complete the registration, click on the link in the email.")
        )
        return redirect("user_signin")


# def change_email(request, key):
#     pass
