import re
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from .models import *
from .utils import SMSUtils
from .serializers import *
# Create your views here.


def extract_placeholders(template: str):
    """Find all placeholders like {name}, {date} in the message template"""
    return re.findall(r"\{(.*?)\}", template)

class ReceiveMessage(APIView):
    def get(self, request, sender, text):
        # You can process the sender and text as needed
        print(f"Sender: {sender}, Message: {text}")
        
        # Example: save message to database if needed
        # Message.objects.create(sender=sender, message=text)

        return Response(
            {"status": "success", "sender": sender, "message": text},
            status=status.HTTP_200_OK
        )

class SmsDlr(APIView):
    def get(self, request, sender, receiver, msg, dlr_val, dlr_msg, reply, timestamp):
        # Capture all DLR data
        dlr_data = {
            "sender": sender,
            "receiver": receiver,
            "msg": msg,
            "dlr_val": dlr_val,
            "dlr_msg": dlr_msg,
            "reply": reply,
            "timestamp": timestamp,
        }

        # Print or save to database
        print("DLR received:", dlr_data)

        return Response(
            {"status": "dlr received", "data": dlr_data},
            status=status.HTTP_200_OK
            )
    
class SendSms(APIView):
    @transaction.atomic
    def post(self, request):
        """
        Expects JSON:
        {
          "message_template": "Hello {name}, your appointment is on {date}.",
          "recipients": [
            {"phone": "255676855433", "params": {"name": "John", "date": "2025-08-21"}}
          ]
        }
        """
        try:
            campaign_name = request.data.get("campaign")
            message_template = request.data.get("message_template")
            recipients = request.data.get("recipients", [])


            if not message_template or not recipients:
                return Response(
                    {"error": "Both 'message_template' and 'recipients' are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Step 1: Extract required placeholders from the template
            required_placeholders = extract_placeholders(message_template)
            # Step 2: Create campaign
            campaign = SMSCampaign.objects.create(
                message_template=message_template,
                name=campaign_name
            )

            # Step 3: Save recipients with personalized messages
            for recipient in recipients:
                phone = recipient.get("phone")
                params = recipient.get("params", {})

                # Validate params
                missing = [p for p in required_placeholders if p not in params]
                if missing:
                    return Response({
                        "phone": phone,
                        "error": f"Missing required params: {', '.join(missing)}"
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Format message
                message = message_template.format(**params)

                Recipient.objects.create(
                    phone_number=phone,
                    campaign=campaign,
                    params=params,
                    personalized_message=message
                )

            # Step 4: Send SMS
            data = []
            recipients_query = Recipient.objects.filter(campaign=campaign.pk)

            for r in recipients_query:
                response = SMSUtils.send_sms(r.phone_number, r.personalized_message)
                data.append({
                    "phone": r.phone_number,  # ✅ fixed
                    "personalized_message": r.personalized_message,  # ✅ fixed
                    "status_code": response.status_code,
                    "response": response.text.strip()
                })

            return Response({"data": data}, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            print("ERROR:", e)
            traceback.print_exc()
            return Response({"status": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        recipients = Recipient.objects.prefetch_related("campaign").all()
        serializer = RecipientSerializer(recipients, many=True)
        return Response(serializer.data)