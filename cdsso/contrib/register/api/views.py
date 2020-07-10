from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from cdsso.contrib.register.models import StudentRegistration

from .serializers import StudentRegistrationSerializer


class StudentRegistrationViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = StudentRegistrationSerializer
    queryset = StudentRegistration.objects.all()
    lookup_field = "id"
