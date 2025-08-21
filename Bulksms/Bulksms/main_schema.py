import graphene
from sms_api.views import Mutation
from sms_api.schema import AllQuery

class Query(AllQuery, graphene.ObjectType):
    pass

class Mutation(Mutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)