from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SectorViewSet, DonationTypeViewSet, FundraisingFrequencyViewSet,
    RequiredSubmissionTypeViewSet, ApplicationStatusViewSet,
    CommunicationTypeViewSet, TagViewSet, DonorViewSet,
    FundingOpportunityViewSet, GrantApplicationViewSet,
    CommunicationViewSet, DocumentViewSet, AlertViewSet,
    UserProfileViewSet, DashboardStatsView, PeriodStatsView
)

router = DefaultRouter()
router.register(r'sectors', SectorViewSet)
router.register(r'donation-types', DonationTypeViewSet)
router.register(r'frequencies', FundraisingFrequencyViewSet)
router.register(r'submission-types', RequiredSubmissionTypeViewSet)
router.register(r'application-statuses', ApplicationStatusViewSet)
router.register(r'communication-types', CommunicationTypeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'donors', DonorViewSet)
router.register(r'funding-opportunities', FundingOpportunityViewSet)
router.register(r'applications', GrantApplicationViewSet)
router.register(r'communications', CommunicationViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'user-profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('stats/period/', PeriodStatsView.as_view(), name='period-stats'),
]