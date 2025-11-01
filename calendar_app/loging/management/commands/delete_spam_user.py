from django.core.management.base import BaseCommand
from loging.models import CustomUser
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Удаляет пользователей, которые создали аккаунт более 60 минут назад и не подтвердили его."

    def handle(self, *args, **options):
        timer = timezone.now() - timedelta(hours=1) # вычисляем время запуска команды - 1 час
        # выбираем всех пользователей с не подтвержденной почтой и созданных раньше, чем timer
        deleted, _ = CustomUser.objects.filter(
            is_verified=False, date_joined__lt=timer
        ).delete()
        self.stdout.write(f"Удалено пользователей: {deleted}")
