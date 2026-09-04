from django.core.management.base import BaseCommand
from django.utils import timezone

from checkapp.models import HealthCheckSchedule
from checkapp.services import send_health_check_to_all


class Command(BaseCommand):

    help = "健康チェックの定期送信設定を確認して自動送信"

    def handle(self, *args, **options):

        schedule = HealthCheckSchedule.objects.filter(pk=1).first()

        if not schedule:
            self.stdout.write("定期送信設定がありません")
            return

        if not schedule.enabled:
            self.stdout.write("自動送信はOFFです")
            return

        now = timezone.localtime()

        # 設定した曜日でなければ送信しない
        if now.weekday() != schedule.weekday:
            self.stdout.write("今日は送信曜日ではありません")
            return

        # 設定時刻より前なら送信しない
        current_time = now.time().replace(
            second=0,
            microsecond=0,
            tzinfo=None
        )

        if current_time < schedule.send_time:
            self.stdout.write("まだ送信時刻になっていません")
            return

        # 今日すでに送信済みなら二重送信しない
        if schedule.last_sent_at:
            last_sent = timezone.localtime(schedule.last_sent_at)

            if last_sent.date() == now.date():
                self.stdout.write("今日はすでに送信済みです")
                return

        success, error = send_health_check_to_all()

        schedule.last_sent_at = now
        schedule.save(update_fields=["last_sent_at"])

        self.stdout.write(
            self.style.SUCCESS(
                f"健康チェック自動送信完了 成功:{success}件 失敗:{error}件"
            )
        )