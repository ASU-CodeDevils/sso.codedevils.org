from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cdsso.contrib.register.models import KnownMember, StudentRegistration

from .serializers import KnownMemberSerializer, StudentRegistrationSerializer


class StudentRegistrationViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = StudentRegistrationSerializer
    queryset = StudentRegistration.objects.all()
    lookup_field = "id"


class KnownMemberViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = KnownMemberSerializer
    queryset = KnownMember.objects.all()
    lookup_field = "email"

    @action(detail=False, methods=["PUT", "PATCH"])
    def register_slack(self, request):
        serializer = KnownMemberSerializer(data=request.data)
        if serializer.is_valid():
            # check first if the user has started the registration process
            registered = StudentRegistration.objects.filter(email__exact=serializer.data["email"])
            if registered:
                registered.update(slack_registered=True)
                registered.save()
            # if not, add them to the list of known members
            else:
                member = KnownMember.objects.filter(email__exact=serializer.data["email"])
                if member:
                    member.update(**serializer.data)
                else:
                    KnownMember.objects.create(**serializer.data)
            return Response(status=status.HTTP_200_OK, data={"ok": True, "detail": "user registered on slack"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"ok": False, **serializer.errors})
