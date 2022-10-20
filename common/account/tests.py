from django.contrib.auth import get_user_model
from django.contrib.auth.models import make_password
from rest_framework import status
from rest_framework.test import APITestCase


class AccountAPITest(APITestCase):
    """
    유저 회원가입, 로그인 테스트
    """
    User = get_user_model()

    def setUp(self):
        """ test 를 위한 mock 데이터 추가 """
        self.email = "test@test.com"
        self.nickname = "test_user"
        self.password = "test1234!"
        self.user = self.User.objects.create(
            email=self.email,
            nickname=self.nickname,
            password=make_password(self.password)
        )

    def test_signup_success(self):
        """ 회원 가입 성공 테스트 """

        data = {
            "email": "test2@test.com",
            "nickname": "test_user_2",
            "password": "test5678!",
            "password2": "test5678!",
        }

        request_url = "/account/signup/"

        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_fail_due_to_invalid_password_minimum_length(self):
        """ 회원 가입 실패 테스트 : 비밀번호 길이가 8자 미만인 경우 """

        data = {
            "email": "test3@test.com",
            "nickname": "test_user_3",
            "password": "test56!",
            "password2": "test56!",
        }

        request_url = "/account/signup/"

        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_fail_due_to_invalid_password(self):
        """ 회원 가입 실패 테스트 : 비밀번호가 문자, 숫자, 특수문자 모두 포함하지 않은 경우 """

        data = {
            "email": "test4@test.com",
            "nickname": "test_user_4",
            "password": "test56789",
            "password2": "test56789",
        }

        request_url = "/account/signup/"

        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_fail_due_to_not_match_p1_and_p2(self):
        """ 회원 가입 실패 테스트 : 입력 받은 비밀번호 2개가 일치하지 않는 경우 """

        data = {
            "email": self.email,
            "nickname": self.nickname,
            "password": self.password,
            "password2": self.password + "salt",
        }

        request_url = "/account/signup/"

        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """ 로그인 성공 테스트 """

        data = {
            "email": self.email,
            "password": self.password,
        }

        request_url = "/account/login/"

        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail_due_to_wrong_password(self):
        """ 로그인 실패 테스트 : 잘못된 비밀번호 """

        data = {
            "email": self.email,
            "password": self.password + "salt",
        }

        request_url = "/account/login/"

        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

