from django.db import models
from django.contrib.auth import get_user_model


class Routine(models.Model):
    USER = get_user_model()
    CATEGORY = (
        ('MIRACLE', 'MIRACLE'),
        ('HOMEWORK', 'HOMEWORK'),
    )

    account_id = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        db_column='account_id',
        related_name='routines',
    )
    title = models.CharField(
        verbose_name='제목',
        max_length=30,
    )
    category = models.CharField(
        verbose_name='분류',
        max_length=20,
        choices=CATEGORY,
    )
    goal = models.CharField(
        verbose_name='목표',
        max_length=50,
    )
    is_alarm = models.BooleanField(
        verbose_name='알림 여부',
        default=False,
    )
    is_deleted = models.BooleanField(
        verbose_name='삭제 여부',
        default=False,
    )
    created_at = models.DateTimeField(
        verbose_name='생성 날짜',
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        verbose_name='수정 날짜',
        auto_now=True,
    )


class RoutineResult(models.Model):
    RESULT = (
        ('NOT', '안함'),
        ('TRY', '시도'),
        ('DONE', '완료'),
    )

    routine_id = models.ForeignKey(
        Routine,
        on_delete=models.CASCADE,
        db_column='routine_id',
        related_name='routine_results',
    )
    result = models.CharField(
        verbose_name='수행 결과',
        max_length=10,
        choices=RESULT,
        default=RESULT[0][0],
    )
    is_deleted = models.BooleanField(
        verbose_name='삭제 여부',
        default=False,
    )
    created_at = models.DateTimeField(
        verbose_name='생성 날짜',
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        verbose_name='수정 날짜',
        auto_now=True,
    )


class RoutineDay(models.Model):
    DAYS = (
        ('MON', '월요일'),
        ('TUE', '화요일'),
        ('WED', '수요일'),
        ('THU', '목요일'),
        ('FRI', '금요일'),
        ('SAT', '토요일'),
        ('SUN', '일요일'),
    )

    routine_id = models.ForeignKey(
        Routine,
        on_delete=models.CASCADE,
        db_column='routine_id',
        related_name='routine_days',
    )
    day = models.CharField(
        verbose_name='요일',
        max_length=10,
        choices=DAYS,
    )
    created_at = models.DateTimeField(
        verbose_name='생성 날짜',
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        verbose_name='수정 날짜',
        auto_now=True,
    )
