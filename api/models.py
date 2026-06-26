from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

# ---------- Lookup tables (dynamic choices) ----------

class Sector(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DonationType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class FundraisingFrequency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RequiredSubmissionType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ApplicationStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CommunicationType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True, related_name='tags')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------- Main Entities ----------

class Donor(models.Model):
    name = models.CharField(max_length=255)
    sectors = models.ManyToManyField(Sector, related_name='donors')
    donation_type = models.ForeignKey(DonationType, on_delete=models.PROTECT, related_name='donors')
    specialisations = models.ManyToManyField(Tag, blank=True, related_name='donors')
    donor_relationship_strategy = models.TextField(blank=True)
    fundraising_frequency = models.ForeignKey(FundraisingFrequency, on_delete=models.PROTECT, related_name='donors')
    what_is_required = models.ForeignKey(RequiredSubmissionType, on_delete=models.PROTECT, related_name='donors')
    website = models.URLField(blank=True)
    contact_person = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class FundingOpportunity(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='funding_opportunities')
    title = models.CharField(max_length=255)
    description = models.TextField()
    call_opening_date = models.DateTimeField(null=True, blank=True)
    call_closing_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField()
    link_to_call = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return f"{self.title} ({self.donor.name})"


class GrantApplication(models.Model):
    funding_opportunity = models.ForeignKey(FundingOpportunity, on_delete=models.CASCADE, related_name='applications')
    status = models.ForeignKey(ApplicationStatus, on_delete=models.PROTECT, related_name='applications')
    submission_date = models.DateTimeField(auto_now_add=True)
    outcome = models.TextField(blank=True)
    amount_requested = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    amount_awarded = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submission_date']

    def __str__(self):
        return f"Application for {self.funding_opportunity.title}"


class Communication(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='communications')
    type = models.ForeignKey(CommunicationType, on_delete=models.PROTECT, related_name='communications')
    date = models.DateTimeField()
    summary = models.TextField()
    follow_up_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='communications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.type.name} with {self.donor.name} on {self.date}"


class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    description = models.TextField(blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Alert(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    trigger_date = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['trigger_date']

    def __str__(self):
        return self.title


# UserProfile (for roles)
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')

    def __str__(self):
        return f"{self.user.username} - {self.role}"