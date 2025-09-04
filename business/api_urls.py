from django.urls import path
from . import api_views, views

app_name = 'business_api'

urlpatterns = [
    # Statistics
    path('api/stats/', api_views.api_stats, name='stats'),
    
    # Businesses
    path('api/businesses/', api_views.api_businesses, name='businesses'),
    path('api/businesses/<int:business_id>/', api_views.api_business_detail, name='business_detail'),
    
    # Koperasi API - removed duplicate, using views.koperasi_api instead
    
    # BUMG API
    path('api/bumg/', api_views.api_bumg_list, name='api_bumg_list'),
    
    # UKM API
    path('api/ukm/operations/', api_views.api_ukm_operations, name='api_ukm_operations'),
    path('api/ukm/list/', api_views.api_ukm_list, name='api_ukm_list'),
    path('api/ukm/stats/', api_views.api_ukm_stats, name='api_ukm_stats'),
    
    # Aset API
    path('api/aset/', api_views.api_aset_list, name='api_aset_list'),
    
    # Layanan Jasa API
    path('api/jasa/', api_views.api_jasa_list, name='api_jasa_list'),
]