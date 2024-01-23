import strawberry
from strawberry.fastapi import GraphQLRouter
from src.graphql.query import Query
from src.graphql.mutation import Mutation
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

# app = FastAPI()
# app.incl
# ude_router(graphql_app, prefix="/graphql")