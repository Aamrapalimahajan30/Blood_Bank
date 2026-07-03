from django.urls import path
from donors import views, auth_views

urlpatterns = [
    path('', views.camp_listing, name='home'),
    path('donors/register/', views.register_donor, name='register_donor'),
    path('camps/', views.camp_listing, name='camp_listing'),
    path('camps/register-donor/', views.camp_register_donor, name='camp_register_donor'),
    path('requests/', views.request_board, name='request_board'),
    path('requests/<str:request_id>/match/', views.match_donors_view, name='match_donors'),
    path('reports/camps/', views.camp_report, name='camp_report'),

    path('signup/', auth_views.hospital_signup, name='signup'),
    path('login/', auth_views.hospital_login, name='login'),
    path('logout/', auth_views.hospital_logout, name='logout'),
    path('my-api-token/', auth_views.my_api_token, name='my_api_token'),
]