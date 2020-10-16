import logging

from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cdsso.contrib.register.models import KnownMember, StudentRegistration

from .serializers import (
    KnownMemberSerializer,
    SlackErrorResponseSerializer,
    SlackResponseSerializer,
    SlackUserObjectSerializer,
    StudentRegistrationSerializer,
)

logger = logging.getLogger("api")
User = get_user_model()


class StudentRegistrationViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = StudentRegistrationSerializer
    queryset = StudentRegistration.objects.all()
    lookup_field = "id"


class KnownMemberViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = KnownMemberSerializer
    queryset = KnownMember.objects.all()
    lookup_field = "email"

    @swagger_auto_schema(
        request_body=SlackUserObjectSerializer,
        responses={
            200: openapi.Response("user registered on slack", SlackResponseSerializer),
            400: openapi.Response("invalid format", SlackErrorResponseSerializer)
        }
    )
    @action(detail=False, methods=["POST"], name="Update Slack information")
    def slack(self, request):
        """
        Updates a user's Slack information. If no user exists, their information is recorded for later
        when the member registers.
        """
        try:
            data = request.data
            user = data["user"]
            email = user["profile"]["email"]

            # update the user's information if they are already registered here
            member = User.objects.filter(email__exact=email)
            created = False
            if member.exists():
                member = member.first()
                member.studentregistration.slack_registered = True
                member.studentregistration.save()
            # or create a new known member if they haven't registered
            else:
                member, created = KnownMember.objects.get_or_create(email__exact=email)
                member.email = email
                member.slack_registered = True
                if created:
                    logger.info("Member found on Slack, but not registered: {}".format(email))

            member.slack_id = user["id"]
            member.tz_offset = user["tz_offset"]
            member.name = user["profile"]["real_name"]
            member.image_24 = user["profile"]["image_24"]
            member.image_512 = user["profile"]["image_512"]

            member.save()
            return Response(
                status=status.HTTP_200_OK,
                data={"ok": True,
                      "created": created,
                      "detail": "user registered on slack"}
            )
        # caught if a key was placed in the wrong position
        except KeyError as key:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"ok": False, "detail": "invalid format", "key": str(key)}
            )
        # unknown exceptions are caught and notify admin
        except Exception as e:
            logger.error("Error when register new member with Slack: {}".format(e))
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"ok": False, "detail": "internal server error"}
            )
