from django.core.management.base import BaseCommand
from loging.models import CustomUser
from main.models import Event
from django.utils import timezone
from datetime import timedelta, datetime
import pytz
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = "Рассылает пользователем напоминания о событиях, которые они добавили"

    def handle(self, *args, **options):
        time_server = timezone.now()
        events = Event.objects.filter(active_alert=True)
        for event in events:
            author = event.author
            user_timezone = pytz.timezone(author.timezone)
            local_time = time_server.astimezone(user_timezone).replace(tzinfo=None)
            next_alert = datetime.fromisoformat(str(event.next_alert_time))
            if (local_time - next_alert).total_seconds() > 0 and ((local_time - next_alert).total_seconds() / 60) >= 30:
                send_mail(
                    subject=f'Напоминание: {event.title}',
                    message=f"У вас запланировано событие: {event.title}. {event.next_time}!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[author.email],
                    fail_silently=False,
                )
                print(f'Отправлено уведомление - {author.email}')
                event.next_alert(local_time)
                event.save()
