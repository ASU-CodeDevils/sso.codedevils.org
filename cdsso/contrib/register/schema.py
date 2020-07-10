"""Defines the GraphQL schema for custom URLs."""

import graphene

from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from cdsso.contrib.register.models import StudentRegistration


class StudentRegistrationNode(DjangoObjectType):
    """Provides links to all CodeDevils custom URLs."""
    class Meta:
        model = StudentRegistration
        interfaces = (Node,)
        description = "Student registration process"
        filter_fields = {
            "slack_registered": ["exact"],
            "sds_registered": ["exact"],
            "user__username": ["exact"]
        }


class Query(object):
    registration = graphene.Node.Field(StudentRegistrationNode)
    registrations = DjangoFilterConnectionField(StudentRegistrationNode)
