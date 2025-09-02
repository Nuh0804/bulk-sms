from django.urls import path
from .views import ReceiveMessage, SmsDlr, SendSms


urlpatterns = [
    path("receive/<str:sender>/<str:text>/", ReceiveMessage.as_view(), name="receive_sms"),
    path(
        'dlr/<str:sender>/<str:receiver>/<str:msg>/<str:dlr_val>/<str:dlr_msg>/<str:reply>/<str:timestamp>/',
        SmsDlr.as_view(),
        name='sms_dlr'
    ),
    path("send-sms/", SendSms.as_view(), name="send sms")
]