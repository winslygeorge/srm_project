from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import FundingOpportunity, Communication, Alert
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=FundingOpportunity)
def create_deadline_alert(sender, instance, created, **kwargs):
    if created:
        alert_date = instance.deadline - timezone.timedelta(days=7)
        if alert_date > timezone.now():
            Alert.objects.create(
                title=f"Deadline approaching: {instance.title}",
                message=f"The funding opportunity '{instance.title}' closes on {instance.deadline}.",
                trigger_date=alert_date,
                content_type=ContentType.objects.get_for_model(instance),
                object_id=instance.id
            )

@receiver(post_save, sender=Communication)
def create_followup_alert(sender, instance, created, **kwargs):
    if instance.follow_up_date and instance.follow_up_date > timezone.now():
        ct = ContentType.objects.get_for_model(instance)
        if not Alert.objects.filter(content_type=ct, object_id=instance.id, title__icontains="Follow-up").exists():
            Alert.objects.create(
                title=f"Follow-up with {instance.donor.name}",
                message=f"Follow-up on communication dated {instance.date}. Summary: {instance.summary[:100]}",
                trigger_date=instance.follow_up_date,
                content_type=ct,
                object_id=instance.id
            )