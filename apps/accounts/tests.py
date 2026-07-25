from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class AuthenticationTests(APITestCase):

    def setUp(self):

        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.profile_url = reverse("profile")
        self.refresh_url = reverse("token_refresh")

        self.user_data = {
            "username": "kamal",
            "email": "kamal@test.com",
            "password": "Test@12345",
            "confirm_password": "Test@12345",
            "company_name": "OpenAI",
            "phone_number": "9876543210",
        }

    def create_user(self):
        return User.objects.create_user(
            username=self.user_data["username"],
            email=self.user_data["email"],
            password=self.user_data["password"],
            company_name=self.user_data["company_name"],
            phone_number=self.user_data["phone_number"],
        )

    def test_user_registration(self):

        response = self.client.post(
            self.register_url,
            self.user_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            User.objects.count(),
            1,
        )

    def test_login_success(self):

        self.create_user()

        response = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_password(self):

        self.create_user()

        response = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": "WrongPassword",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_duplicate_registration(self):

        self.create_user()

        response = self.client.post(
            self.register_url,
            self.user_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_profile_endpoint(self):

        self.create_user()

        login = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
            format="json",
        )

        access = login.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}"
        )

        response = self.client.get(
            self.profile_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_refresh_token(self):

        self.create_user()

        login = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
            format="json",
        )

        refresh = login.data["refresh"]

        response = self.client.post(
            self.refresh_url,
            {
                "refresh": refresh,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data,
        )