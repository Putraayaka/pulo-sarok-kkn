from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    EventCategory, Event, EventParticipant, EventRegistration, 
    EventFeedback, EventSchedule, EventDocument
)


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'start_date', 'end_date', 'location', 
        'status', 'priority', 'current_participants', 'max_participants', 
        'is_featured', 'created_at'
    ]
    list_filter = [
        'status', 'priority', 'category', 'is_featured', 'is_free', 
        'start_date', 'created_at'
    ]
    search_fields = ['title', 'description', 'location', 'contact_person']
    list_editable = ['status', 'priority', 'is_featured']
    readonly_fields = ['slug', 'views_count', 'rating', 'total_ratings', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('title', 'slug', 'category', 'description', 'short_description')
        }),
        ('Waktu dan Tanggal', {
            'fields': ('start_date', 'end_date', 'start_time', 'end_time')
        }),
        ('Lokasi', {
            'fields': ('location', 'address', 'latitude', 'longitude')
        }),
        ('Kapasitas dan Pendaftaran', {
            'fields': ('max_participants', 'current_participants', 'allow_registration', 'registration_deadline')
        }),
        ('Biaya dan Persyaratan', {
            'fields': ('is_free', 'cost', 'requirements')
        }),
        ('Kontak', {
            'fields': ('contact_person', 'contact_phone', 'contact_email')
        }),
        ('Status dan Prioritas', {
            'fields': ('status', 'priority')
        }),
        ('Media', {
            'fields': ('featured_image', 'gallery_images')
        }),
        ('Tambahan', {
            'fields': ('tags', 'notes', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('views_count', 'rating', 'total_ratings', 'published_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'created_by')


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = [
        'event', 'participant', 'status', 'registration_source', 
        'registration_date', 'payment_status', 'check_in_time'
    ]
    list_filter = [
        'status', 'registration_source', 'payment_status', 
        'registration_date', 'event__category'
    ]
    search_fields = ['event__title', 'participant__nama', 'phone', 'email']
    readonly_fields = ['registration_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Event dan Peserta', {
            'fields': ('event', 'participant')
        }),
        ('Pendaftaran', {
            'fields': ('registration_source', 'status', 'registration_date')
        }),
        ('Informasi Tambahan', {
            'fields': ('phone', 'email', 'emergency_contact', 'emergency_phone')
        }),
        ('Kebutuhan Khusus', {
            'fields': ('special_needs', 'dietary_restrictions')
        }),
        ('Kehadiran', {
            'fields': ('check_in_time', 'check_out_time')
        }),
        ('Pembayaran', {
            'fields': ('payment_status', 'payment_amount', 'payment_date')
        }),
        ('Catatan', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event', 'participant', 'created_by')


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'event', 'phone', 'email', 'status', 'registration_date'
    ]
    list_filter = ['status', 'registration_date', 'event__category']
    search_fields = ['full_name', 'phone', 'email', 'event__title']
    readonly_fields = ['registration_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Event', {
            'fields': ('event',)
        }),
        ('Informasi Pribadi', {
            'fields': ('full_name', 'phone', 'email', 'address', 'age', 'gender')
        }),
        ('Pendaftaran', {
            'fields': ('status', 'registration_date')
        }),
        ('Kebutuhan Khusus', {
            'fields': ('special_needs', 'dietary_restrictions')
        }),
        ('Catatan', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event')


@admin.register(EventFeedback)
class EventFeedbackAdmin(admin.ModelAdmin):
    list_display = [
        'event', 'participant', 'rating', 'organization_rating', 
        'venue_rating', 'content_rating', 'created_at'
    ]
    list_filter = ['rating', 'created_at', 'event__category']
    search_fields = ['event__title', 'participant__participant__nama', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Event dan Peserta', {
            'fields': ('event', 'participant')
        }),
        ('Rating dan Feedback', {
            'fields': ('rating', 'comment')
        }),
        ('Rating Detail', {
            'fields': ('organization_rating', 'venue_rating', 'content_rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event', 'participant__participant')


@admin.register(EventSchedule)
class EventScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'event', 'title', 'start_time', 'end_time', 'location', 'speaker', 'order'
    ]
    list_filter = ['event__category', 'start_time']
    search_fields = ['title', 'event__title', 'speaker', 'location']
    list_editable = ['order']
    ordering = ['event', 'order', 'start_time']
    
    fieldsets = (
        ('Event', {
            'fields': ('event',)
        }),
        ('Jadwal', {
            'fields': ('title', 'description', 'start_time', 'end_time', 'order')
        }),
        ('Lokasi dan Pembicara', {
            'fields': ('location', 'speaker')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event')


@admin.register(EventDocument)
class EventDocumentAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'event', 'document_type', 'file_size_display', 
        'download_count', 'is_public', 'uploaded_by', 'created_at'
    ]
    list_filter = ['document_type', 'is_public', 'created_at', 'event__category']
    search_fields = ['title', 'event__title', 'description']
    readonly_fields = ['file_size', 'download_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Event', {
            'fields': ('event',)
        }),
        ('Dokumen', {
            'fields': ('title', 'document_type', 'file', 'description')
        }),
        ('Metadata', {
            'fields': ('file_size', 'download_count', 'is_public')
        }),
        ('Upload', {
            'fields': ('uploaded_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event', 'uploaded_by')
    
    def file_size_display(self, obj):
        return obj.get_file_size_display()
    file_size_display.short_description = 'Ukuran File'
