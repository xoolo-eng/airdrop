"""
    Авторизация пользователя, методы входа, выхода,
    проверки наличия входа, запрос логина пользователя
"""
from user import models


def signin(request, login):
    try:
        user = models.User.objects.get(login=login)
    except models.User.DoesNotExist:
        raise ValueError("libs.signin", "User not found.")
    request.session["user_id"] = user.label[::-1]
    request.session["check"] = "{}{}{}".format(
        request.META.get("HTTP_USER_AGENT"),
        request.META.get("DESKTOP_SESSION"),
        request.META.get("HTTP_X_REAL_IP")
    )


def signout(request):
    if request.session.get("user_id"):
        del request.session["user_id"]
    else:
        raise ValueError("libs.signout", "User not found.")


def is_signin(request, user_id=None):
    salt = None
    check = "{}{}{}".format(
        request.META.get("HTTP_USER_AGENT"),
        request.META.get("DESKTOP_SESSION"),
        request.META.get("HTTP_X_REAL_IP")
    )
    if request.session.get("user_id") and not request.session.get("alarm"):
        if check != request.session["check"]:
            request.session["alarm"] = True
            return False
        salt = request.session["user_id"][::-1]
    else:
        return False
    if user_id:
        try:
            user = models.User.objects.get(label=salt)
        except models.User.DoesNotExist:
            return False
        return user.id == user_id
    return True


def who_signin(request):
    salt = None
    if request.session.get("user_id"):
        salt = request.session["user_id"][::-1]
    else:
        raise ValueError("libs.who_signin", "User not found.")
    user = models.User.objects.get(label=salt)
    return user.id, user.login
