"""Defines the schema for graphene"""
import graphene
from graphene_django.debug import DjangoDebug

from cdsso.contrib.countries import schema as countries_schema
from cdsso.contrib.register import schema as register_schema
from cdsso.users import schema as user_schema
from config.graphene import auth as auth_schema


class Query(
        auth_schema.Query,
        countries_schema.Query,
        register_schema.Query,
        user_schema.Query,
        graphene.ObjectType
):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(
        user_schema.Mutation,
        graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Subscription(
        user_schema.Subscriptions,
        graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")

    class Meta:
        description = "User and group subscriptions"


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
