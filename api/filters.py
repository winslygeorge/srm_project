# api/filters.py
from django_filters import rest_framework as filters
from .models import (
    Donor, FundingOpportunity, GrantApplication,
    Sector, DonationType, FundraisingFrequency, ApplicationStatus
)

class DonorFilter(filters.FilterSet):
    created_at_gte = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_lte = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    sectors = filters.ModelMultipleChoiceFilter(
        queryset=Sector.objects.all(),
        field_name='sectors',
        to_field_name='id',
        conjoined=False
    )
    donation_type = filters.ModelChoiceFilter(
        queryset=DonationType.objects.all(),
        field_name='donation_type'
    )
    fundraising_frequency = filters.ModelChoiceFilter(
        queryset=FundraisingFrequency.objects.all(),
        field_name='fundraising_frequency'
    )
    is_active = filters.BooleanFilter()

    class Meta:
        model = Donor
        fields = ['sectors', 'donation_type', 'fundraising_frequency', 'is_active', 'created_at_gte', 'created_at_lte']


class FundingOpportunityFilter(filters.FilterSet):
    donor = filters.ModelChoiceFilter(
        queryset=Donor.objects.all(),
        field_name='donor'
    )
    deadline_gte = filters.DateTimeFilter(field_name='deadline', lookup_expr='gte')
    deadline_lte = filters.DateTimeFilter(field_name='deadline', lookup_expr='lte')
    is_active = filters.BooleanFilter()

    class Meta:
        model = FundingOpportunity
        fields = ['donor', 'is_active', 'deadline_gte', 'deadline_lte']


class GrantApplicationFilter(filters.FilterSet):
    funding_opportunity = filters.ModelChoiceFilter(
        queryset=FundingOpportunity.objects.all(),
        field_name='funding_opportunity'
    )
    status = filters.ModelChoiceFilter(
        queryset=ApplicationStatus.objects.all(),
        field_name='status'
    )
    submission_date_gte = filters.DateTimeFilter(field_name='submission_date', lookup_expr='gte')
    submission_date_lte = filters.DateTimeFilter(field_name='submission_date', lookup_expr='lte')
    amount_requested_gte = filters.NumberFilter(field_name='amount_requested', lookup_expr='gte')
    amount_requested_lte = filters.NumberFilter(field_name='amount_requested', lookup_expr='lte')
    amount_awarded_gte = filters.NumberFilter(field_name='amount_awarded', lookup_expr='gte')
    amount_awarded_lte = filters.NumberFilter(field_name='amount_awarded', lookup_expr='lte')

    class Meta:
        model = GrantApplication
        fields = ['funding_opportunity', 'status', 'submission_date_gte', 'submission_date_lte']