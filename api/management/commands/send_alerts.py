from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from api.models import Alert
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Send due alerts via email'

    def handle(self, *args, **options):
        now = timezone.now()
        due_alerts = Alert.objects.filter(trigger_date__lte=now, is_sent=False)
        for alert in due_alerts:
            recipients = User.objects.filter(profile__role__in=['admin', 'manager', 'staff']).values_list('email', flat=True)
            if recipients:
                send_mail(
                    subject=f"SRM Alert: {alert.title}",
                    message=alert.message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=list(recipients),
                    fail_silently=True,
                )
            alert.is_sent = True
            alert.save()
            self.stdout.write(self.style.SUCCESS(f"Sent alert '{alert.title}'"))
        self.stdout.write(self.style.SUCCESS("Alert sending completed."))