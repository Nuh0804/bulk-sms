import re
from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
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
    def get(self, request, sender, receiver, dlr_val, reply, message):
        # Capture all DLR data
        dlr_data = {
            "sender": sender,
            "receiver": receiver,
            "dlr_val": dlr_val,
            "reply": reply,
            "msg": message
        }

        # Print or save to database
        print("DLR received:", dlr_data)

        # MessageLog.objects.create(

        # )
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

            # Step 1: Create campaign
            campaign = SMSCampaign.objects.create(
                message_template=message_template,
                name=campaign_name
            )
            # Step 2: Extract required placeholders from the template
            required_placeholders = extract_placeholders(message_template)

            # Step 3: Save recipients with personalized messages
            data = []
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

                saved_recepient = Recipient.objects.create(
                    phone_number=phone,
                    campaign=campaign,
                    params=params,
                    personalized_message=message,
                )
                response = SMSUtils.send_sms(phone, message)
                text = response.text.split(": ")
                saved_recepient.status = True if text[0]==0 else False
                saved_recepient.dlr_value = text[0]
                saved_recepient.response_text = text[1]
                saved_recepient.delivered_at = datetime.now(timezone.utc)
                saved_recepient.save()
                data.append({
                    "phone": phone,  
                    "personalized_message": message,  
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
    

class CampaignViewSet(ModelViewSet):
    def get_queryset(self):
        return SMSCampaign.objects.all()
    
    serializer_class = CampaignSerializer


class AddRecipient(APIView):
    def post(self, request, pk):
        serializer = RecipientCreateSerializer(data = request.data, many = True)
        campaign_queryset = SMSCampaign.objects.filter(id = pk).first()
        if not campaign_queryset:
            return Response({"data": None, "message": "no campaign found"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid(raise_exception=True):
            recipients = []
            for validated_data in serializer.validated_data:
                personalized_message = campaign_queryset.message_template.format(**validated_data["params"])
                recipients.append(Recipient(campaign=campaign_queryset, personalized_message = personalized_message, **validated_data))
            Recipient.objects.bulk_create(recipients)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)