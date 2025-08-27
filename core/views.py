from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date
import json
from datetime import datetime

from .models import CustomUser, UserProfile, UMKMBusiness, WhatsAppBotConfig, SystemSettings

User = get_user_model()


@login_required
def core_module_view(request):
    """Main core module view"""
    context = {
        'page_title': 'Manajemen Sistem',
        'page_subtitle': 'Kelola pengguna, UMKM, dan konfigurasi sistem'
    }
    return render(request, 'admin/modules/core.html', context)


# Core Statistics API
@login_required
def core_stats_api(request):
    """API for core module statistics"""
    try:
        stats = {
            'total_users': CustomUser.objects.count(),
            'active_users': CustomUser.objects.filter(is_active=True).count(),
            'village_staff': CustomUser.objects.filter(is_village_staff=True).count(),
            'total_umkm': UMKMBusiness.objects.count(),
            'active_umkm': UMKMBusiness.objects.filter(is_active=True).count(),
            'system_settings': SystemSettings.objects.filter(is_active=True).count(),
            'whatsapp_configs': WhatsAppBotConfig.objects.filter(is_active=True).count(),
            'recent_users': CustomUser.objects.filter(date_joined__gte=datetime.now().replace(day=1)).count()
        }
        
        return JsonResponse({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memuat statistik: {str(e)}'
        }, status=500)


# User Management API Views
@login_required
def users_list_api(request):
    """API for users list with pagination and search"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        search = request.GET.get('search', '')
        is_active = request.GET.get('is_active', '')
        is_village_staff = request.GET.get('is_village_staff', '')
        
        queryset = CustomUser.objects.all()
        
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(position__icontains=search)
            )
        
        if is_active:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
            
        if is_village_staff:
            queryset = queryset.filter(is_village_staff=is_village_staff.lower() == 'true')
        
        queryset = queryset.order_by('-date_joined')
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'position': user.position,
                    'is_active': user.is_active,
                    'is_village_staff': user.is_village_staff,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M'),
                    'last_login': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Belum pernah login'
                }
                for user in page_obj
            ],
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memuat data pengguna: {str(e)}'
        }, status=500)


@login_required
def user_detail_api(request, user_id):
    """API for user detail"""
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        
        data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'position': user.position,
            'is_active': user.is_active,
            'is_village_staff': user.is_village_staff,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M'),
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else None,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M')
        }
        
        # Get profile if exists
        try:
            profile = user.userprofile
            data['profile'] = {
                'bio': profile.bio,
                'address': profile.address,
                'birth_date': profile.birth_date.strftime('%Y-%m-%d') if profile.birth_date else None,
                'avatar': profile.avatar.url if profile.avatar else None
            }
        except UserProfile.DoesNotExist:
            data['profile'] = None
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memuat detail pengguna: {str(e)}'
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def user_create_api(request):
    """API for creating user"""
    try:
        data = json.loads(request.body)
        
        user = CustomUser.objects.create_user(
            username=data['username'],
            email=data.get('email', ''),
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            phone_number=data.get('phone_number', ''),
            position=data.get('position', ''),
            is_village_staff=data.get('is_village_staff', False),
            is_staff=data.get('is_staff', False),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Pengguna berhasil ditambahkan',
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan pengguna: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def user_update_api(request, user_id):
    """API for updating user"""
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        data = json.loads(request.body)
        
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.position = data.get('position', user.position)
        user.is_village_staff = data.get('is_village_staff', user.is_village_staff)
        user.is_staff = data.get('is_staff', user.is_staff)
        user.is_active = data.get('is_active', user.is_active)
        
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Pengguna berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui pengguna: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def user_delete_api(request, user_id):
    """API for deleting user"""
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        
        # Prevent deleting superuser or current user
        if user.is_superuser:
            return JsonResponse({
                'success': False,
                'message': 'Tidak dapat menghapus superuser'
            }, status=400)
            
        if user.id == request.user.id:
            return JsonResponse({
                'success': False,
                'message': 'Tidak dapat menghapus akun sendiri'
            }, status=400)
        
        user.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Pengguna berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus pengguna: {str(e)}'
        }, status=400)


# UMKM Business API Views
@login_required
def umkm_list_api(request):
    """API for UMKM businesses list"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        search = request.GET.get('search', '')
        business_type = request.GET.get('business_type', '')
        is_active = request.GET.get('is_active', '')
        
        queryset = UMKMBusiness.objects.all()
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(owner_name__icontains=search) |
                Q(business_type__icontains=search) |
                Q(description__icontains=search)
            )
        
        if business_type:
            queryset = queryset.filter(business_type__icontains=business_type)
            
        if is_active:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        queryset = queryset.order_by('-created_at')
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': umkm.id,
                    'name': umkm.name,
                    'owner_name': umkm.owner_name,
                    'phone_number': umkm.phone_number,
                    'whatsapp_number': umkm.whatsapp_number,
                    'business_type': umkm.business_type,
                    'description': umkm.description[:100] + '...' if len(umkm.description) > 100 else umkm.description,
                    'address': umkm.address,
                    'is_active': umkm.is_active,
                    'whatsapp_link': umkm.whatsapp_link,
                    'created_at': umkm.created_at.strftime('%Y-%m-%d %H:%M')
                }
                for umkm in page_obj
            ],
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memuat data UMKM: {str(e)}'
        }, status=500)


@login_required
def umkm_detail_api(request, umkm_id):
    """API for UMKM business detail"""
    try:
        umkm = get_object_or_404(UMKMBusiness, id=umkm_id)
        
        data = {
            'id': umkm.id,
            'name': umkm.name,
            'owner_name': umkm.owner_name,
            'phone_number': umkm.phone_number,
            'whatsapp_number': umkm.whatsapp_number,
            'business_type': umkm.business_type,
            'description': umkm.description,
            'address': umkm.address,
            'is_active': umkm.is_active,
            'whatsapp_link': umkm.whatsapp_link,
            'created_at': umkm.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': umkm.updated_at.strftime('%Y-%m-%d %H:%M')
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memuat detail UMKM: {str(e)}'
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def umkm_create_api(request):
    """API for creating UMKM business"""
    try:
        data = json.loads(request.body)
        
        umkm = UMKMBusiness.objects.create(
            name=data['name'],
            owner_name=data['owner_name'],
            phone_number=data['phone_number'],
            whatsapp_number=data.get('whatsapp_number', ''),
            business_type=data['business_type'],
            description=data['description'],
            address=data['address'],
            is_active=data.get('is_active', True),
            whatsapp_link=data.get('whatsapp_link', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'UMKM berhasil ditambahkan',
            'data': {
                'id': umkm.id,
                'name': umkm.name,
                'owner_name': umkm.owner_name
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan UMKM: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def umkm_update_api(request, umkm_id):
    """API for updating UMKM business"""
    try:
        umkm = get_object_or_404(UMKMBusiness, id=umkm_id)
        data = json.loads(request.body)
        
        umkm.name = data.get('name', umkm.name)
        umkm.owner_name = data.get('owner_name', umkm.owner_name)
        umkm.phone_number = data.get('phone_number', umkm.phone_number)
        umkm.whatsapp_number = data.get('whatsapp_number', umkm.whatsapp_number)
        umkm.business_type = data.get('business_type', umkm.business_type)
        umkm.description = data.get('description', umkm.description)
        umkm.address = data.get('address', umkm.address)
        umkm.is_active = data.get('is_active', umkm.is_active)
        umkm.whatsapp_link = data.get('whatsapp_link', umkm.whatsapp_link)
        umkm.save()
        
        return JsonResponse({
            'success': True,
            'message': 'UMKM berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui UMKM: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def umkm_delete_api(request, umkm_id):
    """API for deleting UMKM business"""
    try:
        umkm = get_object_or_404(UMKMBusiness, id=umkm_id)
        umkm.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'UMKM berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus UMKM: {str(e)}'
        }, status=400)


# System Settings API Views
@login_required
def system_settings_list_api(request):
    """API for system settings list"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        search = request.GET.get('search', '')
        is_active = request.GET.get('is_active', '')
        
        queryset = SystemSettings.objects.all()
        
        if search:
            queryset = queryset.filter(
                Q(setting_key__icontains=search) |
                Q(setting_value__icontains=search) |
                Q(description__icontains=search)
            )
            
        if is_active:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        queryset = queryset.order_by('setting_key')
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': setting.id,
                    'setting_key': setting.setting_key,
                    'setting_value': setting.setting_value[:100] + '...' if len(setting.setting_value) > 100 else setting.setting_value,
                    'description': setting.description,
                    'is_active': setting.is_active,
                    'created_at': setting.created_at.strftime('%Y-%m-%d %H:%M'),
                    'updated_at': setting.updated_at.strftime('%Y-%m-%d %H:%M')
                }
                for setting in page_obj
            ],
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memuat pengaturan sistem: {str(e)}'
        }, status=500)


@login_required
def system_setting_detail_api(request, setting_id):
    """API for system setting detail"""
    try:
        setting = get_object_or_404(SystemSettings, id=setting_id)
        
        data = {
            'id': setting.id,
            'setting_key': setting.setting_key,
            'setting_value': setting.setting_value,
            'description': setting.description,
            'is_active': setting.is_active,
            'created_at': setting.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': setting.updated_at.strftime('%Y-%m-%d %H:%M')
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memuat detail pengaturan: {str(e)}'
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def system_setting_create_api(request):
    """API for creating system setting"""
    try:
        data = json.loads(request.body)
        
        setting = SystemSettings.objects.create(
            setting_key=data['setting_key'],
            setting_value=data['setting_value'],
            description=data.get('description', ''),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Pengaturan berhasil ditambahkan',
            'data': {
                'id': setting.id,
                'setting_key': setting.setting_key
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan pengaturan: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def system_setting_update_api(request, setting_id):
    """API for updating system setting"""
    try:
        setting = get_object_or_404(SystemSettings, id=setting_id)
        data = json.loads(request.body)
        
        setting.setting_key = data.get('setting_key', setting.setting_key)
        setting.setting_value = data.get('setting_value', setting.setting_value)
        setting.description = data.get('description', setting.description)
        setting.is_active = data.get('is_active', setting.is_active)
        setting.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Pengaturan berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui pengaturan: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def system_setting_delete_api(request, setting_id):
    """API for deleting system setting"""
    try:
        setting = get_object_or_404(SystemSettings, id=setting_id)
        setting.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Pengaturan berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus pengaturan: {str(e)}'
        }, status=400)


# WhatsApp Bot Config API Views
@login_required
def whatsapp_config_list_api(request):
    """API for WhatsApp bot configurations list"""
    try:
        configs = WhatsAppBotConfig.objects.all().order_by('-created_at')
        
        data = {
            'results': [
                {
                    'id': config.id,
                    'bot_name': config.bot_name,
                    'welcome_message': config.welcome_message[:100] + '...' if len(config.welcome_message) > 100 else config.welcome_message,
                    'business_hours_start': config.business_hours_start.strftime('%H:%M'),
                    'business_hours_end': config.business_hours_end.strftime('%H:%M'),
                    'auto_reply_enabled': config.auto_reply_enabled,
                    'is_active': config.is_active,
                    'created_at': config.created_at.strftime('%Y-%m-%d %H:%M')
                }
                for config in configs
            ]
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memuat konfigurasi WhatsApp: {str(e)}'
        }, status=500)


@login_required
def whatsapp_config_detail_api(request, config_id):
    """API for WhatsApp bot configuration detail"""
    try:
        config = get_object_or_404(WhatsAppBotConfig, id=config_id)
        
        data = {
            'id': config.id,
            'bot_name': config.bot_name,
            'welcome_message': config.welcome_message,
            'business_hours_start': config.business_hours_start.strftime('%H:%M'),
            'business_hours_end': config.business_hours_end.strftime('%H:%M'),
            'auto_reply_enabled': config.auto_reply_enabled,
            'is_active': config.is_active,
            'created_at': config.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': config.updated_at.strftime('%Y-%m-%d %H:%M')
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memuat detail konfigurasi: {str(e)}'
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def whatsapp_config_create_api(request):
    """API for creating WhatsApp bot configuration"""
    try:
        data = json.loads(request.body)
        
        config = WhatsAppBotConfig.objects.create(
            bot_name=data['bot_name'],
            welcome_message=data['welcome_message'],
            business_hours_start=data['business_hours_start'],
            business_hours_end=data['business_hours_end'],
            auto_reply_enabled=data.get('auto_reply_enabled', True),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Konfigurasi WhatsApp berhasil ditambahkan',
            'data': {
                'id': config.id,
                'bot_name': config.bot_name
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan konfigurasi: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def whatsapp_config_update_api(request, config_id):
    """API for updating WhatsApp bot configuration"""
    try:
        config = get_object_or_404(WhatsAppBotConfig, id=config_id)
        data = json.loads(request.body)
        
        config.bot_name = data.get('bot_name', config.bot_name)
        config.welcome_message = data.get('welcome_message', config.welcome_message)
        config.business_hours_start = data.get('business_hours_start', config.business_hours_start)
        config.business_hours_end = data.get('business_hours_end', config.business_hours_end)
        config.auto_reply_enabled = data.get('auto_reply_enabled', config.auto_reply_enabled)
        config.is_active = data.get('is_active', config.is_active)
        config.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Konfigurasi WhatsApp berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui konfigurasi: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def whatsapp_config_delete_api(request, config_id):
    """API for deleting WhatsApp bot configuration"""
    try:
        config = get_object_or_404(WhatsAppBotConfig, id=config_id)
        config.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Konfigurasi WhatsApp berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus konfigurasi: {str(e)}'
        }, status=400)


# Helper API Views
@login_required
def business_types_dropdown_api(request):
    """API for business types dropdown"""
    try:
        business_types = UMKMBusiness.objects.values_list('business_type', flat=True).distinct().order_by('business_type')
        
        data = {
            'business_types': [
                {'value': bt, 'label': bt}
                for bt in business_types if bt
            ]
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memuat jenis bisnis: {str(e)}'
        }, status=500)
