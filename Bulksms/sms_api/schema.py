import graphene
from .dtos import *
from .models import Message, Recipient

class AllQuery(graphene.ObjectType):
    all_sms = graphene.List(MessageOutput)


    @staticmethod
    def resolve_all_sms(self, info):
        try:
            messages = Message.objects.all()
            data = []
            for sms in messages:
                recipients_query = Recipient.objects.filter(message = sms)
                sms_data = MessageData(
                    unique_id = sms.unique_id,
                    message = sms.message,
                    is_sent = sms.is_sent,
                    created_at = sms.created_at,
                    updated_at = sms.updated_at
                )
                recipient_data = list(map(lambda x: RecipientData(unique_id = x.unique_id, number = x.number, received = x.received), recipients_query))
                data.append(MessageOutput(message = sms_data, recipients = recipient_data))
            return data
        except Exception as e:
            print(e)
            return None