from django.contrib import admin
from .models import VillageVision, VillageHistory, VillageMap, VillageGeography


@admin.register(VillageVision)
class VillageVisionAdmin(admin.ModelAdmin):
    list_display = ('title', 'effective_date', 'is_active', 'created_at')
    list_filter = ('is_active', 'effective_date')
    search_fields = ('title', 'vision_text', 'mission_text')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(VillageHistory)
class VillageHistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'period_start', 'period_end', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(VillageMap)
class VillageMapAdmin(admin.ModelAdmin):
    list_display = ('title', 'map_type', 'is_active', 'created_at')
    list_filter = ('map_type', 'is_active')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(VillageGeography)
class VillageGeographyAdmin(admin.ModelAdmin):
    list_display = ('total_area', 'climate_type', 'is_active', 'updated_at')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
