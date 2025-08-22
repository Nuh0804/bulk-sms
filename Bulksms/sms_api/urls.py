from django.urls import path
from .views import ReceiveMessage, SmsDlr


urlpatterns = [
    path("receive/<str:sender>/<str:text>/", ReceiveMessage.as_view(), name="receive_sms"),
    path(
        'dlr/<str:msgid>/<str:dest>/<str:source>/<str:smsc>/<str:orig_msgid>/<str:status>/<str:timestamp>/',
        SmsDlr.as_view(),
        name='sms_dlr'
    ),
]