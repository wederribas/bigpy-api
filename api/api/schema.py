import graphene

import bigpy.schema


class Query(bigpy.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
