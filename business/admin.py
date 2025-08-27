from django.contrib import admin
from .models import BusinessCategory, Business, BusinessOwner, BusinessProduct, BusinessFinance


@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'business_type', 'status', 'employee_count', 'established_date')
    list_filter = ('category', 'business_type', 'status')
    search_fields = ('name', 'description', 'address')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'established_date'


@admin.register(BusinessOwner)
class BusinessOwnerAdmin(admin.ModelAdmin):
    list_display = ('owner', 'business', 'ownership_percentage', 'role', 'is_active')
    list_filter = ('is_active', 'business__business_type')
    search_fields = ('owner__nama', 'business__name', 'role')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('owner',)


@admin.register(BusinessProduct)
class BusinessProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'price', 'stock_quantity', 'is_available')
    list_filter = ('is_available', 'business__category')
    search_fields = ('name', 'description', 'business__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BusinessFinance)
class BusinessFinanceAdmin(admin.ModelAdmin):
    list_display = ('business', 'transaction_type', 'amount', 'transaction_date', 'category')
    list_filter = ('transaction_type', 'business__business_type')
    search_fields = ('business__name', 'description', 'category')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'transaction_date'
