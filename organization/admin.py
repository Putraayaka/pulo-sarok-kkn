from django.contrib import admin
from .models import OrganizationType, Organization, OrganizationMember, OrganizationEvent, OrganizationDocument


@admin.register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization_type', 'leader', 'established_date', 'is_active')
    list_filter = ('organization_type', 'is_active', 'established_date')
    search_fields = ('name', 'description', 'leader__nama')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('leader',)


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ('member', 'organization', 'position', 'join_date', 'is_active')
    list_filter = ('position', 'is_active', 'organization__organization_type')
    search_fields = ('member__nama', 'organization__name')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('member',)


@admin.register(OrganizationEvent)
class OrganizationEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'event_type', 'event_date', 'is_completed')
    list_filter = ('event_type', 'is_completed', 'organization__organization_type')
    search_fields = ('title', 'description', 'organization__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'event_date'


@admin.register(OrganizationDocument)
class OrganizationDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'document_type', 'document_date', 'is_public')
    list_filter = ('document_type', 'is_public', 'organization__organization_type')
    search_fields = ('title', 'description', 'organization__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'document_date'
