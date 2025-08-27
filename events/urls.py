from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Main Views
    path('', views.events_dashboard, name='events_dashboard'),
    path('list/', views.events_list, name='events_list'),
    path('calendar/', views.events_calendar, name='events_calendar'),
    path('categories/', views.events_categories, name='events_categories'),
    path('participants/', views.events_participants, name='events_participants'),
    path('reports/', views.events_reports, name='events_reports'),
    
    # API Endpoints
    path('api/stats/', views.events_stats_api, name='events_stats_api'),
    path('api/events/', views.events_list_api, name='events_list_api'),
    path('api/events/create/', views.event_create_api, name='event_create_api'),
    path('api/events/<int:event_id>/', views.event_detail_api, name='event_detail_api'),
    path('api/events/<int:event_id>/update/', views.event_update_api, name='event_update_api'),
    path('api/events/<int:event_id>/delete/', views.event_delete_api, name='event_delete_api'),
    
    # Categories API
    path('api/categories/', views.categories_list_api, name='categories_list_api'),
    path('api/categories/create/', views.category_create_api, name='category_create_api'),
    
    # Participants API
    path('api/participants/', views.participants_list_api, name='participants_list_api'),
    path('api/participants/create/', views.participant_create_api, name='participant_create_api'),
    
    # Helper APIs
    path('api/events-dropdown/', views.get_events_for_dropdown, name='get_events_for_dropdown'),
    path('api/penduduk-dropdown/', views.get_penduduk_for_dropdown, name='get_penduduk_for_dropdown'),
    
    # Export APIs
    path('api/export/excel/', views.export_events_excel, name='export_events_excel'),
    path('api/export/pdf/', views.export_events_pdf, name='export_events_pdf'),
]

