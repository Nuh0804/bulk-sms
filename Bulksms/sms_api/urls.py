from django.urls import path
from .views import CampaignViewSet, SmsDlr, ReceiveMessage, SendSms, AddRecipient
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("campaign", CampaignViewSet, basename="campaign")



urlpatterns = [
    path("receive/<str:sender>/<str:text>/", ReceiveMessage.as_view(), name="receive_sms"),
    path(
        'dlr/<str:receiver>/<str:sender>/<str:dlr_val>/<str:reply>/<str:message>',
        SmsDlr.as_view(),
        name='sms_dlr'
    ),
    path("send-sms/", SendSms.as_view(), name="send sms"),
    path("campaign/<int:pk>/recipients/", view= AddRecipient.as_view(), name="add recipient")
]

urlpatterns += router.urls