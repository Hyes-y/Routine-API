from rest_framework.serializers import (ListField, CharField, SerializerMethodField, Serializer, ModelSerializer)
from .models import Routine, RoutineDay, RoutineResult


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

        for day in days:
            RoutineDay.objects.create(routine_id=routine, day=day)

        return routine

    def update(self, instance, validated_data):
        days = validated_data.pop('days')

        if days:
            RoutineDay.objects.filter(routine_id=instance).delete()
            for day in days:
                RoutineDay.objects.create(routine_id=instance, day=day)

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
    result = CharField(max_length=10)
    days = SerializerMethodField()

    class Meta:
        model = Routine
        fields = ('id', 'title', 'goal', 'result', 'days')

    def get_days(self, obj):
        routine_days = RoutineDay.objects.filter(routine_id=obj).values_list('day', flat=True)
        days = list(routine_days)
        return days
