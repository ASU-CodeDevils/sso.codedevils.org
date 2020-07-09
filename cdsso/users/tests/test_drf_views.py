import pytest
from datetime import datetime
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

        assert response.data == {
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.username}/",
            "anonymous": user.anonymous,
            "bio": user.bio,
            "date_joined": datetime.strftime(user.date_joined),
            "dob": user.dob,
            "facebook_url": user.facebook_url,
            "first_name": user.first_name,
            "github_username": user.github_username,
            "id": user.id,
            "instagram_url": user.instagram_url,
            "is_active": user.is_active,
            "last_login": datetime.strftime(user.last_login, fmt=DATE_FORMAT),
            "last_name": user.last_name,
            "linkedin_url": user.linkedin_url,
            "receive_notifications": user.receive_notifications,
            "slack_username": user.slack_username,
            "twitter_username": user.twitter_username
        }
