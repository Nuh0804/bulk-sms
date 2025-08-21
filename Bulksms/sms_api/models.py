from django.db import models
from uuid import uuid4

# Create your models here.

class Message(models.Model):
    unique_id = models.UUIDField(default=uuid4, unique=True, auto_created=True)
    message = models.CharField(max_length=160)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.message
    

class Recipient(models.Model):
    unique_id = models.UUIDField(default=uuid4, unique=True, auto_created=True)
    number = models.CharField(max_length=10)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    received = models.BooleanField(default=False)

    def __str__(self):
        return f'message {self.message.message} to {self.number} '
