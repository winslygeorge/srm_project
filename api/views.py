# api/views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncWeek, TruncYear
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.decorators import action
from rest_framework import status

from .models import (
    Sector, DonationType, FundraisingFrequency, RequiredSubmissionType,
    ApplicationStatus, CommunicationType, Tag, Donor, FundingOpportunity,
    GrantApplication, Communication, Document, Alert, UserProfile
)
from .serializers import (
    SectorSerializer, DonationTypeSerializer, FundraisingFrequencySerializer,
    RequiredSubmissionTypeSerializer, ApplicationStatusSerializer,
    CommunicationTypeSerializer, TagSerializer, DonorSerializer,
    FundingOpportunitySerializer, GrantApplicationSerializer,
    CommunicationSerializer, DocumentSerializer, AlertSerializer,
    UserProfileSerializer
)
from .permissions import IsAdminOrReadOnly, IsManagerOrAdmin
from .pagination import CustomPageNumberPagination
from .filters import DonorFilter, FundingOpportunityFilter, GrantApplicationFilter


# ---------- Lookup ViewSets ----------
class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']


class DonationTypeViewSet(viewsets.ModelViewSet):
    queryset = DonationType.objects.all()
    serializer_class = DonationTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ['name']


class FundraisingFrequencyViewSet(viewsets.ModelViewSet):
    queryset = FundraisingFrequency.objects.all()
    serializer_class = FundraisingFrequencySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ['name']


class RequiredSubmissionTypeViewSet(viewsets.ModelViewSet):
    queryset = RequiredSubmissionType.objects.all()
    serializer_class = RequiredSubmissionTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ['name']


class ApplicationStatusViewSet(viewsets.ModelViewSet):
    queryset = ApplicationStatus.objects.all()
    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ['name']


class CommunicationTypeViewSet(viewsets.ModelViewSet):
    queryset = CommunicationType.objects.all()
    serializer_class = CommunicationTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ['name']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sector']
    search_fields = ['name']


# ---------- Main ViewSets ----------
class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DonorFilter
    search_fields = ['name', 'contact_person', 'contact_email']
    ordering_fields = ['name', 'created_at']

    @action(detail=True, methods=['post'])
    def send_email(self, request, pk=None):
        donor = self.get_object()

        # Get recipient email from request data
        recipient_email = request.data.get('to_email')
        if not recipient_email:
            return Response(
                {"error": "Recipient email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        subject = request.data.get('subject')
        body = request.data.get('body')
        if not subject or not body:
            return Response(
                {"error": "Subject and body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Send email
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient_email],
            )
            email.send(fail_silently=False)

            # Create communication log
            comm_type, _ = CommunicationType.objects.get_or_create(
                name="Email",
                defaults={"description": "Outgoing email"}
            )

            # Store the full email content in the `summary` field
            communication = Communication.objects.create(
                donor=donor,
                type=comm_type,
                date=timezone.now(),
                summary=f"Email sent to {recipient_email} - Subject: {subject}\n\n{body}",
                created_by=request.user if request.user.is_authenticated else None,
            )

            # Return the created communication
            serializer = CommunicationSerializer(communication)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FundingOpportunityViewSet(viewsets.ModelViewSet):
    queryset = FundingOpportunity.objects.all()
    serializer_class = FundingOpportunitySerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FundingOpportunityFilter
    search_fields = ['title', 'description']
    ordering_fields = ['deadline', 'call_opening_date']


class GrantApplicationViewSet(viewsets.ModelViewSet):
    queryset = GrantApplication.objects.all()
    serializer_class = GrantApplicationSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = GrantApplicationFilter
    search_fields = ['notes', 'outcome']
    ordering_fields = ['submission_date']


class CommunicationViewSet(viewsets.ModelViewSet):
    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['donor', 'type']
    search_fields = ['summary']
    ordering_fields = ['date', 'follow_up_date']


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['content_type', 'object_id']
    search_fields = ['name', 'description']


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_sent', 'content_type', 'object_id']
    search_fields = ['title', 'message']
    ordering_fields = ['trigger_date']


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# ---------- Statistics Views ----------
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_donors = Donor.objects.filter(is_active=True).count()
        active_opportunities = FundingOpportunity.objects.filter(is_active=True).count()
        total_applications = GrantApplication.objects.count()

        app_status_counts = GrantApplication.objects.values('status__name').annotate(count=Count('id'))
        apps_by_status = {item['status__name']: item['count'] for item in app_status_counts}

        submitted_apps = GrantApplication.objects.exclude(status__name='Draft')
        awarded_apps = submitted_apps.filter(status__name='Awarded')
        success_rate = (awarded_apps.count() / submitted_apps.count()) * 100 if submitted_apps.count() > 0 else 0
        total_awarded = awarded_apps.aggregate(Sum('amount_awarded'))['amount_awarded__sum'] or 0

        now = timezone.now()
        upcoming = FundingOpportunity.objects.filter(
            deadline__gte=now, deadline__lte=now + timedelta(days=30), is_active=True
        ).order_by('deadline')[:10]
        upcoming_data = [{'title': opp.title, 'donor': opp.donor.name, 'deadline': opp.deadline} for opp in upcoming]

        data = {
            'total_donors': total_donors,
            'active_opportunities': active_opportunities,
            'total_applications': total_applications,
            'applications_by_status': apps_by_status,
            'success_rate': round(success_rate, 2),
            'total_awarded_amount': total_awarded,
            'upcoming_deadlines': upcoming_data,
        }
        return Response(data)


class PeriodStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        period = request.query_params.get('period', 'monthly')  # monthly, weekly, yearly
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        sector = request.query_params.get('sector')
        donation_type = request.query_params.get('donation_type')

        donor_qs = Donor.objects.filter(is_active=True)
        opp_qs = FundingOpportunity.objects.all()
        app_qs = GrantApplication.objects.all()

        if sector:
            donor_qs = donor_qs.filter(sectors__id=sector)
            opp_qs = opp_qs.filter(donor__sectors__id=sector)
            app_qs = app_qs.filter(funding_opportunity__donor__sectors__id=sector)
        if donation_type:
            donor_qs = donor_qs.filter(donation_type__id=donation_type)
            opp_qs = opp_qs.filter(donor__donation_type__id=donation_type)
            app_qs = app_qs.filter(funding_opportunity__donor__donation_type__id=donation_type)

        if start_date:
            start_date = datetime.fromisoformat(start_date)
            donor_qs = donor_qs.filter(created_at__gte=start_date)
            opp_qs = opp_qs.filter(created_at__gte=start_date)
            app_qs = app_qs.filter(created_at__gte=start_date)
        if end_date:
            end_date = datetime.fromisoformat(end_date)
            donor_qs = donor_qs.filter(created_at__lte=end_date)
            opp_qs = opp_qs.filter(created_at__lte=end_date)
            app_qs = app_qs.filter(created_at__lte=end_date)

        trunc_func = {'monthly': TruncMonth, 'weekly': TruncWeek, 'yearly': TruncYear}.get(period, TruncMonth)

        donors_by_period = donor_qs.annotate(period=trunc_func('created_at')).values('period').annotate(count=Count('id')).order_by('period')
        opps_by_period = opp_qs.annotate(period=trunc_func('created_at')).values('period').annotate(count=Count('id')).order_by('period')
        apps_by_period = app_qs.annotate(period=trunc_func('created_at')).values('period').annotate(count=Count('id')).order_by('period')
        awarded_apps = app_qs.filter(status__name='Awarded')
        awarded_by_period = awarded_apps.annotate(period=trunc_func('created_at')).values('period').annotate(
            count=Count('id'), total_awarded=Sum('amount_awarded')).order_by('period')

        periods_set = set()
        for item in donors_by_period:
            if item['period']:
                periods_set.add(item['period'].isoformat())
        for item in opps_by_period:
            if item['period']:
                periods_set.add(item['period'].isoformat())
        for item in apps_by_period:
            if item['period']:
                periods_set.add(item['period'].isoformat())
        for item in awarded_by_period:
            if item['period']:
                periods_set.add(item['period'].isoformat())

        result = []
        for p in sorted(periods_set):
            donor_count = next((item['count'] for item in donors_by_period if item['period'] and item['period'].isoformat() == p), 0)
            opp_count = next((item['count'] for item in opps_by_period if item['period'] and item['period'].isoformat() == p), 0)
            app_count = next((item['count'] for item in apps_by_period if item['period'] and item['period'].isoformat() == p), 0)
            awarded = next((item for item in awarded_by_period if item['period'] and item['period'].isoformat() == p), None)
            awarded_count = awarded['count'] if awarded else 0
            awarded_total = awarded['total_awarded'] if awarded else 0

            result.append({
                'period': p,
                'donors_added': donor_count,
                'opportunities_added': opp_count,
                'applications_submitted': app_count,
                'applications_awarded': awarded_count,
                'total_awarded': awarded_total,
            })

        return Response(result)