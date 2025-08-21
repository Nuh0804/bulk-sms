import graphene

class createMessage(graphene.InputObjectType):
    message = graphene.String()
    recipients = graphene.List(graphene.String)

class MessageData(graphene.ObjectType):
    unique_id = graphene.UUID()
    message = graphene.String()
    is_sent = graphene.Boolean()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

class RecipientData(graphene.ObjectType):
    unique_id = graphene.UUID()
    number = graphene.String()
    received = graphene.Boolean()

class MessageOutput(graphene.ObjectType):
    message = graphene.Field(MessageData)
    recipients = graphene.List(RecipientData)


class MessageResponse(graphene.ObjectType):
    successful = graphene.Field(MessageOutput)
    failed = graphene.Field(MessageOutput)