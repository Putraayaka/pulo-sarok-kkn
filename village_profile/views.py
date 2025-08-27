from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.core.serializers import serialize
import json
from .models import VillageVision, VillageHistory, VillageMap, VillageGeography, GoogleMapsEmblem
from .forms import (
    VillageVisionForm, VillageHistoryForm, VillageMapForm, 
    VillageGeographyForm, GoogleMapsEmblemForm, VillageProfileSearchForm
)


# Dashboard Views
def village_profile_dashboard(request):
    """Dashboard utama profil desa"""
    context = {
        'vision_count': VillageVision.objects.filter(is_active=True).count(),
        'history_count': VillageHistory.objects.filter(is_active=True).count(),
        'maps_count': VillageMap.objects.filter(is_active=True).count(),
        'geography_count': VillageGeography.objects.filter(is_active=True).count(),
        'emblem_count': GoogleMapsEmblem.objects.filter(is_active=True).count(),
        'latest_vision': VillageVision.objects.filter(is_active=True).first(),
        'featured_history': VillageHistory.objects.filter(is_featured=True, is_active=True)[:3],
        'active_maps': VillageMap.objects.filter(is_active=True)[:4],
        'latest_geography': VillageGeography.objects.filter(is_active=True).first(),
        'visible_emblems': GoogleMapsEmblem.objects.filter(is_visible=True, is_active=True)[:3]
    }
    return render(request, 'admin/modules/village_profile/dashboard.html', context)


def village_profile_overview(request):
    """Halaman overview profil desa untuk publik"""
    context = {
        'current_vision': VillageVision.objects.filter(is_active=True).first(),
        'featured_histories': VillageHistory.objects.filter(is_featured=True, is_active=True)[:3],
        'geography_data': VillageGeography.objects.filter(is_active=True).first(),
        'maps_preview': VillageMap.objects.filter(is_active=True)[:2],
        'village_emblem': GoogleMapsEmblem.objects.filter(is_visible=True, is_active=True).first()
    }
    return render(request, 'admin/modules/village_profile/overview.html', context)


# Vision & Mission Views
class VillageVisionListView(ListView):
    """Daftar visi misi desa"""
    model = VillageVision
    template_name = 'admin/modules/village_profile/vision/list.html'
    context_object_name = 'visions'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = VillageVision.objects.all().order_by('-effective_date')
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(vision_text__icontains=search_query) |
                Q(mission_text__icontains=search_query)
            )
        return queryset


class VillageVisionDetailView(DetailView):
    """Detail visi misi desa"""
    model = VillageVision
    template_name = 'admin/modules/village_profile/vision/detail.html'
    context_object_name = 'vision'


@method_decorator(login_required, name='dispatch')
class VillageVisionCreateView(CreateView):
    """Tambah visi misi desa"""
    model = VillageVision
    form_class = VillageVisionForm
    template_name = 'admin/modules/village_profile/vision/form.html'
    success_url = reverse_lazy('village_profile:vision_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Visi misi desa berhasil ditambahkan!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class VillageVisionUpdateView(UpdateView):
    """Edit visi misi desa"""
    model = VillageVision
    form_class = VillageVisionForm
    template_name = 'admin/modules/village_profile/vision/form.html'
    success_url = reverse_lazy('village_profile:vision_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Visi misi desa berhasil diperbarui!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class VillageVisionDeleteView(DeleteView):
    """Hapus visi misi desa"""
    model = VillageVision
    template_name = 'admin/modules/village_profile/vision/delete.html'
    success_url = reverse_lazy('village_profile:vision_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Visi misi desa berhasil dihapus!')
        return super().delete(request, *args, **kwargs)


# History Views
class VillageHistoryListView(ListView):
    """Daftar sejarah desa"""
    model = VillageHistory
    template_name = 'admin/modules/village_profile/history/list.html'
    context_object_name = 'histories'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = VillageHistory.objects.all().order_by('period_start')
        search_query = self.request.GET.get('search')
        featured_only = self.request.GET.get('featured')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(period_start__icontains=search_query)
            )
        
        if featured_only:
            queryset = queryset.filter(is_featured=True)
            
        return queryset


class VillageHistoryDetailView(DetailView):
    """Detail sejarah desa"""
    model = VillageHistory
    template_name = 'admin/modules/village_profile/history/detail.html'
    context_object_name = 'history'


@method_decorator(login_required, name='dispatch')
class VillageHistoryCreateView(CreateView):
    """Tambah sejarah desa"""
    model = VillageHistory
    form_class = VillageHistoryForm
    template_name = 'admin/modules/village_profile/history/form.html'
    success_url = reverse_lazy('village_profile:history_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Sejarah desa berhasil ditambahkan!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class VillageHistoryUpdateView(UpdateView):
    """Edit sejarah desa"""
    model = VillageHistory
    form_class = VillageHistoryForm
    template_name = 'admin/modules/village_profile/history/form.html'
    success_url = reverse_lazy('village_profile:history_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Sejarah desa berhasil diperbarui!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class VillageHistoryDeleteView(DeleteView):
    """Hapus sejarah desa"""
    model = VillageHistory
    template_name = 'admin/modules/village_profile/history/delete.html'
    success_url = reverse_lazy('village_profile:history_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Sejarah desa berhasil dihapus!')
        return super().delete(request, *args, **kwargs)


# Maps Views
class VillageMapListView(ListView):
    """Daftar peta desa"""
    model = VillageMap
    template_name = 'admin/modules/village_profile/maps/list.html'
    context_object_name = 'maps'
    paginate_by = 8
    
    def get_queryset(self):
        queryset = VillageMap.objects.all().order_by('map_type', 'title')
        map_type = self.request.GET.get('type')
        search_query = self.request.GET.get('search')
        
        if map_type:
            queryset = queryset.filter(map_type=map_type)
            
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['map_types'] = VillageMap.MAP_TYPE_CHOICES
        return context


class VillageMapDetailView(DetailView):
    """Detail peta desa"""
    model = VillageMap
    template_name = 'admin/modules/village_profile/maps/detail.html'
    context_object_name = 'village_map'


@method_decorator(login_required, name='dispatch')
class VillageMapCreateView(CreateView):
    """Tambah peta desa"""
    model = VillageMap
    form_class = VillageMapForm
    template_name = 'admin/modules/village_profile/maps/form.html'
    success_url = reverse_lazy('village_profile:maps_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Peta desa berhasil ditambahkan!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class VillageMapUpdateView(UpdateView):
    """Edit peta desa"""
    model = VillageMap
    form_class = VillageMapForm
    template_name = 'admin/modules/village_profile/maps/form.html'
    success_url = reverse_lazy('village_profile:maps_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Peta desa berhasil diperbarui!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class VillageMapDeleteView(DeleteView):
    """Hapus peta desa"""
    model = VillageMap
    template_name = 'admin/modules/village_profile/maps/delete.html'
    success_url = reverse_lazy('village_profile:maps_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Peta desa berhasil dihapus!')
        return super().delete(request, *args, **kwargs)


# Geography Views
class VillageGeographyListView(ListView):
    """Daftar geografi desa"""
    model = VillageGeography
    template_name = 'admin/modules/village_profile/geography/list.html'
    context_object_name = 'geographies'
    paginate_by = 10


class VillageGeographyDetailView(DetailView):
    """Detail geografi desa"""
    model = VillageGeography
    template_name = 'admin/modules/village_profile/geography/detail.html'
    context_object_name = 'geography'


@method_decorator(login_required, name='dispatch')
class VillageGeographyCreateView(CreateView):
    """Tambah geografi desa"""
    model = VillageGeography
    form_class = VillageGeographyForm
    template_name = 'admin/modules/village_profile/geography/form.html'
    success_url = reverse_lazy('village_profile:geography_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Data geografi desa berhasil ditambahkan!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class VillageGeographyUpdateView(UpdateView):
    """Edit geografi desa"""
    model = VillageGeography
    form_class = VillageGeographyForm
    template_name = 'admin/modules/village_profile/geography/form.html'
    success_url = reverse_lazy('village_profile:geography_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Data geografi desa berhasil diperbarui!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class VillageGeographyDeleteView(DeleteView):
    """Hapus geografi desa"""
    model = VillageGeography
    template_name = 'admin/modules/village_profile/geography/delete.html'
    success_url = reverse_lazy('village_profile:geography_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Data geografi desa berhasil dihapus!')
        return super().delete(request, *args, **kwargs)


# Google Maps Emblem Views
class GoogleMapsEmblemListView(ListView):
    """Daftar emblem Google Maps"""
    model = GoogleMapsEmblem
    template_name = 'admin/modules/village_profile/emblem/list.html'
    context_object_name = 'emblems'
    paginate_by = 10


class GoogleMapsEmblemDetailView(DetailView):
    """Detail emblem Google Maps"""
    model = GoogleMapsEmblem
    template_name = 'admin/modules/village_profile/emblem/detail.html'
    context_object_name = 'emblem'


@method_decorator(login_required, name='dispatch')
class GoogleMapsEmblemCreateView(CreateView):
    """Tambah emblem Google Maps"""
    model = GoogleMapsEmblem
    form_class = GoogleMapsEmblemForm
    template_name = 'admin/modules/village_profile/emblem/form.html'
    success_url = reverse_lazy('village_profile:emblem_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Emblem Google Maps berhasil ditambahkan!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class GoogleMapsEmblemUpdateView(UpdateView):
    """Edit emblem Google Maps"""
    model = GoogleMapsEmblem
    form_class = GoogleMapsEmblemForm
    template_name = 'admin/modules/village_profile/emblem/form.html'
    success_url = reverse_lazy('village_profile:emblem_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Emblem Google Maps berhasil diperbarui!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class GoogleMapsEmblemDeleteView(DeleteView):
    """Hapus emblem Google Maps"""
    model = GoogleMapsEmblem
    template_name = 'admin/modules/village_profile/emblem/delete.html'
    success_url = reverse_lazy('village_profile:emblem_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Emblem Google Maps berhasil dihapus!')
        return super().delete(request, *args, **kwargs)


# API Views
def api_village_profile_stats(request):
    """API untuk statistik profil desa"""
    stats = {
        'vision_count': VillageVision.objects.filter(is_active=True).count(),
        'history_count': VillageHistory.objects.filter(is_active=True).count(),
        'maps_count': VillageMap.objects.filter(is_active=True).count(),
        'geography_count': VillageGeography.objects.filter(is_active=True).count(),
        'emblem_count': GoogleMapsEmblem.objects.filter(is_active=True).count(),
        'featured_history_count': VillageHistory.objects.filter(is_featured=True, is_active=True).count(),
        'visible_emblem_count': GoogleMapsEmblem.objects.filter(is_visible=True, is_active=True).count()
    }
    return JsonResponse(stats)


def api_village_maps_data(request):
    """API untuk data peta desa"""
    maps_data = []
    maps = VillageMap.objects.filter(is_active=True)
    
    for village_map in maps:
        maps_data.append({
            'id': village_map.id,
            'title': village_map.title,
            'type': village_map.get_map_type_display(),
            'description': village_map.description,
            'latitude': float(village_map.coordinates_center_lat) if village_map.coordinates_center_lat else None,
            'longitude': float(village_map.coordinates_center_lng) if village_map.coordinates_center_lng else None,
            'zoom_level': village_map.zoom_level,
            'image_url': village_map.map_image.url if village_map.map_image else None
        })
    
    return JsonResponse({'maps': maps_data})


def api_village_emblems_data(request):
    """API untuk data emblem Google Maps"""
    emblems_data = []
    emblems = GoogleMapsEmblem.objects.filter(is_visible=True, is_active=True)
    
    for emblem in emblems:
        emblems_data.append({
            'id': emblem.id,
            'title': emblem.title,
            'description': emblem.description,
            'latitude': float(emblem.latitude),
            'longitude': float(emblem.longitude),
            'zoom_level': emblem.zoom_level,
            'size': emblem.emblem_size,
            'google_maps_url': emblem.google_maps_url
        })
    
    return JsonResponse({'emblems': emblems_data})


def api_village_geography_data(request):
    """API untuk data geografi desa"""
    geography = VillageGeography.objects.filter(is_active=True).first()
    
    if not geography:
        return JsonResponse({'error': 'Data geografi tidak ditemukan'}, status=404)
    
    geography_data = {
        'total_area': float(geography.total_area),
        'agricultural_area': float(geography.agricultural_area) if geography.agricultural_area else 0,
        'residential_area': float(geography.residential_area) if geography.residential_area else 0,
        'forest_area': float(geography.forest_area) if geography.forest_area else 0,
        'water_area': float(geography.water_area) if geography.water_area else 0,
        'altitude_min': geography.altitude_min,
        'altitude_max': geography.altitude_max,
        'climate_type': geography.climate_type,
        'rainfall_average': float(geography.rainfall_average) if geography.rainfall_average else 0,
        'temperature_min': float(geography.temperature_min) if geography.temperature_min else 0,
        'temperature_max': float(geography.temperature_max) if geography.temperature_max else 0,
        'boundaries': {
            'north': geography.boundaries_north,
            'south': geography.boundaries_south,
            'east': geography.boundaries_east,
            'west': geography.boundaries_west
        }
    }
    
    return JsonResponse({'geography': geography_data})


def api_search_village_profile(request):
    """API untuk pencarian data profil desa"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    
    results = []
    
    if search_type in ['all', 'vision']:
        visions = VillageVision.objects.filter(
            Q(title__icontains=query) | Q(vision_text__icontains=query) | Q(mission_text__icontains=query),
            is_active=True
        )[:5]
        
        for vision in visions:
            results.append({
                'type': 'vision',
                'id': vision.id,
                'title': vision.title,
                'content': vision.vision_text[:100] + '...' if len(vision.vision_text) > 100 else vision.vision_text,
                'url': f'/village-profile/vision/{vision.id}/'
            })
    
    if search_type in ['all', 'history']:
        histories = VillageHistory.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_active=True
        )[:5]
        
        for history in histories:
            results.append({
                'type': 'history',
                'id': history.id,
                'title': history.title,
                'content': history.content[:100] + '...' if len(history.content) > 100 else history.content,
                'url': f'/village-profile/history/{history.id}/'
            })
    
    if search_type in ['all', 'maps']:
        maps = VillageMap.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            is_active=True
        )[:5]
        
        for village_map in maps:
            results.append({
                'type': 'map',
                'id': village_map.id,
                'title': village_map.title,
                'content': village_map.description[:100] + '...' if village_map.description and len(village_map.description) > 100 else village_map.description or '',
                'url': f'/village-profile/maps/{village_map.id}/'
            })
    
    return JsonResponse({'results': results, 'total': len(results)})


# Utility Views
def village_profile_search(request):
    """Halaman pencarian profil desa"""
    form = VillageProfileSearchForm(request.GET or None)
    results = []
    
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        search_type = form.cleaned_data.get('search_type')
        is_active_only = form.cleaned_data.get('is_active_only')
        
        if search_query:
            # Implementasi pencarian berdasarkan tipe
            if search_type == 'vision' or search_type == 'all':
                visions = VillageVision.objects.filter(
                    Q(title__icontains=search_query) |
                    Q(vision_text__icontains=search_query) |
                    Q(mission_text__icontains=search_query)
                )
                if is_active_only:
                    visions = visions.filter(is_active=True)
                results.extend(visions)
            
            # Tambahkan pencarian untuk model lainnya...
    
    context = {
        'form': form,
        'results': results
    }
    return render(request, 'admin/modules/village_profile/search.html', context)


def village_profile_export(request):
    """Export data profil desa"""
    export_type = request.GET.get('type', 'all')
    format_type = request.GET.get('format', 'json')
    
    data = {}
    
    if export_type in ['all', 'vision']:
        visions = VillageVision.objects.filter(is_active=True)
        data['visions'] = serialize('json', visions)
    
    if export_type in ['all', 'history']:
        histories = VillageHistory.objects.filter(is_active=True)
        data['histories'] = serialize('json', histories)
    
    if export_type in ['all', 'maps']:
        maps = VillageMap.objects.filter(is_active=True)
        data['maps'] = serialize('json', maps)
    
    if export_type in ['all', 'geography']:
        geographies = VillageGeography.objects.filter(is_active=True)
        data['geographies'] = serialize('json', geographies)
    
    if export_type in ['all', 'emblem']:
        emblems = GoogleMapsEmblem.objects.filter(is_active=True)
        data['emblems'] = serialize('json', emblems)
    
    if format_type == 'json':
        response = JsonResponse(data)
        response['Content-Disposition'] = f'attachment; filename="village_profile_{export_type}.json"'
        return response
    
    return JsonResponse({'error': 'Format tidak didukung'}, status=400)