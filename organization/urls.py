from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    # Organization module views
    path('', views.organization_admin_view, name='organization_admin'),
    path('struktur/', views.struktur_organisasi_view, name='struktur_organisasi'),
    path('kategori/', views.kategori_organisasi_view, name='kategori_organisasi'),
    path('anggota/', views.data_anggota_view, name='data_anggota'),
    path('jabatan/', views.data_jabatan_view, name='data_jabatan'),
    path('periode/', views.periode_kepengurusan_view, name='periode_kepengurusan'),
    path('galeri/', views.galeri_kegiatan_view, name='galeri_kegiatan'),
    
    # OrganizationType APIs
    path('types/', views.organization_types_api, name='organizationtype_list'),
    path('types/<int:type_id>/', views.organization_type_detail_api, name='organizationtype_detail'),
    path('types/create/', views.organization_type_create_api, name='organizationtype_create'),
    path('types/<int:type_id>/update/', views.organization_type_update_api, name='organizationtype_update'),
    path('types/<int:type_id>/delete/', views.organization_type_delete_api, name='organizationtype_delete'),
    
    # Organization APIs
    path('organizations/', views.organizations_api, name='organization_list'),
    path('organizations/<int:org_id>/', views.organization_detail_api, name='organization_detail'),
    path('organizations/create/', views.organization_create_api, name='organization_create'),
    path('organizations/<int:org_id>/update/', views.organization_update_api, name='organization_update'),
    path('organizations/<int:org_id>/delete/', views.organization_delete_api, name='organization_delete'),
    
    # OrganizationMember APIs
    path('members/', views.organization_members_api, name='organizationmember_list'),
    path('members/<int:member_id>/', views.organization_member_detail_api, name='organizationmember_detail'),
    path('members/create/', views.organization_member_create_api, name='organizationmember_create'),
    path('members/<int:member_id>/update/', views.organization_member_update_api, name='organizationmember_update'),
    path('members/<int:member_id>/delete/', views.organization_member_delete_api, name='organizationmember_delete'),
    
    # OrganizationEvent APIs
    path('events/', views.organization_events_api, name='organizationevent_list'),
    path('events/<int:event_id>/', views.organization_event_detail_api, name='organizationevent_detail'),
    path('events/create/', views.organization_event_create_api, name='organizationevent_create'),
    path('events/<int:event_id>/update/', views.organization_event_update_api, name='organizationevent_update'),
    path('events/<int:event_id>/delete/', views.organization_event_delete_api, name='organizationevent_delete'),
    
    # Dropdown APIs
    path('types/dropdown/', views.organization_types_dropdown_api, name='organization_types_dropdown'),
    path('organizations/dropdown/', views.organizations_dropdown_api, name='organizations_dropdown'),
    
    # Kategori Organisasi API
    path('api/kategori-organisasi/', views.kategori_organisasi_api, name='kategori_organisasi_api'),
    path('api/kategori-organisasi/statistics/', views.kategori_organisasi_statistics_api, name='kategori_organisasi_statistics'),
    path('api/kategori-organisasi/create/', views.kategori_organisasi_create_api, name='kategori_organisasi_create'),
    path('api/kategori-organisasi/<int:kategori_id>/update/', views.kategori_organisasi_update_api, name='kategori_organisasi_update'),
    path('api/kategori-organisasi/<int:kategori_id>/delete/', views.kategori_organisasi_delete_api, name='kategori_organisasi_delete'),
    
    # Jabatan APIs
    path('api/jabatan/', views.jabatan_api, name='jabatan_list'),
    path('api/jabatan/statistics/', views.jabatan_statistics_api, name='jabatan_statistics'),
    path('api/jabatan/create/', views.jabatan_create_api, name='jabatan_create'),
    path('api/jabatan/<int:jabatan_id>/', views.jabatan_detail_api, name='jabatan_detail'),
    path('api/jabatan/<int:jabatan_id>/update/', views.jabatan_update_api, name='jabatan_update'),
    path('api/jabatan/<int:jabatan_id>/delete/', views.jabatan_delete_api, name='jabatan_delete'),
    path('api/jabatan/export/', views.jabatan_export_api, name='jabatan_export'),
    
    # Periode Kepengurusan APIs
    path('api/periode-kepengurusan/', views.periode_kepengurusan_api, name='periode_kepengurusan_list'),
    path('api/periode-kepengurusan/statistics/', views.periode_kepengurusan_statistics_api, name='periode_kepengurusan_statistics'),
    path('api/periode-kepengurusan/create/', views.periode_kepengurusan_create_api, name='periode_kepengurusan_create'),
    path('api/periode-kepengurusan/<int:periode_id>/update/', views.periode_kepengurusan_update_api, name='periode_kepengurusan_update'),
    path('api/periode-kepengurusan/<int:periode_id>/delete/', views.periode_kepengurusan_delete_api, name='periode_kepengurusan_delete'),
    path('api/periode-kepengurusan/export/', views.periode_kepengurusan_export_api, name='periode_kepengurusan_export'),
    
    # Anggota Organisasi APIs
    path('api/anggota-organisasi/', views.anggota_organisasi_api, name='anggota_organisasi_list'),
    path('api/anggota-organisasi/statistics/', views.anggota_organisasi_statistics_api, name='anggota_organisasi_statistics'),
    path('api/anggota-organisasi/create/', views.anggota_organisasi_create_api, name='anggota_organisasi_create'),
    path('api/anggota-organisasi/<int:anggota_id>/', views.anggota_organisasi_detail_api, name='anggota_organisasi_detail'),
    path('api/anggota-organisasi/<int:anggota_id>/update/', views.anggota_organisasi_update_api, name='anggota_organisasi_update'),
    path('api/anggota-organisasi/<int:anggota_id>/delete/', views.anggota_organisasi_delete_api, name='anggota_organisasi_delete'),
    path('api/anggota-organisasi/export/', views.anggota_organisasi_export_api, name='anggota_organisasi_export'),
    
    # Galeri Kegiatan APIs
    path('api/galeri-kegiatan/', views.galeri_kegiatan_api, name='galeri_kegiatan_list'),
    path('api/galeri-kegiatan/statistics/', views.galeri_kegiatan_statistics_api, name='galeri_kegiatan_statistics'),
    path('api/galeri-kegiatan/create/', views.galeri_kegiatan_create_api, name='galeri_kegiatan_create'),
    path('api/galeri-kegiatan/<int:galeri_id>/', views.galeri_kegiatan_detail_api, name='galeri_kegiatan_detail'),
    path('api/galeri-kegiatan/<int:galeri_id>/update/', views.galeri_kegiatan_update_api, name='galeri_kegiatan_update'),
    path('api/galeri-kegiatan/<int:galeri_id>/delete/', views.galeri_kegiatan_delete_api, name='galeri_kegiatan_delete'),
    path('api/galeri-kegiatan/export/', views.galeri_kegiatan_export_api, name='galeri_kegiatan_export'),
    
    # Struktur Organisasi APIs
    path('api/struktur-organisasi/', views.struktur_organisasi_api, name='struktur_organisasi_list'),
    path('api/struktur-organisasi/statistics/', views.struktur_organisasi_statistics_api, name='struktur_organisasi_statistics'),
    path('api/struktur-organisasi/create/', views.struktur_organisasi_create_api, name='struktur_organisasi_create'),
    path('api/struktur-organisasi/<int:struktur_id>/', views.struktur_organisasi_detail_api, name='struktur_organisasi_detail'),
    path('api/struktur-organisasi/<int:struktur_id>/update/', views.struktur_organisasi_update_api, name='struktur_organisasi_update'),
    path('api/struktur-organisasi/<int:struktur_id>/delete/', views.struktur_organisasi_delete_api, name='struktur_organisasi_delete'),
    path('api/struktur-organisasi/export/', views.struktur_organisasi_export_api, name='struktur_organisasi_export'),
    
    # Organizations API
    path('api/organizations/', views.organizations_api, name='organizations_api'),
    path('api/organizations/chart-data/', views.organizations_chart_data_api, name='organizations_chart_data'),
    
    # Statistics API
    path('api/statistics/', views.organization_statistics_api, name='organization_statistics'),
    path('statistics/', views.organization_statistics_api, name='organization_statistics_legacy')
]