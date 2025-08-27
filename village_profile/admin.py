from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import VillageVision, VillageHistory, VillageMap, VillageGeography, GoogleMapsEmblem


@admin.register(VillageVision)
class VillageVisionAdmin(admin.ModelAdmin):
    list_display = ['title', 'effective_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'effective_date', 'created_at']
    search_fields = ['title', 'vision_text', 'mission_text']
    date_hierarchy = 'effective_date'
    ordering = ['-effective_date']
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('title', 'effective_date', 'is_active')
        }),
        ('Visi & Misi', {
            'fields': ('vision_text', 'mission_text')
        }),
        ('Deskripsi Tambahan', {
            'fields': ('description',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['activate_vision', 'deactivate_vision']
    
    def activate_vision(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} visi misi berhasil diaktifkan.")
    activate_vision.short_description = "Aktifkan visi misi terpilih"
    
    def deactivate_vision(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} visi misi berhasil dinonaktifkan.")
    deactivate_vision.short_description = "Nonaktifkan visi misi terpilih"


@admin.register(VillageHistory)
class VillageHistoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'period_display', 'is_featured', 'is_active', 'image_preview']
    list_filter = ['is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'content', 'period_start', 'period_end']
    ordering = ['period_start']
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('title', 'content')
        }),
        ('Periode Sejarah', {
            'fields': ('period_start', 'period_end')
        }),
        ('Media & Status', {
            'fields': ('historical_image', 'is_featured', 'is_active')
        })
    )
    
    def period_display(self, obj):
        if obj.period_start and obj.period_end:
            return f"{obj.period_start} - {obj.period_end}"
        elif obj.period_start:
            return f"Sejak {obj.period_start}"
        return "Periode tidak ditentukan"
    period_display.short_description = "Periode"
    
    def image_preview(self, obj):
        if obj.historical_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;"/>',
                obj.historical_image.url
            )
        return "Tidak ada gambar"
    image_preview.short_description = "Preview Gambar"
    
    actions = ['mark_as_featured', 'unmark_as_featured']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} sejarah berhasil ditandai sebagai unggulan.")
    mark_as_featured.short_description = "Tandai sebagai sejarah unggulan"
    
    def unmark_as_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} sejarah berhasil dihapus dari unggulan.")
    unmark_as_featured.short_description = "Hapus dari sejarah unggulan"


@admin.register(VillageMap)
class VillageMapAdmin(admin.ModelAdmin):
    list_display = ['title', 'map_type', 'coordinates_display', 'zoom_level', 'is_active', 'map_preview']
    list_filter = ['map_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['map_type', 'title']
    
    fieldsets = (
        ('Informasi Peta', {
            'fields': ('title', 'map_type', 'description')
        }),
        ('File Peta', {
            'fields': ('map_image', 'map_file')
        }),
        ('Koordinat & Zoom', {
            'fields': ('coordinates_center_lat', 'coordinates_center_lng', 'zoom_level')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )
    
    def coordinates_display(self, obj):
        if obj.coordinates_center_lat and obj.coordinates_center_lng:
            return f"{obj.coordinates_center_lat}, {obj.coordinates_center_lng}"
        return "Koordinat tidak diset"
    coordinates_display.short_description = "Koordinat"
    
    def map_preview(self, obj):
        if obj.map_image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;"/>',
                obj.map_image.url
            )
        return "Tidak ada gambar"
    map_preview.short_description = "Preview Peta"
    
    actions = ['activate_maps', 'deactivate_maps']
    
    def activate_maps(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} peta berhasil diaktifkan.")
    activate_maps.short_description = "Aktifkan peta terpilih"
    
    def deactivate_maps(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} peta berhasil dinonaktifkan.")
    deactivate_maps.short_description = "Nonaktifkan peta terpilih"


@admin.register(VillageGeography)
class VillageGeographyAdmin(admin.ModelAdmin):
    list_display = ['geography_summary', 'total_area', 'altitude_range', 'temperature_range', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['climate_type', 'boundaries_north', 'boundaries_south', 'boundaries_east', 'boundaries_west']
    
    fieldsets = (
        ('Luas Wilayah', {
            'fields': ('total_area', 'agricultural_area', 'residential_area', 'forest_area', 'water_area')
        }),
        ('Topografi', {
            'fields': ('altitude_min', 'altitude_max')
        }),
        ('Iklim', {
            'fields': ('climate_type', 'rainfall_average', 'temperature_min', 'temperature_max')
        }),
        ('Batas Wilayah', {
            'fields': ('boundaries_north', 'boundaries_south', 'boundaries_east', 'boundaries_west')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )
    
    def geography_summary(self, obj):
        return f"Geografi Desa - {obj.total_area} Ha"
    geography_summary.short_description = "Ringkasan"
    
    def altitude_range(self, obj):
        if obj.altitude_min and obj.altitude_max:
            return f"{obj.altitude_min} - {obj.altitude_max} mdpl"
        elif obj.altitude_min:
            return f"Min: {obj.altitude_min} mdpl"
        elif obj.altitude_max:
            return f"Max: {obj.altitude_max} mdpl"
        return "Tidak diset"
    altitude_range.short_description = "Ketinggian"
    
    def temperature_range(self, obj):
        if obj.temperature_min and obj.temperature_max:
            return f"{obj.temperature_min}°C - {obj.temperature_max}°C"
        return "Tidak diset"
    temperature_range.short_description = "Suhu"


@admin.register(GoogleMapsEmblem)
class GoogleMapsEmblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'coordinates_display', 'emblem_size', 'is_visible', 'is_active', 'maps_link']
    list_filter = ['emblem_size', 'is_visible', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informasi Emblem', {
            'fields': ('title', 'description')
        }),
        ('Koordinat Google Maps', {
            'fields': ('latitude', 'longitude', 'zoom_level')
        }),
        ('Pengaturan Emblem', {
            'fields': ('emblem_size',)
        }),
        ('Status & Visibilitas', {
            'fields': ('is_active', 'is_visible')
        })
    )
    
    def coordinates_display(self, obj):
        return obj.coordinates_display
    coordinates_display.short_description = "Koordinat"
    
    def maps_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank" style="color: #007cba; text-decoration: none;">🗺️ Buka di Google Maps</a>',
            obj.google_maps_url
        )
    maps_link.short_description = "Link Google Maps"
    
    actions = ['show_emblem', 'hide_emblem']
    
    def show_emblem(self, request, queryset):
        queryset.update(is_visible=True)
        self.message_user(request, f"{queryset.count()} emblem berhasil ditampilkan.")
    show_emblem.short_description = "Tampilkan emblem di peta"
    
    def hide_emblem(self, request, queryset):
        queryset.update(is_visible=False)
        self.message_user(request, f"{queryset.count()} emblem berhasil disembunyikan.")
    hide_emblem.short_description = "Sembunyikan emblem dari peta"


# Kustomisasi Admin Site
admin.site.site_header = "Admin Profil Desa Pulosarok"
admin.site.site_title = "Profil Desa Admin"
admin.site.index_title = "Kelola Data Profil Desa"