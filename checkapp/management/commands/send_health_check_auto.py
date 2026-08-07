from django.core.management.base import BaseCommand

from checkapp.services import send_health_check_to_all


class Command(BaseCommand):

    help = "健康チェックを全組合員へ自動送信"

    def handle(self, *args, **options):

        success, error = send_health_check_to_all()

        self.stdout.write(
            self.style.SUCCESS(
                f"完了 成功:{success}件 失敗:{error}件"
            )
        )