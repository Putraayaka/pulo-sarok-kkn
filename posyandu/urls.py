from django.urls import path
from . import views

app_name = 'posyandu'

urlpatterns = [
    # Main dashboard
    path('', views.posyandu_dashboard, name='posyandu_dashboard'),
    
    # Submenu Views
    path('kader/', views.kader_admin, name='kader_admin'),
    path('ibu-hamil/', views.ibu_hamil_admin, name='ibu_hamil_admin'),
    path('balita/', views.view_balita, name='view_balita'),
    path('lansia/', views.view_lansia, name='view_lansia'),
    path('stunting/', views.stunting_admin, name='stunting_admin'),
    
    # Posyandu Location APIs
    path('api/locations/', views.posyandu_location_list, name='posyandu_location_list'),
    path('api/locations/<int:location_id>/', views.posyandu_location_detail, name='posyandu_location_detail'),
    path('api/locations/create/', views.posyandu_location_create, name='posyandu_location_create'),
    path('api/locations/<int:location_id>/update/', views.posyandu_location_update, name='posyandu_location_update'),
    path('api/locations/<int:location_id>/delete/', views.posyandu_location_delete, name='posyandu_location_delete'),
    
    # Posyandu Schedule APIs
    path('api/schedules/', views.posyandu_schedule_list, name='posyandu_schedule_list'),
    path('api/schedules/<int:schedule_id>/', views.posyandu_schedule_detail, name='posyandu_schedule_detail'),
    path('api/schedules/create/', views.posyandu_schedule_create, name='posyandu_schedule_create'),
    path('api/schedules/<int:schedule_id>/update/', views.posyandu_schedule_update, name='posyandu_schedule_update'),
    path('api/schedules/<int:schedule_id>/delete/', views.posyandu_schedule_delete, name='posyandu_schedule_delete'),
    
    # Posyandu Stats
    path('api/stats/', views.posyandu_stats, name='posyandu_stats'),
    
    # Helper APIs
    path('api/locations-dropdown/', views.get_posyandu_locations, name='get_posyandu_locations'),
    path('api/residents/', views.get_residents_for_posyandu, name='get_residents_for_posyandu'),
    
    # Kader APIs
    path('api/kader/', views.kader_list_api, name='kader_list_api'),
    path('api/kader/<int:kader_id>/', views.kader_detail_api, name='kader_detail_api'),
    path('api/kader/create/', views.kader_create_api, name='kader_create_api'),
    path('api/kader/<int:kader_id>/update/', views.kader_update_api, name='kader_update_api'),
    path('api/kader/<int:kader_id>/delete/', views.kader_delete_api, name='kader_delete_api'),
    
    # Ibu Hamil APIs
    path('api/ibu-hamil/', views.ibu_hamil_list_api, name='ibu_hamil_list_api'),
    path('api/ibu-hamil/<int:ibu_id>/', views.ibu_hamil_detail_api, name='ibu_hamil_detail_api'),
    path('api/ibu-hamil/create/', views.ibu_hamil_create_api, name='ibu_hamil_create_api'),
    path('api/ibu-hamil/<int:ibu_id>/update/', views.ibu_hamil_update_api, name='ibu_hamil_update_api'),
    path('api/ibu-hamil/<int:ibu_id>/delete/', views.ibu_hamil_delete_api, name='ibu_hamil_delete_api'),
    
    # Pemeriksaan Ibu Hamil APIs
    path('api/pemeriksaan-ibu-hamil/', views.pemeriksaan_ibu_hamil_list_api, name='pemeriksaan_ibu_hamil_list_api'),
    path('api/pemeriksaan-ibu-hamil/create/', views.pemeriksaan_ibu_hamil_create_api, name='pemeriksaan_ibu_hamil_create_api'),
    
    # Balita APIs (using existing nutrition data)
    path('api/balita/', views.balita_list_api, name='balita_list_api'),
    
    # Lansia APIs (using health records)
    path('api/lansia/', views.lansia_list_api, name='lansia_list_api'),
    
    # Stunting APIs
    path('api/stunting/', views.stunting_list_api, name='stunting_list_api'),
    path('api/stunting/<int:stunting_id>/', views.stunting_detail_api, name='stunting_detail_api'),
    path('api/stunting/create/', views.stunting_create_api, name='stunting_create_api'),
    path('api/stunting/<int:stunting_id>/update/', views.stunting_update_api, name='stunting_update_api'),
    path('api/stunting/<int:stunting_id>/delete/', views.stunting_delete_api, name='stunting_delete_api'),
]