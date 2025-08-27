from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Core module view
    path('', views.core_module_view, name='core_module'),
    
    # Statistics API
    path('stats/', views.core_stats_api, name='core_stats'),
    
    # CustomUser CRUD API endpoints
    path('users/', views.users_list_api, name='users_list'),
    path('users/<int:user_id>/', views.user_detail_api, name='user_detail'),
    path('users/create/', views.user_create_api, name='user_create'),
    path('users/<int:user_id>/update/', views.user_update_api, name='user_update'),
    path('users/<int:user_id>/delete/', views.user_delete_api, name='user_delete'),
    
    # UMKMBusiness CRUD API endpoints
    path('umkm/', views.umkm_list_api, name='umkm_list'),
    path('umkm/<int:umkm_id>/', views.umkm_detail_api, name='umkm_detail'),
    path('umkm/create/', views.umkm_create_api, name='umkm_create'),
    path('umkm/<int:umkm_id>/update/', views.umkm_update_api, name='umkm_update'),
    path('umkm/<int:umkm_id>/delete/', views.umkm_delete_api, name='umkm_delete'),
    
    # SystemSettings CRUD API endpoints
    path('settings/', views.system_settings_list_api, name='system_settings_list'),
    path('settings/<int:setting_id>/', views.system_setting_detail_api, name='system_setting_detail'),
    path('settings/create/', views.system_setting_create_api, name='system_setting_create'),
    path('settings/<int:setting_id>/update/', views.system_setting_update_api, name='system_setting_update'),
    path('settings/<int:setting_id>/delete/', views.system_setting_delete_api, name='system_setting_delete'),
    
    # WhatsAppBotConfig CRUD API endpoints
    path('whatsapp/', views.whatsapp_config_list_api, name='whatsapp_config_list'),
    path('whatsapp/<int:config_id>/', views.whatsapp_config_detail_api, name='whatsapp_config_detail'),
    path('whatsapp/create/', views.whatsapp_config_create_api, name='whatsapp_config_create'),
    path('whatsapp/<int:config_id>/update/', views.whatsapp_config_update_api, name='whatsapp_config_update'),
    path('whatsapp/<int:config_id>/delete/', views.whatsapp_config_delete_api, name='whatsapp_config_delete'),
    
    # Helper APIs
    path('business-types/', views.business_types_dropdown_api, name='business_types_dropdown'),
]