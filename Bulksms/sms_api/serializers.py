from rest_framework import serializers
from .models import *
class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSCampaign  # Assuming you have a Campaign model
        fields = ["id", "name",]  # Include fields you need

class RecipientSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer()  # Nested serializer

    class Meta:
        model = Recipient
        fields = ["id", "phone_number", "campaign"]  # Include fields you need
