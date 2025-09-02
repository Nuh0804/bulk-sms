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
    received = models.BooleanField(default=False)
    params = models.JSONField(default=dict)  # {"name": "John", "location": "Dar es Salaam"}
    personalized_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'message {self.campaign.name} to {self.phone_number} '


class MessageLog(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name="logs")
    status = models.CharField(
        max_length=30,
        choices=[
            ("queued", "Queued"),
            ("sent", "Sent"),
            ("delivered", "Delivered"),
            ("failed", "Failed"),
        ],
        default="queued"
    )
    response_text = models.TextField(blank=True, null=True)  # Kannel or SMPP response
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.recipient.phone_number} - {self.status}"


class Dlr(models.Model):
    smsc = models.CharField(max_length=500)
    timestamp = models.IntegerField()  # let DB set it
    destination = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    service = models.CharField(max_length=160)
    url = models.TextField()
    mask = models.IntegerField()
    status = models.IntegerField()
    boxc = models.CharField(max_length=100)