from rest_framework.serializers import (ListField, CharField, SerializerMethodField, Serializer, ModelSerializer)
from .models import Routine, RoutineDay, RoutineResult
from datetime import datetime


class RoutineCreateUpdateDeleteSerializer(ModelSerializer):
    days = ListField(write_only=True, min_length=1, max_length=7)

    class Meta:
        model = Routine
        fields = ('id', 'title', 'category', 'goal', 'is_alarm', 'days')
        read_only_fields = ('id', )

    def to_representation(self, instance):
        res = {'routine_id': instance.id}
        return res

    def create(self, validated_data):
        days = validated_data.pop('days')
        user = self.context['request'].user
        routine = self.Meta.model.objects.create(account_id=user, **validated_data)

        # routine의 요일 데이터 생성
        for day in days:
            RoutineDay.objects.create(routine_id=routine, day=day)
            # routine 생성 날짜와 요일이 같은 경우 result data 추가
            if day == RoutineDay.DAYS[datetime.now().weekday()][0]:
                RoutineResult.objects.create(routine_id=routine)

        return routine

    def update(self, instance, validated_data):
        days = validated_data.pop('days')

        if days:
            # 기존에 있던 routine 요일 데이터 삭제
            RoutineDay.objects.filter(routine_id=instance).delete()

            # 변경한 routine 요일 데이터 생성
            for day in days:
                RoutineDay.objects.create(routine_id=instance, day=day)
                # 변경한 routine 요일과 변경 날짜가 일치하는 경우
                if day == RoutineDay.DAYS[datetime.now().weekday()][0]:
                    # 요일 데이터를 전체 삭제 후 다시 생성하므로 기존에 이미 result data가 있었는지 확인 후 없으면 생성
                    res = RoutineResult.objects.filter(routine_id=instance, created_at__date=datetime.now().date())
                    if len(res) == 0:
                        RoutineResult.objects.create(routine_id=instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RoutineListSerializer(ModelSerializer):
    result = CharField(max_length=10)

    class Meta:
        model = Routine
        fields = ('id', 'title', 'goal', 'result')


class RoutineRetrieveSerializer(ModelSerializer):
    days = SerializerMethodField()

    class Meta:
        model = Routine
        fields = ('id', 'title', 'goal', 'days')

    def get_days(self, obj):
        """ routine의 요일 리스트를 반환하는 함수 """
        routine_days = RoutineDay.objects.filter(routine_id=obj).values_list('day', flat=True)
        days = list(routine_days)
        return days


class RoutineResultSerializer(ModelSerializer):
    class Meta:
        model = RoutineResult
        fields = '__all__'