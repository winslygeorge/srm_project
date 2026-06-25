from rest_framework import serializers
from .models import (
    Sector, DonationType, FundraisingFrequency, RequiredSubmissionType,
    ApplicationStatus, CommunicationType, Tag, Donor, FundingOpportunity,
    GrantApplication, Communication, Document, Alert, UserProfile
)
from django.contrib.auth import get_user_model

User = get_user_model()

# ---------- Lookup serializers ----------
class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'

class DonationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationType
        fields = '__all__'

class FundraisingFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = FundraisingFrequency
        fields = '__all__'

class RequiredSubmissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredSubmissionType
        fields = '__all__'

class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = '__all__'

class CommunicationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationType
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# ---------- Main serializers ----------
class DonorSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all(), many=True)
    specialisations = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    donation_type = serializers.PrimaryKeyRelatedField(queryset=DonationType.objects.all())
    fundraising_frequency = serializers.PrimaryKeyRelatedField(queryset=FundraisingFrequency.objects.all())
    what_is_required = serializers.PrimaryKeyRelatedField(queryset=RequiredSubmissionType.objects.all())

    class Meta:
        model = Donor
        fields = '__all__'

class FundingOpportunitySerializer(serializers.ModelSerializer):
    donor = serializers.PrimaryKeyRelatedField(queryset=Donor.objects.all())

    class Meta:
        model = FundingOpportunity
        fields = '__all__'

class GrantApplicationSerializer(serializers.ModelSerializer):
    funding_opportunity = serializers.PrimaryKeyRelatedField(queryset=FundingOpportunity.objects.all())
    status = serializers.PrimaryKeyRelatedField(queryset=ApplicationStatus.objects.all())

    class Meta:
        model = GrantApplication
        fields = '__all__'

class CommunicationSerializer(serializers.ModelSerializer):
    donor = serializers.PrimaryKeyRelatedField(queryset=Donor.objects.all())
    type = serializers.PrimaryKeyRelatedField(queryset=CommunicationType.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Communication
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Document
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

# ---------- Statistics serializers ----------
class DashboardStatsSerializer(serializers.Serializer):
    total_donors = serializers.IntegerField()
    active_opportunities = serializers.IntegerField()
    total_applications = serializers.IntegerField()
    applications_by_status = serializers.DictField(child=serializers.IntegerField())
    success_rate = serializers.FloatField()
    total_awarded_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    upcoming_deadlines = serializers.ListField(child=serializers.DictField())

class PeriodStatsSerializer(serializers.Serializer):
    period = serializers.CharField()
    donors_added = serializers.IntegerField()
    opportunities_added = serializers.IntegerField()
    applications_submitted = serializers.IntegerField()
    applications_awarded = serializers.IntegerField()
    total_awarded = serializers.DecimalField(max_digits=15, decimal_places=2)