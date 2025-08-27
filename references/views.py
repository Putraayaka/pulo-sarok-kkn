from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from datetime import date, timedelta
import json
import pandas as pd
import io
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from .models import Penduduk, Dusun, Lorong, DisabilitasType, DisabilitasData, ReligionReference, Family
from .forms import PendudukForm, DusunForm, LorongForm, DisabilitasTypeForm, DisabilitasDataForm, FamilyForm

def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_admin)
def references_admin(request):
    """Main references admin view"""
    context = {
        'page_title': 'Data Referensi',
        'page_subtitle': 'Kelola data penduduk dan referensi desa'
    }
    return render(request, 'admin/modules/references/index.html', context)

# Penduduk Views
@login_required
@user_passes_test(is_admin)
def penduduk_list_api(request):
    """API endpoint for penduduk list with pagination and search"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        search = request.GET.get('search', '').strip()
        
        queryset = Penduduk.objects.all()
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(nik__icontains=search) |
                Q(birth_place__icontains=search)
            )
        
        queryset = queryset.order_by('-created_at')
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': p.id,
                    'name': p.name,
                    'nik': p.nik,
                    'gender': p.get_gender_display(),
                    'birth_place': p.birth_place,
                    'birth_date': p.birth_date.strftime('%d/%m/%Y') if p.birth_date else '',
                    'dusun': p.dusun.name if p.dusun else '',
                    'lorong': p.lorong.name if p.lorong else '',
                    'marital_status': p.get_marital_status_display(),
                    'religion': p.religion,
                    'age': p.age,
                    'created_at': p.created_at.strftime('%d/%m/%Y %H:%M') if hasattr(p, 'created_at') else ''
                } for p in page_obj
            ],
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous()
            }
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Admin Views
@login_required
@user_passes_test(is_admin)
def dusun_admin(request):
    """Dusun admin view"""
    context = {
        'page_title': 'Kelola Dusun',
        'page_subtitle': 'Kelola data dusun'
    }
    return render(request, 'admin/modules/references/dusun.html', context)

@login_required
@user_passes_test(is_admin)
def lorong_admin(request):
    """Lorong admin view"""
    context = {
        'page_title': 'Kelola Lorong',
        'page_subtitle': 'Kelola data lorong'
    }
    return render(request, 'admin/modules/references/lorong.html', context)

@login_required
@user_passes_test(is_admin)
def penduduk_admin(request):
    """Penduduk admin view"""
    context = {
        'page_title': 'Kelola Penduduk',
        'page_subtitle': 'Kelola data penduduk'
    }
    return render(request, 'admin/modules/references/penduduk.html', context)

@login_required
@user_passes_test(is_admin)
def disabilitas_admin(request):
    """Disabilitas admin view"""
    context = {
        'page_title': 'Kelola Disabilitas',
        'page_subtitle': 'Kelola data disabilitas'
    }
    return render(request, 'admin/modules/references/disabilitas.html', context)

# Statistics API
@login_required
def references_stats_api(request):
    """API for references statistics"""
    try:
        from django.db.models import Count, Q
        from datetime import datetime, timedelta
        
        # Basic stats
        total_penduduk = Penduduk.objects.count()
        total_dusun = Dusun.objects.count()
        total_lorong = Lorong.objects.count()
        total_disabilitas = DisabilitasData.objects.count()
        
        # Demographics
        male_count = Penduduk.objects.filter(gender='L').count()
        female_count = Penduduk.objects.filter(gender='P').count()
        
        # Age groups calculation
        from datetime import date
        today = date.today()
        
        anak_count = 0
        dewasa_count = 0
        lansia_count = 0
        
        for penduduk in Penduduk.objects.all():
            age = today.year - penduduk.birth_date.year - ((today.month, today.day) < (penduduk.birth_date.month, penduduk.birth_date.day))
            if age < 18:
                anak_count += 1
            elif age < 60:
                dewasa_count += 1
            else:
                lansia_count += 1
        
        # Recent activity (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        new_penduduk = Penduduk.objects.filter(created_at__gte=thirty_days_ago).count()
        new_disabilitas = DisabilitasData.objects.filter(created_at__gte=thirty_days_ago).count()
        
        # Population by dusun
        population_by_dusun = list(Penduduk.objects.values('dusun__name').annotate(count=Count('id')).order_by('-count'))
        
        # Disability by type
        disability_by_type = list(DisabilitasData.objects.values('disability_type__name').annotate(count=Count('id')).order_by('-count'))
        
        # Religion distribution
        religion_distribution = list(Penduduk.objects.values('religion').annotate(count=Count('id')).order_by('-count'))
        
        # Education distribution
        education_distribution = list(Penduduk.objects.values('education').annotate(count=Count('id')).order_by('-count'))
        
        stats = {
            'basic_stats': {
                'total_penduduk': total_penduduk,
                'total_dusun': total_dusun,
                'total_lorong': total_lorong,
                'total_disabilitas': total_disabilitas
            },
            'demographics': {
                'male_count': male_count,
                'female_count': female_count,
                'age_groups': {
                    'anak': anak_count,
                    'dewasa': dewasa_count,
                    'lansia': lansia_count
                }
            },
            'recent_activity': {
                'new_penduduk': new_penduduk,
                'new_disabilitas': new_disabilitas
            },
            'population_by_dusun': population_by_dusun,
            'disability': {
                'by_type': disability_by_type
            },
            'distributions': {
                'religion': religion_distribution,
                'education': education_distribution
            }
        }
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Export/Import APIs (placeholder)
@login_required
@user_passes_test(is_admin)
def export_data(request, model_type):
    """Export data API"""
    return JsonResponse({'message': f'Export {model_type} not implemented yet'})

@login_required
@user_passes_test(is_admin)
def import_data(request, model_type):
    """Import data API"""
    return JsonResponse({'message': f'Import {model_type} not implemented yet'})

@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def penduduk_create_api(request):
    """API endpoint for creating penduduk"""
    if request.method == 'GET':
        # Return form data for modal
        dusun_list = [{'id': d.id, 'name': d.name} for d in Dusun.objects.all()]
        lorong_list = [{'id': l.id, 'name': l.name} for l in Lorong.objects.all()]
        
        return JsonResponse({
            'dusun_choices': dusun_list,
            'lorong_choices': lorong_list,
            'religion_choices': [{'value': k, 'label': v} for k, v in Penduduk.RELIGION_CHOICES],
            'gender_choices': [{'value': k, 'label': v} for k, v in Penduduk.GENDER_CHOICES],
            'marital_status_choices': [{'value': k, 'label': v} for k, v in Penduduk.MARITAL_STATUS_CHOICES]
        })
    
    try:
        data = json.loads(request.body)
        form = PendudukForm(data)
        
        if form.is_valid():
            penduduk = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Data penduduk berhasil ditambahkan',
                'data': {
                    'id': penduduk.id,
                    'name': penduduk.name,
                    'nik': penduduk.nik
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "PUT", "DELETE"])
def penduduk_detail_api(request, pk):
    """API endpoint for penduduk detail, update, and delete"""
    try:
        penduduk = get_object_or_404(Penduduk, pk=pk)
        
        if request.method == 'GET':
            data = {
                'id': penduduk.id,
                'name': penduduk.name,
                'nik': penduduk.nik,
                'gender': penduduk.gender,
                'birth_place': penduduk.birth_place,
                'birth_date': penduduk.birth_date.strftime('%Y-%m-%d') if penduduk.birth_date else '',
                'dusun_id': penduduk.dusun.id if penduduk.dusun else None,
                'lorong_id': penduduk.lorong.id if penduduk.lorong else None,
                'marital_status': penduduk.marital_status,
                'religion': penduduk.religion,
                'education': penduduk.education,
                'occupation': penduduk.occupation,
                'address': penduduk.address
            }
            return JsonResponse(data)
        
        elif request.method == 'PUT':
            data = json.loads(request.body)
            form = PendudukForm(data, instance=penduduk)
            
            if form.is_valid():
                penduduk = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Data penduduk berhasil diperbarui'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
        
        elif request.method == 'DELETE':
            penduduk.delete()
            return JsonResponse({
                'success': True,
                'message': 'Data penduduk berhasil dihapus'
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Dusun Views
@login_required
@user_passes_test(is_admin)
def dusun_list_api(request):
    """API endpoint for dusun list with pagination and search"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        search = request.GET.get('search', '').strip()
        
        queryset = Dusun.objects.all()
        
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        queryset = queryset.order_by('name')
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': d.id,
                    'name': d.name,
                    'code': d.code,
                    'population_count': d.population_count,
                    'area_size': float(d.area_size) if d.area_size else 0,
                    'total_residents': d.residents.count(),
                    'is_active': d.is_active
                } for d in page_obj
            ],
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous()
            }
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def dusun_create_api(request):
    """API endpoint for creating dusun"""
    try:
        data = json.loads(request.body)
        form = DusunForm(data)
        
        if form.is_valid():
            dusun = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Data dusun berhasil ditambahkan',
                'data': {
                    'id': dusun.id,
                    'name': dusun.name
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "PUT", "DELETE"])
def dusun_detail_api(request, pk):
    """API endpoint for dusun detail, update, and delete"""
    try:
        dusun = get_object_or_404(Dusun, pk=pk)
        
        if request.method == 'GET':
            data = {
                'id': dusun.id,
                'name': dusun.name,
                'code': dusun.code,
                'description': dusun.description,
                'area_size': float(dusun.area_size) if dusun.area_size else 0,
                'population_count': dusun.population_count,
                'is_active': dusun.is_active
            }
            return JsonResponse(data)
        
        elif request.method == 'PUT':
            data = json.loads(request.body)
            form = DusunForm(data, instance=dusun)
            
            if form.is_valid():
                dusun = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Data dusun berhasil diperbarui'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
        
        elif request.method == 'DELETE':
            # Check if dusun has penduduk
            if dusun.residents.exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Tidak dapat menghapus dusun yang masih memiliki penduduk'
                }, status=400)
            
            dusun.delete()
            return JsonResponse({
                'success': True,
                'message': 'Data dusun berhasil dihapus'
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Lorong Views
@login_required
@user_passes_test(is_admin)
def lorong_list_api(request):
    """API endpoint for lorong list with pagination and search"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        search = request.GET.get('search', '').strip()
        dusun_id = request.GET.get('dusun_id')
        
        queryset = Lorong.objects.all()
        
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        if dusun_id:
            queryset = queryset.filter(dusun_id=dusun_id)
        
        queryset = queryset.select_related('dusun').order_by('dusun__name', 'name')
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': l.id,
                    'name': l.name,
                    'code': l.code,
                    'dusun': l.dusun.name if l.dusun else '',
                    'dusun_id': l.dusun.id if l.dusun else None,
                    'length': float(l.length) if l.length else 0,
                    'house_count': l.house_count,
                    'total_residents': l.residents.count(),
                    'is_active': l.is_active
                } for l in page_obj
            ],
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous()
            }
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def lorong_create_api(request):
    """API endpoint for creating lorong"""
    if request.method == 'GET':
        # Return dusun choices for form
        dusun_list = [{'id': d.id, 'name': d.name} for d in Dusun.objects.all()]
        return JsonResponse({'dusun_choices': dusun_list})
    
    try:
        data = json.loads(request.body)
        form = LorongForm(data)
        
        if form.is_valid():
            lorong = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Data lorong berhasil ditambahkan',
                'data': {
                    'id': lorong.id,
                    'name': lorong.name
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "PUT", "DELETE"])
def lorong_detail_api(request, pk):
    """API endpoint for lorong detail, update, and delete"""
    try:
        lorong = get_object_or_404(Lorong, pk=pk)
        
        if request.method == 'GET':
            data = {
                'id': lorong.id,
                'name': lorong.name,
                'code': lorong.code,
                'description': lorong.description,
                'length': float(lorong.length) if lorong.length else 0,
                'house_count': lorong.house_count,
                'dusun_id': lorong.dusun.id if lorong.dusun else None,
                'is_active': lorong.is_active
            }
            return JsonResponse(data)
        
        elif request.method == 'PUT':
            data = json.loads(request.body)
            form = LorongForm(data, instance=lorong)
            
            if form.is_valid():
                lorong = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Data lorong berhasil diperbarui'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
        
        elif request.method == 'DELETE':
            # Check if lorong has penduduk
            if lorong.residents.exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Tidak dapat menghapus lorong yang masih memiliki penduduk'
                }, status=400)
            
            lorong.delete()
            return JsonResponse({
                'success': True,
                'message': 'Data lorong berhasil dihapus'
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Statistics API
@login_required
@user_passes_test(is_admin)
def references_stats_api(request):
    """API endpoint for references statistics"""
    try:
        data = {
            'total_penduduk': Penduduk.objects.count(),
            'total_dusun': Dusun.objects.count(),
            'total_lorong': Lorong.objects.count(),
            'total_disabilitas': DisabilitasData.objects.count(),
            'penduduk_laki': Penduduk.objects.filter(gender='L').count(),
            'penduduk_perempuan': Penduduk.objects.filter(gender='P').count(),
            'penduduk_per_dusun': [
                {
                    'dusun': d.name,
                    'jumlah': d.residents.count()
                } for d in Dusun.objects.all()
            ],
            'disabilitas_per_type': [
                {
                    'type': dt.name,
                    'jumlah': DisabilitasData.objects.filter(disability_type=dt).count()
                } for dt in DisabilitasType.objects.all()
            ]
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Disabilitas Type Views
@login_required
@user_passes_test(is_admin)
def disabilitas_type_list_api(request):
    """API endpoint for disabilitas type list"""
    try:
        search = request.GET.get('search', '').strip()
        
        queryset = DisabilitasType.objects.all()
        
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        queryset = queryset.order_by('name')
        
        data = {
            'results': [
                {
                    'id': dt.id,
                    'name': dt.name,
                    'code': dt.code,
                    'description': dt.description,
                    'is_active': dt.is_active,
                    'total_cases': DisabilitasData.objects.filter(disability_type=dt).count()
                } for dt in queryset
            ]
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def disabilitas_type_create_api(request):
    """API endpoint for creating disabilitas type"""
    try:
        data = json.loads(request.body)
        form = DisabilitasTypeForm(data)
        
        if form.is_valid():
            disability_type = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Jenis disabilitas berhasil ditambahkan',
                'data': {
                    'id': disability_type.id,
                    'name': disability_type.name
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "PUT", "DELETE"])
def disabilitas_type_detail_api(request, pk):
    """API endpoint for disabilitas type detail, update, and delete"""
    try:
        disability_type = get_object_or_404(DisabilitasType, pk=pk)
        
        if request.method == 'GET':
            data = {
                'id': disability_type.id,
                'name': disability_type.name,
                'code': disability_type.code,
                'description': disability_type.description,
                'is_active': disability_type.is_active
            }
            return JsonResponse(data)
        
        elif request.method == 'PUT':
            data = json.loads(request.body)
            form = DisabilitasTypeForm(data, instance=disability_type)
            
            if form.is_valid():
                disability_type = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Jenis disabilitas berhasil diperbarui'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
        
        elif request.method == 'DELETE':
            # Check if disability type has data
            if DisabilitasData.objects.filter(disability_type=disability_type).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Tidak dapat menghapus jenis disabilitas yang masih memiliki data'
                }, status=400)
            
            disability_type.delete()
            return JsonResponse({
                'success': True,
                'message': 'Jenis disabilitas berhasil dihapus'
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Disabilitas Data Views
@login_required
@user_passes_test(is_admin)
def disabilitas_data_list_api(request):
    """API endpoint for disabilitas data list with pagination and search"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        search = request.GET.get('search', '').strip()
        
        queryset = DisabilitasData.objects.all()
        
        if search:
            queryset = queryset.filter(
                Q(penduduk__name__icontains=search) |
                Q(penduduk__nik__icontains=search) |
                Q(disability_type__name__icontains=search)
            )
        
        queryset = queryset.select_related('penduduk', 'disability_type').order_by('-created_at')
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': dd.id,
                    'penduduk_name': dd.penduduk.name,
                    'penduduk_nik': dd.penduduk.nik,
                    'disability_type': dd.disability_type.name,
                    'severity': dd.get_severity_display(),
                    'needs_assistance': dd.needs_assistance,
                    'diagnosis_date': dd.diagnosis_date.strftime('%d/%m/%Y') if dd.diagnosis_date else '',
                    'is_active': dd.is_active,
                    'created_at': dd.created_at.strftime('%d/%m/%Y %H:%M')
                } for dd in page_obj
            ],
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous()
            }
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def disabilitas_data_create_api(request):
    """API endpoint for creating disabilitas data"""
    if request.method == 'GET':
        # Return form data for modal
        penduduk_list = [{'id': p.id, 'name': p.name, 'nik': p.nik} for p in Penduduk.objects.all()]
        disability_types = [{'id': dt.id, 'name': dt.name} for dt in DisabilitasType.objects.filter(is_active=True)]
        
        return JsonResponse({
            'penduduk_choices': penduduk_list,
            'disability_type_choices': disability_types,
            'severity_choices': [{'value': k, 'label': v} for k, v in DisabilitasData.SEVERITY_CHOICES]
        })
    
    try:
        data = json.loads(request.body)
        form = DisabilitasDataForm(data)
        
        if form.is_valid():
            disability_data = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Data disabilitas berhasil ditambahkan',
                'data': {
                    'id': disability_data.id,
                    'penduduk_name': disability_data.penduduk.name
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "PUT", "DELETE"])
def disabilitas_data_detail_api(request, pk):
    """API endpoint for disabilitas data detail, update, and delete"""
    try:
        disability_data = get_object_or_404(DisabilitasData, pk=pk)
        
        if request.method == 'GET':
            data = {
                'id': disability_data.id,
                'penduduk_id': disability_data.penduduk.id,
                'disability_type_id': disability_data.disability_type.id,
                'severity': disability_data.severity,
                'description': disability_data.description,
                'diagnosis_date': disability_data.diagnosis_date.strftime('%Y-%m-%d') if disability_data.diagnosis_date else '',
                'needs_assistance': disability_data.needs_assistance,
                'is_active': disability_data.is_active
            }
            return JsonResponse(data)
        
        elif request.method == 'PUT':
            data = json.loads(request.body)
            form = DisabilitasDataForm(data, instance=disability_data)
            
            if form.is_valid():
                disability_data = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Data disabilitas berhasil diperbarui'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
        
        elif request.method == 'DELETE':
            disability_data.delete()
            return JsonResponse({
                'success': True,
                'message': 'Data disabilitas berhasil dihapus'
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Individual Admin Pages
@login_required
@user_passes_test(is_admin)
def dusun_admin(request):
    """Admin page for Dusun management"""
    context = {
        'page_title': 'Input Data Dusun',
        'page_subtitle': 'Kelola data dusun di wilayah Gampong'
    }
    return render(request, 'admin/modules/references/dusun.html', context)

@login_required
@user_passes_test(is_admin)
def lorong_admin(request):
    """Admin page for Lorong management"""
    context = {
        'page_title': 'Input Data Lorong',
        'page_subtitle': 'Kelola data lorong di setiap dusun'
    }
    return render(request, 'admin/modules/references/lorong.html', context)

@login_required
@user_passes_test(is_admin)
def penduduk_admin(request):
    """Admin page for Penduduk management"""
    context = {
        'page_title': 'Input Data Penduduk',
        'page_subtitle': 'Kelola data penduduk Gampong'
    }
    return render(request, 'admin/modules/references/penduduk.html', context)

@login_required
@user_passes_test(is_admin)
def disabilitas_admin(request):
    """Admin page for Disabilitas management"""
    context = {
        'page_title': 'Input Data Disabilitas',
        'page_subtitle': 'Kelola data penyandang disabilitas'
    }
    return render(request, 'admin/modules/references/disabilitas.html', context)

# Export/Import Functions
@login_required
@user_passes_test(is_admin)
def export_data(request, model_type):
    """Export data to Excel/CSV"""
    try:
        is_template = request.GET.get('template', 'false').lower() == 'true'
        
        if model_type == 'dusun':
            if is_template:
                # Create template with headers only
                df = pd.DataFrame(columns=['name', 'code', 'area_size', 'population_count', 'description'])
                filename = 'template_dusun.xlsx'
            else:
                # Export actual data
                queryset = Dusun.objects.all().values('name', 'code', 'area_size', 'population_count', 'description')
                df = pd.DataFrame(list(queryset))
                filename = f'data_dusun_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
                
        elif model_type == 'lorong':
            if is_template:
                df = pd.DataFrame(columns=['name', 'code', 'dusun__name', 'length', 'house_count', 'description'])
                filename = 'template_lorong.xlsx'
            else:
                queryset = Lorong.objects.select_related('dusun').values('name', 'code', 'dusun__name', 'length', 'house_count', 'description')
                df = pd.DataFrame(list(queryset))
                filename = f'data_lorong_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
                
        elif model_type == 'penduduk':
            if is_template:
                df = pd.DataFrame(columns=['nik', 'name', 'gender', 'birth_place', 'birth_date', 'religion', 'education', 'occupation', 'marital_status', 'dusun__name', 'lorong__name', 'address'])
                filename = 'template_penduduk.xlsx'
            else:
                queryset = Penduduk.objects.select_related('dusun', 'lorong').values('nik', 'name', 'gender', 'birth_place', 'birth_date', 'religion', 'education', 'occupation', 'marital_status', 'dusun__name', 'lorong__name', 'address')
                df = pd.DataFrame(list(queryset))
                filename = f'data_penduduk_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
                
        elif model_type == 'disabilitas':
            if is_template:
                df = pd.DataFrame(columns=['penduduk__nik', 'penduduk__name', 'disability_type__name', 'severity', 'description', 'diagnosis_date', 'needs_assistance'])
                filename = 'template_disabilitas.xlsx'
            else:
                queryset = DisabilitasData.objects.select_related('penduduk', 'disability_type').values('penduduk__nik', 'penduduk__name', 'disability_type__name', 'severity', 'description', 'diagnosis_date', 'needs_assistance')
                df = pd.DataFrame(list(queryset))
                filename = f'data_disabilitas_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        else:
            return JsonResponse({'error': 'Model type tidak valid'}, status=400)
        
        # Create Excel file
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def import_data(request, model_type):
    """Import data from Excel/CSV"""
    try:
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'File tidak ditemukan'}, status=400)
        
        file = request.FILES['file']
        
        if not file.name.endswith(('.xlsx', '.xls', '.csv')):
            return JsonResponse({'error': 'Format file tidak didukung'}, status=400)
        
        # Read file
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        success_count = 0
        error_count = 0
        errors = []
        
        if model_type == 'dusun':
            for index, row in df.iterrows():
                try:
                    dusun_data = {
                        'name': row.get('name', ''),
                        'code': row.get('code', ''),
                        'area_size': row.get('area_size') if pd.notna(row.get('area_size')) else None,
                        'population_count': row.get('population_count', 0),
                        'description': row.get('description', ''),
                        'is_active': True
                    }
                    
                    # Check if dusun with same code exists
                    if Dusun.objects.filter(code=dusun_data['code']).exists():
                        errors.append(f"Baris {index + 2}: Kode dusun '{dusun_data['code']}' sudah ada")
                        error_count += 1
                        continue
                    
                    form = DusunForm(dusun_data)
                    if form.is_valid():
                        form.save()
                        success_count += 1
                    else:
                        errors.append(f"Baris {index + 2}: {form.errors}")
                        error_count += 1
                        
                except Exception as e:
                    errors.append(f"Baris {index + 2}: {str(e)}")
                    error_count += 1
        
        # Prepare response
        message = f"Import selesai. Berhasil: {success_count}, Gagal: {error_count}"
        
        if error_count > 0:
            return JsonResponse({
                'success': success_count > 0,
                'message': message,
                'errors': errors[:10]  # Limit errors shown
            })
        else:
            return JsonResponse({
                'success': True,
                'message': message
            })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@user_passes_test(is_admin)
def references_stats_api(request):
    """API endpoint for dashboard statistics"""
    try:
        # Basic counts
        total_dusun = Dusun.objects.filter(is_active=True).count()
        total_lorong = Lorong.objects.filter(is_active=True).count()
        total_penduduk = Penduduk.objects.filter(is_active=True).count()
        total_disabilitas = DisabilitasData.objects.filter(is_active=True).count()
        
        # Demographics
        male_count = Penduduk.objects.filter(gender='L', is_active=True).count()
        female_count = Penduduk.objects.filter(gender='P', is_active=True).count()
        
        # Age groups
        today = date.today()
        age_groups = {
            'anak': 0,      # 0-17 tahun
            'dewasa': 0,    # 18-59 tahun  
            'lansia': 0     # 60+ tahun
        }
        
        for penduduk in Penduduk.objects.filter(is_active=True):
            age = penduduk.age
            if age <= 17:
                age_groups['anak'] += 1
            elif age <= 59:
                age_groups['dewasa'] += 1
            else:
                age_groups['lansia'] += 1
        
        # Religion distribution
        religion_stats = (Penduduk.objects
                         .filter(is_active=True)
                         .values('religion')
                         .annotate(count=Count('id'))
                         .order_by('-count'))
        
        # Education distribution
        education_stats = (Penduduk.objects
                          .filter(is_active=True, education__isnull=False)
                          .exclude(education='')
                          .values('education')
                          .annotate(count=Count('id'))
                          .order_by('-count'))
        
        # Marital status distribution
        marital_stats = (Penduduk.objects
                        .filter(is_active=True)
                        .values('marital_status')
                        .annotate(count=Count('id'))
                        .order_by('-count'))
        
        # Disability statistics
        disability_type_stats = (DisabilitasData.objects
                                .filter(is_active=True)
                                .values('disability_type__name')
                                .annotate(count=Count('id'))
                                .order_by('-count'))
        
        disability_severity_stats = (DisabilitasData.objects
                                   .filter(is_active=True)
                                   .values('severity')
                                   .annotate(count=Count('id'))
                                   .order_by('-count'))
        
        # Population by dusun
        dusun_population = (Penduduk.objects
                           .filter(is_active=True)
                           .values('dusun__name')
                           .annotate(count=Count('id'))
                           .order_by('-count'))
        
        # Recent additions (last 30 days)
        thirty_days_ago = today - timedelta(days=30)
        recent_penduduk = Penduduk.objects.filter(
            created_at__gte=thirty_days_ago,
            is_active=True
        ).count()
        
        recent_disabilitas = DisabilitasData.objects.filter(
            created_at__gte=thirty_days_ago,
            is_active=True
        ).count()
        
        # Top 5 dusun by population
        top_dusun = list(dusun_population[:5])
        
        # Format response
        response_data = {
            'basic_stats': {
                'total_dusun': total_dusun,
                'total_lorong': total_lorong,
                'total_penduduk': total_penduduk,
                'total_disabilitas': total_disabilitas
            },
            'demographics': {
                'male_count': male_count,
                'female_count': female_count,
                'age_groups': age_groups
            },
            'distributions': {
                'religion': list(religion_stats),
                'education': list(education_stats),
                'marital_status': list(marital_stats)
            },
            'disability': {
                'by_type': list(disability_type_stats),
                'by_severity': list(disability_severity_stats)
            },
            'population_by_dusun': list(dusun_population),
            'top_dusun': top_dusun,
            'recent_activity': {
                'new_penduduk': recent_penduduk,
                'new_disabilitas': recent_disabilitas
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@user_passes_test(is_admin)
def dashboard_summary_api(request):
    """Enhanced API endpoint for dashboard summary with more detailed statistics"""
    try:
        # Calculate comprehensive statistics
        stats = {
            # Basic counts
            'total_dusun': Dusun.objects.filter(is_active=True).count(),
            'total_lorong': Lorong.objects.filter(is_active=True).count(),
            'total_penduduk': Penduduk.objects.filter(is_active=True).count(),
            'total_disabilitas': DisabilitasData.objects.filter(is_active=True).count(),
            
            # Demographics
            'male_percentage': 0,
            'female_percentage': 0,
            'average_age': 0,
            
            # Recent growth (last 30 days)
            'new_residents_month': 0,
            'new_disabilities_month': 0,
            
            # Disability insights
            'disability_percentage': 0,
            'needs_assistance_count': 0,
            
            # Geographic distribution
            'avg_population_per_dusun': 0,
            'avg_houses_per_lorong': 0,
        }
        
        total_penduduk = Penduduk.objects.filter(is_active=True).count()
        
        if total_penduduk > 0:
            # Demographics calculations
            male_count = Penduduk.objects.filter(gender='L', is_active=True).count()
            female_count = Penduduk.objects.filter(gender='P', is_active=True).count()
            
            stats['male_percentage'] = round((male_count / total_penduduk) * 100, 1)
            stats['female_percentage'] = round((female_count / total_penduduk) * 100, 1)
            
            # Average age calculation
            ages = [p.age for p in Penduduk.objects.filter(is_active=True)]
            stats['average_age'] = round(sum(ages) / len(ages), 1) if ages else 0
            
            # Disability statistics
            total_disabilitas = DisabilitasData.objects.filter(is_active=True).count()
            stats['disability_percentage'] = round((total_disabilitas / total_penduduk) * 100, 1)
            stats['needs_assistance_count'] = DisabilitasData.objects.filter(
                is_active=True, 
                needs_assistance=True
            ).count()
        
        # Recent activity (last 30 days)
        thirty_days_ago = date.today() - timedelta(days=30)
        stats['new_residents_month'] = Penduduk.objects.filter(
            created_at__gte=thirty_days_ago,
            is_active=True
        ).count()
        
        stats['new_disabilities_month'] = DisabilitasData.objects.filter(
            created_at__gte=thirty_days_ago,
            is_active=True
        ).count()
        
        # Geographic averages
        active_dusun_count = Dusun.objects.filter(is_active=True).count()
        if active_dusun_count > 0:
            stats['avg_population_per_dusun'] = round(total_penduduk / active_dusun_count, 0)
        
        active_lorong_count = Lorong.objects.filter(is_active=True).count()
        if active_lorong_count > 0:
            total_houses = Lorong.objects.filter(is_active=True).aggregate(
                total=Sum('house_count')
            )['total'] or 0
            stats['avg_houses_per_lorong'] = round(total_houses / active_lorong_count, 1)
        
        return JsonResponse(stats)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Family Views
@login_required
@user_passes_test(is_admin)
def family_list_api(request):
    """API endpoint for family list with pagination and search"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        search = request.GET.get('search', '').strip()
        
        families = Family.objects.filter(is_active=True)
        
        if search:
            families = families.filter(
                Q(kk_number__icontains=search) |
                Q(head__name__icontains=search) |
                Q(head__nik__icontains=search) |
                Q(address__icontains=search)
            )
        
        # Calculate total before pagination
        total_count = families.count()
        
        # Apply pagination
        start = (page - 1) * per_page
        end = start + per_page
        families = families[start:end]
        
        # Serialize data
        family_data = []
        for family in families:
            family_data.append({
                'id': family.id,
                'kk_number': family.kk_number,
                'head_name': family.head.name,
                'head_nik': family.head.nik,
                'family_status': family.family_status,
                'total_members': family.total_members,
                'total_income': float(family.total_income) if family.total_income else None,
                'dusun': family.dusun.name,
                'lorong': family.lorong.name if family.lorong else None,
                'address': family.address,
                'phone_number': family.phone_number,
                'is_active': family.is_active,
                'created_at': family.created_at.strftime('%Y-%m-%d %H:%M:%S') if family.created_at else None,
            })
        
        # Calculate pagination info
        total_pages = (total_count + per_page - 1) // per_page
        has_previous = page > 1
        has_next = page < total_pages
        
        response_data = {
            'results': family_data,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_items': total_count,
                'total_pages': total_pages,
                'has_previous': has_previous,
                'has_next': has_next,
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def family_create_api(request):
    """API endpoint for creating family"""
    if request.method == 'GET':
        # Return form data for modal
        dusun_list = [{'id': d.id, 'name': d.name} for d in Dusun.objects.all()]
        lorong_list = [{'id': l.id, 'name': l.name} for l in Lorong.objects.all()]
        head_choices = [{'id': p.id, 'name': f"{p.name} ({p.nik})"} for p in Penduduk.objects.filter(is_active=True).order_by('name')]
        
        return JsonResponse({
            'dusun_choices': dusun_list,
            'lorong_choices': lorong_list,
            'head_choices': head_choices,
            'family_status_choices': [{'value': k, 'label': v} for k, v in Family.FAMILY_STATUS_CHOICES],
        })
    
    try:
        data = json.loads(request.body)
        form = FamilyForm(data)
        
        if form.is_valid():
            family = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Data keluarga berhasil ditambahkan',
                'data': {
                    'id': family.id,
                    'kk_number': family.kk_number,
                    'head_name': family.head.name
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET", "PUT", "DELETE"])
def family_detail_api(request, pk):
    """API endpoint for family detail, update, and delete"""
    try:
        family = get_object_or_404(Family, pk=pk)
        
        if request.method == 'GET':
            data = {
                'id': family.id,
                'kk_number': family.kk_number,
                'head_id': family.head.id if family.head else None,
                'family_status': family.family_status,
                'total_members': family.total_members,
                'total_income': float(family.total_income) if family.total_income else None,
                'address': family.address,
                'dusun_id': family.dusun.id if family.dusun else None,
                'lorong_id': family.lorong.id if family.lorong else None,
                'rt_number': family.rt_number,
                'rw_number': family.rw_number,
                'house_number': family.house_number,
                'postal_code': family.postal_code,
                'phone_number': family.phone_number,
                'is_active': family.is_active,
            }
            return JsonResponse(data)
        
        elif request.method == 'PUT':
            data = json.loads(request.body)
            form = FamilyForm(data, instance=family)
            
            if form.is_valid():
                family = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Data keluarga berhasil diperbarui'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
        
        elif request.method == 'DELETE':
            family.delete()
            return JsonResponse({
                'success': True,
                'message': 'Data keluarga berhasil dihapus'
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
