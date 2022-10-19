from django.db import transaction
from apps.routine.models import Routine, RoutineResult, RoutineDay
from datetime import datetime


class RoutineResultSchedule:
    def __init__(self):
        self.Routine = Routine
        self.RoutineResult = RoutineResult
        self.RoutineDay = RoutineDay
    
    @transaction.atomic()
    def run(self):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} DB Routine result 데이터 동기화")
        day = self.RoutineDay.DAYS[datetime.now().weekday()][0]
        data = self.RoutineDay.objects.filter(day=day, routine_id__is_deleted=False)[:]

        for i, val in enumerate(data):
            print(f"data upload ... {i+1}")
            try:
                RoutineResult.objects.create(routine_id=val.routine_id, result="NOT")
            except Exception as e:
                print(f"Routine id: {val.id} 오류")
                print(e)
                continue

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} DB 데이터 동기화 완료")
        return


