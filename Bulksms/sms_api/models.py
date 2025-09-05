from django.db import models
from uuid import uuid4

# Create your models here.

class SMSCampaign(models.Model):
    unique_id = models.UUIDField(default=uuid4, unique=True, auto_created=True)
    name = models.CharField(max_length=255)
    message_template = models.TextField()
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.name
    

class Recipient(models.Model):
    unique_id = models.UUIDField(default=uuid4, unique=True, auto_created=True)
    phone_number = models.CharField(max_length=15)
    campaign = models.ForeignKey(SMSCampaign, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    params = models.JSONField(default=dict)  # {"name": "John", "location": "Dar es Salaam"}
    personalized_message = models.TextField(blank=True, null=True)
    dlr_value = models.IntegerField(blank=True, null=True)
    response_text = models.TextField(blank=True, null=True)  # Kannel or SMPP response
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'message {self.campaign.name} to {self.phone_number} '

# DLR received: {'sender': '255676855433', 'receiver': 'KILAKONA', 'dlr_val': '1', 'reply': 'sub:001+dlvrd:001+submit+date:2509041917+done+date:2509041917+stat:DELIVRD+err:000+text:'}

class MessageLog(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name="logs")
    dlr_value = models.IntegerField()
    response_text = models.TextField(blank=True, null=True)  # Kannel or SMPP response
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.recipient.phone_number}"
