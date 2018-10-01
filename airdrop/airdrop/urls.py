from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from user import views as uv
from home import views as hv
from sender import views as sv
from rest import views as rv


# home urls
urlpatterns = i18n_patterns(
    path("", hv.home, name="home")
)

# user urls
urlpatterns += i18n_patterns(
    path("user/registration/", uv.registration, name="user_registration"),
    path("user/signin/", uv.sign_in, name="user_signin"),
    path("user/signout/", uv.sign_out, name="user_signout"),
    path("user/activate/<str:key>/", uv.activate, name="user_activate"),
    path("user/send_message/<str:key>/", uv.send_message, name="send_message"),
    path("user/", uv.user, name="user_page"),
)

# sender urls
urlpatterns += i18n_patterns(
    path("sender/load/", sv.load, name="load_data"),
    path("sender/orders/<int:num>/", sv.orders, name="view_orders"),
    path("sender/order/<str:address>/", sv.order, name="view_order"),
    path("sender/order/<str:address>/start/", sv.start, name="start_order"),
    path("sender/order/<str:address>/repeat/", sv.repeat, name="repeat_order"),
    path("sender/orders/download/<str:order_address>.csv", sv.download, name="download_order"),
)

# rest urls
urlpatterns += [
    path("rest/check_payment/", rv.chech_pyment, name="rest_check_payment"),
    path("rest/check_token/", rv.check_token, name="rest_check_token"),
]
