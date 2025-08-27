from django.contrib import admin
from .models import Dusun, Lorong, Penduduk, DisabilitasType, DisabilitasData, ReligionReference


@admin.register(Dusun)
class DusunAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'area_size', 'population_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Lorong)
class LorongAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'dusun', 'length', 'house_count', 'is_active')
    list_filter = ('dusun', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'dusun__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Penduduk)
class PendudukAdmin(admin.ModelAdmin):
    list_display = ('name', 'nik', 'gender', 'birth_date', 'age', 'dusun', 'is_active')
    list_filter = ('gender', 'marital_status', 'religion', 'dusun', 'is_active', 'created_at')
    search_fields = ('name', 'nik', 'address')
    readonly_fields = ('created_at', 'updated_at', 'age')
    date_hierarchy = 'birth_date'

    def age(self, obj):
        return obj.age
    age.short_description = 'Umur'


@admin.register(DisabilitasType)
class DisabilitasTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DisabilitasData)
class DisabilitasDataAdmin(admin.ModelAdmin):
    list_display = ('penduduk', 'disability_type', 'severity', 'needs_assistance', 'is_active')
    list_filter = ('disability_type', 'severity', 'needs_assistance', 'is_active', 'created_at')
    search_fields = ('penduduk__name', 'penduduk__nik', 'disability_type__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ReligionReference)
class ReligionReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at', 'updated_at')
