from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.routine.models import Routine, RoutineDay, RoutineResult


class RoutineAPITest(APITestCase):
    """
    Routine CRRUD 테스트
    """
    def setUp(self):
        """ test 를 위한 mock 데이터 추가 """

        self.url = "/routines/"

        User = get_user_model()

        self.user = User.objects.create(
            nickname='test_user',
            password=make_password('test1234')
        )

        self.routine = Routine.objects.create(
            account_id=self.user,
            title='테스트 루틴',
            category=Routine.CATEGORY[0][0],
            goal='테스트 통과'
        )

        self.routine_day = RoutineDay.objects.create(
            routine_id=self.routine,
            day=RoutineDay.DAYS[2][0]
        )

        self.routine_result = RoutineResult.objects.create(
            routine_id=self.routine,
            result=RoutineResult.RESULT[1][0]
        )

        self.refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

    def test_routine_create_success(self):
        """ 프로젝트 생성 성공 테스트 """

        data = {
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }

        request_url = self.url
        response = self.client.post(request_url, data=data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_routine_list_success(self):
        """ routine list 성공 테스트 """
        request_url = self.url
        response = self.client.get(request_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routine_retrieve_success(self):
        """ routine retrieve 성공 테스트 """
        request_url = f"{self.url}{self.routine.id}/"
        response = self.client.get(request_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routine_update_success(self):
        """ routine update 성공 테스트 """

        data = {
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }
        request_url = f"{self.url}{self.routine.id}/"
        response = self.client.put(request_url, data=data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routine_destroy_success(self):
        """ routine 삭제 성공 테스트 """
        request_url = f"{self.url}{self.routine.id}/"
        response = self.client.delete(request_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routine_check_success(self):
        """ routine 결과 기록 성공 테스트 """
        data = {
            "result": "TRY",
        }
        request_url = f"{self.url}{self.routine.id}/check/"
        response = self.client.put(request_url, data=data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_routine_result_lookup_success(self):
        """ routine 결과 기록 조회 성공 테스트 """
        request_url = f"{self.url}{self.routine.id}/result/"
        response = self.client.get(request_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
