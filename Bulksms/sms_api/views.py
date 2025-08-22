from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .models import *
# Create your views here.


class ReceiveMessage(APIView):
    def get(self, request, sender, text):
        # You can process the sender and text as needed
        print(f"Sender: {sender}, Message: {text}")
        
        # Example: save message to database if needed
        # Message.objects.create(sender=sender, message=text)

        return Response(
            {"status": "success", "sender": sender, "message": text},
            status=HTTP_200_OK
        )

class SmsDlr(APIView):
    def get(self, request, msgid, dest, source, smsc, orig_msgid, status, timestamp):
        # Capture all DLR data
        dlr_data = {
            "msgid": msgid,
            "dest": dest,
            "source": source,
            "smsc": smsc,
            "orig_msgid": orig_msgid,
            "status": status,
            "timestamp": timestamp,
        }

        # Print or save to database
        print("DLR received:", dlr_data)

        return Response(
            {"status": "dlr received", "data": dlr_data},
            status=HTTP_200_OK
            )
    