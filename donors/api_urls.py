from django.urls import path
from donors import api_views

urlpatterns = [
    path('donors/', api_views.DonorListAPI.as_view(), name='api_donors'),
    path('camps/', api_views.CampListAPI.as_view(), name='api_camps'),
    path('requests/', api_views.BloodRequestListAPI.as_view(), name='api_requests'),
    path('requests/<str:request_id>/match/', api_views.MatchDonorsAPI.as_view(), name='api_match'),
    path('reports/camps/', api_views.CampReportAPI.as_view(), name='api_camp_report'),
]