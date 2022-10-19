from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    RoutineCreateUpdateDeleteSerializer,
    RoutineListSerializer,
    RoutineRetrieveSerializer,
    RoutineResultSerializer
)
from .models import Routine, RoutineResult
from django.db.models import F
from datetime import datetime


class RoutineViewSet(viewsets.ModelViewSet):
    """ Routine CRRUD API """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ queryset 반환 함수 """
        if self.action in ('create', 'update', 'destroy'):
            queryset = Routine.objects.filter(
                account_id=self.request.user,
                is_deleted=False
            )
        elif self.action in 'retrieve':
            queryset = Routine.objects.filter(
                account_id=self.request.user,
                is_deleted=False,
                routine_results__created_at__date=datetime.now().date(),
            ).annotate(result=F('routine_results__result'))

        else:
            # list 요청시 날짜(현재 날짜 이전)에 해당하는 루틴만 조회 가능
            params = self.request.query_params
            today = datetime.now().strftime('%Y-%m-%d')
            date = params.get('date', today)

            if date > today:
                raise ParseError(f"{today} 이전 루틴만 확인 가능합니다.")

            queryset = Routine.objects.prefetch_related('routine_results').filter(
                account_id=self.request.user,
                # is_deleted=False,
                routine_results__created_at__date=date,
            ).annotate(result=F('routine_results__result'))

        return queryset

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'destroy'):
            return RoutineCreateUpdateDeleteSerializer
        elif self.action == 'list':
            return RoutineListSerializer
        else:
            return RoutineRetrieveSerializer

    def list(self, request, *args, **kwargs):
        response = super(RoutineViewSet, self).list(request, *args, **kwargs)
        data = {
            "data": response.data,
            "message": {
                "msg": "Routine lookup was successful.",
                "status": "ROUTINE_LIST_OK"
            }
        }
        response.data = data
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(RoutineViewSet, self).retrieve(request, *args, **kwargs)
        data = {
            "data": response.data,
            "message": {
                "msg": "Routine lookup was successful.",
                "status": "ROUTINE_DETAIL_OK"
            }
        }
        response.data = data
        return response

    def create(self, request, *args, **kwargs):
        response = super(RoutineViewSet, self).create(request, *args, **kwargs)
        data = {
            "data": response.data,
            "message": {
                "msg": "You have successfully created the routine.",
                "status": "ROUTINE_CREATE_OK"
             }
        }
        response.data = data
        return response

    def update(self, request, *args, **kwargs):
        response = super(RoutineViewSet, self).update(request, *args, **kwargs)
        data = {
            "data": response.data,
            "message": {
                "msg": "The routine has been modified.",
                "status": "ROUTINE_UPDATE_OK"
            }
        }
        response.data = data
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {
            "data": {
                "routine_id": instance.id
            },
            "message": {
                "msg": "The routine has been deleted.",
                "status": "ROUTINE_DELETE_OK"
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """
        routine 삭제
        is_deleted: True 로 변경
        """
        instance.is_deleted = True
        instance.save()

    @action(detail=True, methods=['get'])
    def result(self, request, *args, **kwargs):
        try:
            response = super(RoutineViewSet, self).retrieve(request, *args, **kwargs)
            instance = self.get_object()
            routine_result = RoutineResult.objects.filter(
                routine_id=instance,
                created_at__date=datetime.now().date(),
            )[0]
            response.data['result'] = routine_result.result
            data = {
                "data": response.data,
                "message": {
                    "msg": "The routine result lookup was successful.",
                    "status": "ROUTINE_RESULT_LOOKUP_OK"
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                "message": {
                    "msg": "You can only lookup what you have to do today.",
                    "status": "ROUTINE_RESULT_LOOKUP_FAIL"
                }
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def check(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            routine_result = RoutineResult.objects.filter(
                routine_id=instance,
                created_at__date=datetime.now().date(),
            )[0]

            value = request.data.get('result', 'NOT')
            routine_result.result = value
            routine_result.save()

            data = {
                "data": {
                    "routine_id": instance.id
                },
                "message": {
                    "msg": "The routine result has been modified.",
                    "status": "ROUTINE_RESULT_UPDATE_OK"
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                "message": {
                    "msg": "You can only check what you have to do today.",
                    "status": "ROUTINE_RESULT_UPDATE_FAIL"
                }
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class RoutineResultView(viewsets.ModelViewSet):
    serializer_class = RoutineResultSerializer

    def get_queryset(self):
        queryset = RoutineResult.objects.filter(
            routine_id__account_id=self.request.user,
        )

        return queryset

