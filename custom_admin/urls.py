from django.urls import path, include
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Authentication
    path('login/', views.admin_login_view, name='login'),
    path('logout/', views.admin_logout_view, name='logout'),
    
    # Main dashboard
    path('', views.admin_dashboard, name='dashboard'),
    
    # API endpoints
    path('api/dashboard-stats/', views.dashboard_stats_api, name='dashboard_stats_api'),
    path('api/recent-activities/', views.recent_activities_api, name='recent_activities_api'),
    path('api/system-info/', views.system_info_api, name='system_info_api'),
    path('api/search/', views.search_global, name='search_global'),
    
    # Module views
    path('module/<str:module_name>/', views.module_view, name='module_view'),
    
    # Profile and settings
    path('profile/', views.admin_profile, name='profile'),
    path('settings/', views.admin_settings, name='settings'),
    
    # Include API URLs from each app
    path('api/core/', include('core.urls')),
    path('api/references/', include('references.urls')),
    path('api/village_profile/', include('village_profile.urls')),
    path('api/posyandu/', include('posyandu.urls')),
    path('api/organization/', include('organization.urls')),
    path('api/news/', include('news.urls')),
    path('api/letters/', include('letters.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/business/', include('business.urls')),
    path('api/beneficiaries/', include('beneficiaries.urls')),
]