from django.urls import path
from . import views

app_name = 'village_profile'

urlpatterns = [
    # Main redirect
    path('', views.village_profile_admin, name='village_profile_admin'),
    
    # Submenu Views
    path('visi-misi/', views.visi_misi_admin, name='visi_misi'),
    path('sejarah/', views.sejarah_admin, name='sejarah'), 
    path('geografis/', views.geografis_admin, name='geografis'),
    path('peta-desa/', views.peta_desa_admin, name='peta_desa'),
    
    # VillageVision APIs
    path('vision/', views.village_vision_list_api, name='village_vision_list'),
    path('vision/<int:pk>/', views.village_vision_detail_api, name='village_vision_detail'),
    path('vision/create/', views.village_vision_create_api, name='village_vision_create'),
    path('vision/<int:pk>/update/', views.village_vision_update_api, name='village_vision_update'),
    path('vision/<int:pk>/delete/', views.village_vision_delete_api, name='village_vision_delete'),
    
    # VillageHistory APIs
    path('history/', views.village_history_list_api, name='village_history_list'),
    path('history/<int:pk>/', views.village_history_detail_api, name='village_history_detail'),
    path('history/create/', views.village_history_create_api, name='village_history_create'),
    path('history/<int:pk>/update/', views.village_history_update_api, name='village_history_update'),
    path('history/<int:pk>/delete/', views.village_history_delete_api, name='village_history_delete'),
    
    # VillageMap APIs
    path('maps/', views.village_map_list_api, name='village_map_list'),
    path('maps/<int:pk>/', views.village_map_detail_api, name='village_map_detail'),
    path('maps/create/', views.village_map_create_api, name='village_map_create'),
    path('maps/<int:pk>/delete/', views.village_map_delete_api, name='village_map_delete'),
    
    # Geography APIs
    path('geography/', views.village_geography_list_api, name='village_geography_list'),
    path('geography/save/', views.village_geography_save_api, name='village_geography_save'),
    path('geography/<int:pk>/save/', views.village_geography_save_api, name='village_geography_update'),

    # Statistics API
    path('stats/', views.village_profile_stats_api, name='village_profile_stats'),
]