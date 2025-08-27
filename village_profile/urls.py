from django.urls import path
from . import views

app_name = 'village_profile'

urlpatterns = [
    # Dashboard URLs
    path('', views.village_profile_dashboard, name='dashboard'),
    path('overview/', views.village_profile_overview, name='overview'),
    
    # Vision & Mission URLs
    path('vision/', views.VillageVisionListView.as_view(), name='vision_list'),
    path('vision/<int:pk>/', views.VillageVisionDetailView.as_view(), name='vision_detail'),
    path('vision/add/', views.VillageVisionCreateView.as_view(), name='vision_add'),
    path('vision/<int:pk>/edit/', views.VillageVisionUpdateView.as_view(), name='vision_edit'),
    path('vision/<int:pk>/delete/', views.VillageVisionDeleteView.as_view(), name='vision_delete'),
    
    # History URLs
    path('history/', views.VillageHistoryListView.as_view(), name='history_list'),
    path('history/<int:pk>/', views.VillageHistoryDetailView.as_view(), name='history_detail'),
    path('history/add/', views.VillageHistoryCreateView.as_view(), name='history_add'),
    path('history/<int:pk>/edit/', views.VillageHistoryUpdateView.as_view(), name='history_edit'),
    path('history/<int:pk>/delete/', views.VillageHistoryDeleteView.as_view(), name='history_delete'),
    
    # Maps URLs
    path('maps/', views.VillageMapListView.as_view(), name='maps_list'),
    path('maps/<int:pk>/', views.VillageMapDetailView.as_view(), name='maps_detail'),
    path('maps/add/', views.VillageMapCreateView.as_view(), name='maps_add'),
    path('maps/<int:pk>/edit/', views.VillageMapUpdateView.as_view(), name='maps_edit'),
    path('maps/<int:pk>/delete/', views.VillageMapDeleteView.as_view(), name='maps_delete'),
    
    # Geography URLs
    path('geography/', views.VillageGeographyListView.as_view(), name='geography_list'),
    path('geography/<int:pk>/', views.VillageGeographyDetailView.as_view(), name='geography_detail'),
    path('geography/add/', views.VillageGeographyCreateView.as_view(), name='geography_add'),
    path('geography/<int:pk>/edit/', views.VillageGeographyUpdateView.as_view(), name='geography_edit'),
    path('geography/<int:pk>/delete/', views.VillageGeographyDeleteView.as_view(), name='geography_delete'),
    
    # Google Maps Emblem URLs
    path('emblem/', views.GoogleMapsEmblemListView.as_view(), name='emblem_list'),
    path('emblem/<int:pk>/', views.GoogleMapsEmblemDetailView.as_view(), name='emblem_detail'),
    path('emblem/add/', views.GoogleMapsEmblemCreateView.as_view(), name='emblem_add'),
    path('emblem/<int:pk>/edit/', views.GoogleMapsEmblemUpdateView.as_view(), name='emblem_edit'),
    path('emblem/<int:pk>/delete/', views.GoogleMapsEmblemDeleteView.as_view(), name='emblem_delete'),
    
    # API URLs
    path('api/stats/', views.api_village_profile_stats, name='api_stats'),
    path('api/maps-data/', views.api_village_maps_data, name='api_maps_data'),
    path('api/emblems-data/', views.api_village_emblems_data, name='api_emblems_data'),
    path('api/geography-data/', views.api_village_geography_data, name='api_geography_data'),
    path('api/search/', views.api_search_village_profile, name='api_search'),
    
    # Utility URLs
    path('search/', views.village_profile_search, name='search'),
    path('export/', views.village_profile_export, name='export'),
]