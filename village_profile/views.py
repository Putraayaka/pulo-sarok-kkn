from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
import json

from .models import VillageVision, VillageHistory, VillageMap, VillageGeography


# Main Views for each submenu section
@login_required
def visi_misi_admin(request):
    """Visi Misi Desa admin page"""
    context = {
        'page_title': 'Visi Misi Desa',
        'page_subtitle': 'Kelola visi dan misi desa'
    }
    return render(request, 'village_profile/visi_misi.html', context)

@login_required
def sejarah_admin(request):
    """Sejarah Desa admin page"""
    context = {
        'page_title': 'Sejarah Desa',
        'page_subtitle': 'Kelola sejarah desa'
    }
    return render(request, 'village_profile/sejarah.html', context)

@login_required
def geografis_admin(request):
    """Data Geografis admin page"""
    context = {
        'page_title': 'Data Geografis',
        'page_subtitle': 'Kelola data geografis desa'
    }
    return render(request, 'village_profile/geografis.html', context)

@login_required
def peta_desa_admin(request):
    """Peta Desa admin page"""
    context = {
        'page_title': 'Kelola Peta Desa',
        'page_subtitle': 'Kelola peta dan galeri desa'
    }
    return render(request, 'village_profile/peta_desa.html', context)

@login_required
def village_profile_admin(request):
    """Main village profile admin page - redirect to visi misi"""
    from django.shortcuts import redirect
    return redirect('village_profile:visi_misi')


# Village Vision API Views
@login_required
@require_http_methods(["GET"])
def village_vision_list_api(request):
    """API to get list of village visions"""
    try:
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        queryset = VillageVision.objects.all()
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(vision_text__icontains=search) |
                Q(mission_text__icontains=search)
            )
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': item.id,
                    'title': item.title,
                    'vision_text': item.vision_text[:100] + '...' if len(item.vision_text) > 100 else item.vision_text,
                    'mission_text': item.mission_text[:100] + '...' if len(item.mission_text) > 100 else item.mission_text,
                    'effective_date': item.effective_date.strftime('%d/%m/%Y'),
                    'is_active': item.is_active,
                    'created_at': item.created_at.strftime('%d/%m/%Y %H:%M')
                }
                for item in page_obj
            ],
            'pagination': {
                'current_page': page,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def village_vision_detail_api(request, pk):
    """API to get village vision detail"""
    try:
        vision = get_object_or_404(VillageVision, pk=pk)
        
        data = {
            'id': vision.id,
            'title': vision.title,
            'vision_text': vision.vision_text,
            'mission_text': vision.mission_text,
            'description': vision.description,
            'effective_date': vision.effective_date.strftime('%Y-%m-%d'),
            'is_active': vision.is_active,
            'created_at': vision.created_at.strftime('%d/%m/%Y %H:%M'),
            'updated_at': vision.updated_at.strftime('%d/%m/%Y %H:%M')
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def village_vision_create_api(request):
    """API to create new village vision"""
    try:
        data = json.loads(request.body)
        
        vision = VillageVision.objects.create(
            title=data['title'],
            vision_text=data['vision_text'],
            mission_text=data['mission_text'],
            description=data.get('description', ''),
            effective_date=data['effective_date'],
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Visi misi berhasil ditambahkan',
            'data': {
                'id': vision.id,
                'title': vision.title
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def village_vision_update_api(request, pk):
    """API to update village vision"""
    try:
        vision = get_object_or_404(VillageVision, pk=pk)
        data = json.loads(request.body)
        
        vision.title = data['title']
        vision.vision_text = data['vision_text']
        vision.mission_text = data['mission_text']
        vision.description = data.get('description', '')
        vision.effective_date = data['effective_date']
        vision.is_active = data.get('is_active', True)
        vision.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Visi misi berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def village_vision_delete_api(request, pk):
    """API to delete village vision"""
    try:
        vision = get_object_or_404(VillageVision, pk=pk)
        vision.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Visi misi berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Village History API Views
@login_required
@require_http_methods(["GET"])
def village_history_list_api(request):
    """API to get list of village history"""
    try:
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        queryset = VillageHistory.objects.all()
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(period_start__icontains=search) |
                Q(period_end__icontains=search)
            )
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': item.id,
                    'title': item.title,
                    'content': item.content[:100] + '...' if len(item.content) > 100 else item.content,
                    'period_start': item.period_start or '-',
                    'period_end': item.period_end or '-',
                    'is_featured': item.is_featured,
                    'is_active': item.is_active,
                    'created_at': item.created_at.strftime('%d/%m/%Y %H:%M')
                }
                for item in page_obj
            ],
            'pagination': {
                'current_page': page,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'has_previous': page_obj.has_previous(),
                'has_next': page_obj.has_next(),
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def village_history_detail_api(request, pk):
    """API to get village history detail"""
    try:
        history = get_object_or_404(VillageHistory, pk=pk)
        
        data = {
            'id': history.id,
            'title': history.title,
            'content': history.content,
            'period_start': history.period_start,
            'period_end': history.period_end,
            'historical_image': history.historical_image.url if history.historical_image else None,
            'is_featured': history.is_featured,
            'is_active': history.is_active,
            'created_at': history.created_at.strftime('%d/%m/%Y %H:%M'),
            'updated_at': history.updated_at.strftime('%d/%m/%Y %H:%M')
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def village_history_create_api(request):
    """API to create new village history"""
    try:
        data = json.loads(request.body)
        
        history = VillageHistory.objects.create(
            title=data['title'],
            content=data['content'],
            period_start=data.get('period_start'),
            period_end=data.get('period_end'),
            is_featured=data.get('is_featured', False),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Sejarah desa berhasil ditambahkan',
            'data': {
                'id': history.id,
                'title': history.title
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def village_history_update_api(request, pk):
    """API to update village history"""
    try:
        history = get_object_or_404(VillageHistory, pk=pk)
        data = json.loads(request.body)
        
        history.title = data['title']
        history.content = data['content']
        history.period_start = data.get('period_start')
        history.period_end = data.get('period_end')
        history.is_featured = data.get('is_featured', False)
        history.is_active = data.get('is_active', True)
        history.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Sejarah desa berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def village_history_delete_api(request, pk):
    """API to delete village history"""
    try:
        history = get_object_or_404(VillageHistory, pk=pk)
        history.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Sejarah desa berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Village Map CRUD API Views
@login_required
@csrf_exempt
@require_http_methods(["POST"])
def village_map_create_api(request):
    """API to create new village map"""
    try:
        title = request.POST.get('title')
        map_type = request.POST.get('map_type')
        description = request.POST.get('description', '')
        map_image = request.FILES.get('map_image')
        coordinates_center_lat = request.POST.get('coordinates_center_lat')
        coordinates_center_lng = request.POST.get('coordinates_center_lng')
        zoom_level = request.POST.get('zoom_level', 15)
        is_active = request.POST.get('is_active') == 'true'
        
        if not title or not map_type or not map_image:
            return JsonResponse({'error': 'Judul, jenis peta, dan gambar wajib diisi'}, status=400)
        
        village_map = VillageMap.objects.create(
            title=title,
            map_type=map_type,
            description=description,
            map_image=map_image,
            coordinates_center_lat=coordinates_center_lat if coordinates_center_lat else None,
            coordinates_center_lng=coordinates_center_lng if coordinates_center_lng else None,
            zoom_level=int(zoom_level),
            is_active=is_active
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Peta berhasil diupload',
            'data': {
                'id': village_map.id,
                'title': village_map.title
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def village_map_delete_api(request, pk):
    """API to delete village map"""
    try:
        village_map = get_object_or_404(VillageMap, pk=pk)
        village_map.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Peta berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def village_map_list_api(request):
    """API to get list of village maps"""
    try:
        search = request.GET.get('search', '')
        map_type = request.GET.get('map_type', '')
        
        queryset = VillageMap.objects.all()
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        
        if map_type:
            queryset = queryset.filter(map_type=map_type)
        
        data = {
            'results': [
                {
                    'id': item.id,
                    'title': item.title,
                    'map_type': item.get_map_type_display(),
                    'description': item.description[:100] + '...' if item.description and len(item.description) > 100 else item.description or '-',
                    'map_image': item.map_image.url if item.map_image else None,
                    'is_active': item.is_active,
                    'created_at': item.created_at.strftime('%d/%m/%Y %H:%M')
                }
                for item in queryset
            ]
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def village_map_detail_api(request, pk):
    """API to get village map detail"""
    try:
        village_map = get_object_or_404(VillageMap, pk=pk)
        
        data = {
            'id': village_map.id,
            'title': village_map.title,
            'map_type': village_map.map_type,
            'description': village_map.description,
            'map_image': village_map.map_image.url if village_map.map_image else None,
            'map_file': village_map.map_file.url if village_map.map_file else None,
            'coordinates_center_lat': str(village_map.coordinates_center_lat) if village_map.coordinates_center_lat else None,
            'coordinates_center_lng': str(village_map.coordinates_center_lng) if village_map.coordinates_center_lng else None,
            'zoom_level': village_map.zoom_level,
            'is_active': village_map.is_active,
            'created_at': village_map.created_at.strftime('%d/%m/%Y %H:%M'),
            'updated_at': village_map.updated_at.strftime('%d/%m/%Y %H:%M')
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Village Geography API Views
@login_required
@require_http_methods(["GET"])
def village_geography_list_api(request):
    """API to get village geography data"""
    try:
        geography = VillageGeography.objects.filter(is_active=True).first()
        
        if geography:
            data = {
                'id': geography.id,
                'total_area': str(geography.total_area),
                'agricultural_area': str(geography.agricultural_area) if geography.agricultural_area else None,
                'residential_area': str(geography.residential_area) if geography.residential_area else None,
                'forest_area': str(geography.forest_area) if geography.forest_area else None,
                'water_area': str(geography.water_area) if geography.water_area else None,
                'altitude_min': geography.altitude_min,
                'altitude_max': geography.altitude_max,
                'climate_type': geography.climate_type,
                'rainfall_average': str(geography.rainfall_average) if geography.rainfall_average else None,
                'temperature_min': str(geography.temperature_min) if geography.temperature_min else None,
                'temperature_max': str(geography.temperature_max) if geography.temperature_max else None,
                'boundaries_north': geography.boundaries_north,
                'boundaries_south': geography.boundaries_south,
                'boundaries_east': geography.boundaries_east,
                'boundaries_west': geography.boundaries_west,
                'created_at': geography.created_at.strftime('%d/%m/%Y %H:%M'),
                'updated_at': geography.updated_at.strftime('%d/%m/%Y %H:%M')
            }
        else:
            data = None
        
        return JsonResponse({'data': data})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST", "PUT"])
def village_geography_save_api(request, pk=None):
    """API to create or update village geography"""
    try:
        data = json.loads(request.body)
        
        if pk:
            geography = get_object_or_404(VillageGeography, pk=pk)
        else:
            # Check if geography already exists
            geography = VillageGeography.objects.filter(is_active=True).first()
            if not geography:
                geography = VillageGeography()
        
        geography.total_area = data['total_area']
        geography.agricultural_area = data.get('agricultural_area')
        geography.residential_area = data.get('residential_area')
        geography.forest_area = data.get('forest_area')
        geography.water_area = data.get('water_area')
        geography.altitude_min = data.get('altitude_min')
        geography.altitude_max = data.get('altitude_max')
        geography.climate_type = data.get('climate_type')
        geography.rainfall_average = data.get('rainfall_average')
        geography.temperature_min = data.get('temperature_min')
        geography.temperature_max = data.get('temperature_max')
        geography.boundaries_north = data.get('boundaries_north')
        geography.boundaries_south = data.get('boundaries_south')
        geography.boundaries_east = data.get('boundaries_east')
        geography.boundaries_west = data.get('boundaries_west')
        geography.is_active = True
        geography.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Data geografi desa berhasil disimpan',
            'data': {
                'id': geography.id
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Statistics API
@login_required
@require_http_methods(["GET"])
def village_profile_stats_api(request):
    """API to get village profile statistics"""
    try:
        stats = {
            'total_visions': VillageVision.objects.count(),
            'active_visions': VillageVision.objects.filter(is_active=True).count(),
            'total_histories': VillageHistory.objects.count(),
            'featured_histories': VillageHistory.objects.filter(is_featured=True).count(),
            'total_maps': VillageMap.objects.count(),
            'active_maps': VillageMap.objects.filter(is_active=True).count(),
            'has_geography': VillageGeography.objects.filter(is_active=True).exists()
        }
        
        return JsonResponse(stats)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
