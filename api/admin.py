from django.contrib import admin
from .models import *

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(DonationType)
class DonationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(FundraisingFrequency)
class FundraisingFrequencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(RequiredSubmissionType)
class RequiredSubmissionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(ApplicationStatus)
class ApplicationStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(CommunicationType)
class CommunicationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sector']
    list_filter = ['sector']

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'donation_type', 'fundraising_frequency', 'is_active']
    list_filter = ['sectors', 'donation_type', 'fundraising_frequency', 'is_active']
    search_fields = ['name', 'contact_person', 'contact_email']
    filter_horizontal = ['sectors', 'specialisations']

@admin.register(FundingOpportunity)
class FundingOpportunityAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'donor', 'deadline', 'is_active']
    list_filter = ['donor', 'is_active']
    search_fields = ['title']

@admin.register(GrantApplication)
class GrantApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'funding_opportunity', 'status', 'submission_date']
    list_filter = ['status']
    search_fields = ['notes']

@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'donor', 'type', 'date', 'follow_up_date']
    list_filter = ['type']
    search_fields = ['summary']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'uploaded_at']
    search_fields = ['name']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'trigger_date', 'is_sent']
    list_filter = ['is_sent']
    search_fields = ['title']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'role']
    list_filter = ['role']