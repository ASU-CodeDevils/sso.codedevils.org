import pytest
from django.test import RequestFactory

from cdsso.users.api.views import UserViewSet
from cdsso.users.models import User

pytestmark = pytest.mark.django_db
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        last_login = (
            None if not user.last_login else user.last_login.strftime(DATE_FORMAT)
        )
        date_joined = (
            None if not user.date_joined else user.date_joined.strftime(DATE_FORMAT)
        )

        assert response.data == {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            # "url": f"http://testserver/api/users/{user.username}/",
            "anonymous": user.anonymous,
            "date_joined": date_joined,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "is_alumni": user.is_alumni,
            "receive_notifications": user.receive_notifications,
            "last_login": last_login,
            "image_24": user.image_24,
            "image_512": user.image_512,
            "tz_offset": user.tz_offset,
            "slack_id": user.slack_id
        }
