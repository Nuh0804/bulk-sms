from django.db import IntegrityError
import graphene
from .dtos import *
from .models import *
# Create your views here.

class CreateMessageMutation(graphene.Mutation):
    class Arguments:
        input = createMessage(required = True)

    data = graphene.String()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input):
        try:
            message = Message.objects.create(message = input.message)
            for recipient in input.recipients:
                Recipient.objects.create(number = recipient, message = message)
            return CreateMessageMutation(data = "successful stored and queued for sending", success = True)
        except Exception as e:
            print(e)
            return CreateMessageMutation(data = "failed", success = False)
        


class Mutation(graphene.ObjectType):
    create_message = CreateMessageMutation.Field()