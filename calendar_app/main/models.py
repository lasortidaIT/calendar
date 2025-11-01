from datetime import timedelta, datetime
from django.db import models
from django.utils.translation.trans_null import activate
from loging.models import CustomUser


class Event(models.Model):
    REPEAT_CHOICES = [
        ('none', 'Нет'),
        ('daily', 'Каждый день'),
        ('weekly', 'Каждую неделю'),
        ('monthly', 'Каждый месяц'),
        ('yearly', 'Каждый год'),
    ]

    END_REPEAT = [
        ('never', 'Никогда'),
        ('date', 'По дате')
    ]

    ALERT_CHOICES = [
        ('none', 'Нет'),
        ('30m', 'За 30 минут'),
        ('1h', 'За 1 час'),
        ('2h', 'За 2 часа'),
        ('3h', 'За 3 часа'),
        ('1d', 'В начале дня'),
    ]

    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    repeat_status = models.CharField(max_length=10, choices=REPEAT_CHOICES)
    end_repeat = models.CharField(max_length=10, choices=END_REPEAT)
    end_repeat_date = models.DateTimeField(default=datetime.now(), blank=True)
    alert = models.CharField(max_length=10, choices=ALERT_CHOICES)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events')

    next_time = models.DateTimeField(null=True, blank=True)
    next_alert_time = models.DateTimeField(null=True, blank=True)
    active_alert = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # выполняем подготовку к оповещениям
    def start_alerts(self, time):
        if self.repeat_status == 'none':
            start_date = datetime.fromisoformat(str(self.start_date))
            if start_date > time:
                self.active_alert = True
                self.next_time = datetime.isoformat(start_date)
                self.calculate_alert_time()
        else:
            curr = datetime.fromisoformat(str(self.start_date))
            while curr <= time:
                if self.repeat_status == 'daily':
                    curr += timedelta(days=1)
                elif self.repeat_status == 'weekly':
                    curr += timedelta(weeks=1)
                elif self.repeat_status == 'monthly':
                    curr += timedelta(days=30)
                elif self.repeat_status == 'yearly':
                    curr += timedelta(days=365)
            if self.end_repeat == 'date' and datetime.fromisoformat(str(self.end_date)) > curr or self.end_repeat == 'never':
                self.active_alert = True
                self.next_time = datetime.isoformat(curr)
                self.calculate_alert_time()

    def next_alert(self, time):
        next_time = datetime.fromisoformat(str(self.next_time))
        if self.repeat_status == 'daily':
            next_time += timedelta(days=1)
        elif self.repeat_status == 'weekly':
            next_time += timedelta(weeks=1)
        elif self.repeat_status == 'monthly':
            next_time += timedelta(days=30)
        elif self.repeat_status == 'yearly':
            next_time += timedelta(days=365)

        if self.end_repeat == 'date' and datetime.fromisoformat(str(self.end_date)) < next_time:
            self.active_alert = False
        else:
            self.next_time = datetime.isoformat(next_time)
            self.calculate_alert_time()


    def calculate_alert_time(self):
        timedate = datetime.fromisoformat(str(self.next_time))
        if self.alert == '30m':
            next_alert_time = timedate - timedelta(minutes=30)
        elif self.alert == '1h':
            next_alert_time = timedate - timedelta(hours=1)
        elif self.alert == '2h':
            next_alert_time = timedate - timedelta(hours=2)
        elif self.alert == '3h':
            next_alert_time = timedate - timedelta(hours=3)
        else:
            next_alert_time = timedate.replace(hour=0, minute=0)
        self.next_alert_time = datetime.isoformat(next_alert_time)
