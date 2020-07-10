"""Defines the GraphQL schema for custom URLs."""

import graphene

from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django.types import DjangoObjectType

from cdsso.users.api.serializers import UserSerializer, USER_EXCLUDE_FIELDS
from cdsso.users.models import User


class UserNode(DjangoObjectType):
    """
    User information who are not marked anonymous. The actualCount will have the total number of members,
    and the resulting data will be non-anonymous users.
    """
    class Meta:
        model = User
        interfaces = (Node,)
        description = "User information"
        exclude = USER_EXCLUDE_FIELDS
        lookup_field = "username"
        filter_fields = {
            "username": ["exact"],
            "email": ["exact", "icontains", "istartswith"],
            "name": ["icontains", "istartswith"],
        }

    @classmethod
    def get_queryset(cls, queryset, info):
        """Overrides the default queryset to filter anyone who wishes to remain anonymous."""
        return queryset.filter(anonymous=False)


class UserSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = UserSerializer
        lookup_field = "username"
        model_operations = ["update", "patch"]
        description = "Change/update user information"


class Query(graphene.ObjectType):
    user = Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


class Mutation(graphene.ObjectType):
    update_user = UserSerializerMutation.Field()
