from rest_framework import serializers
from .models import *
class CampaignSerializer(serializers.ModelSerializer):
    recepient_no = serializers.SerializerMethodField()
    class Meta:
        model = SMSCampaign  # Assuming you have a Campaign model
        fields = ["id", "name", "message_template", "recepient_no"]  # Include fields you need

    def get_recepient_no(self, obj):
        return Recipient.objects.filter(campaign = obj).count()
        

class RecipientSerializer(serializers.ModelSerializer):
    campaign = CampaignSerializer()  # Nested serializer

    class Meta:
        model = Recipient
        fields = ["id", "phone_number", "params","campaign"]  # Include fields you need


class RecipientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ["phone_number", "params"]