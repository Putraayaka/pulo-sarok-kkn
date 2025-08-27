from django.urls import path
from . import views

app_name = 'references'

urlpatterns = [
    # References module view
    path('', views.references_admin, name='references_admin'),
    
    # Individual admin pages
    path('admin/dusun/', views.dusun_admin, name='dusun_admin'),
    path('admin/lorong/', views.lorong_admin, name='lorong_admin'),
    path('admin/penduduk/', views.penduduk_admin, name='penduduk_admin'),
    path('admin/disabilitas/', views.disabilitas_admin, name='disabilitas_admin'),
    
    # Statistics API
    path('stats/', views.references_stats_api, name='references_stats'),
    path('dashboard-summary/', views.dashboard_summary_api, name='dashboard_summary'),
    
    # Export/Import APIs
    path('export/<str:model_type>/', views.export_data, name='export_data'),
    path('import/<str:model_type>/', views.import_data, name='import_data'),
    
    # Penduduk APIs
    path('api/penduduk/', views.penduduk_list_api, name='penduduk_list'),
    path('api/penduduk/<int:pk>/', views.penduduk_detail_api, name='penduduk_detail'),
    path('api/penduduk/create/', views.penduduk_create_api, name='penduduk_create'),
    
    # Dusun APIs
    path('api/dusun/', views.dusun_list_api, name='dusun_list'),
    path('api/dusun/<int:pk>/', views.dusun_detail_api, name='dusun_detail'),
    path('api/dusun/create/', views.dusun_create_api, name='dusun_create'),
    
    # Lorong APIs
    path('api/lorong/', views.lorong_list_api, name='lorong_list'),
    path('api/lorong/<int:pk>/', views.lorong_detail_api, name='lorong_detail'),
    path('api/lorong/create/', views.lorong_create_api, name='lorong_create'),
    
    # Disabilitas Type APIs
    path('api/disabilitas-type/', views.disabilitas_type_list_api, name='disabilitas_type_list'),
    path('api/disabilitas-type/<int:pk>/', views.disabilitas_type_detail_api, name='disabilitas_type_detail'),
    path('api/disabilitas-type/create/', views.disabilitas_type_create_api, name='disabilitas_type_create'),
    
    # Disabilitas Data APIs
    path('api/disabilitas-data/', views.disabilitas_data_list_api, name='disabilitas_data_list'),
    path('api/disabilitas-data/<int:pk>/', views.disabilitas_data_detail_api, name='disabilitas_data_detail'),
    path('api/disabilitas-data/create/', views.disabilitas_data_create_api, name='disabilitas_data_create'),
]