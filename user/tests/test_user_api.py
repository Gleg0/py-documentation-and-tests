from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

MOVIE_URL = reverse("cinema:movie-list")

class JWTAuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="password"
        )

    def test_jwt_authentication_flow(self):
        url = reverse("user:token_obtain_pair")
        res = self.client.post(url, {"email": self.user.email, "password": "password"}, format="json")
        self.assertEqual(res.status_code, 200)
        access = res.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        res = self.client.get(MOVIE_URL)
        self.assertEqual(res.status_code, 200)

        self.client.credentials()
        res = self.client.get(MOVIE_URL)
        self.assertEqual(res.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")
        res = self.client.get(MOVIE_URL)
        self.assertEqual(res.status_code, 401)
