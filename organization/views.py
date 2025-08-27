from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.core.files.storage import default_storage
from django.conf import settings
import json
import os
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, Alignment
from io import BytesIO

from .models import (
    OrganizationType, Organization, OrganizationMember, 
    OrganizationEvent, OrganizationDocument,
    Jabatan, PeriodeKepengurusan, AnggotaOrganisasi,
    GaleriKegiatan, StrukturOrganisasi
)
from references.models import Penduduk


@login_required
def organization_admin_view(request):
    """Main organization admin view"""
    context = {
        'page_title': 'Manajemen Organisasi',
        'page_subtitle': 'Kelola data organisasi, anggota, dan kegiatan'
    }
    return render(request, 'admin/modules/organization.html', context)


@login_required
def struktur_organisasi_view(request):
    """Struktur Organisasi view"""
    context = {
        'page_title': 'Struktur Organisasi',
        'page_subtitle': 'Kelola struktur organisasi dan diagram'
    }
    return render(request, 'admin/modules/organization/struktur_organisasi.html', context)


@login_required
def data_anggota_view(request):
    """Data Anggota view"""
    context = {
        'page_title': 'Data Anggota',
        'page_subtitle': 'Kelola data anggota organisasi'
    }
    return render(request, 'admin/modules/organization/data_anggota.html', context)


@login_required
def data_jabatan_view(request):
    """Data Jabatan view"""
    context = {
        'page_title': 'Data Jabatan',
        'page_subtitle': 'Kelola data jabatan dalam organisasi'
    }
    return render(request, 'admin/modules/organization/data_jabatan.html', context)


@login_required
def periode_kepengurusan_view(request):
    """Periode Kepengurusan view"""
    context = {
        'page_title': 'Periode Kepengurusan',
        'page_subtitle': 'Kelola periode kepengurusan organisasi'
    }
    return render(request, 'admin/modules/organization/periode_kepengurusan.html', context)


@login_required
def galeri_kegiatan_view(request):
    """Galeri Kegiatan view"""
    context = {
        'page_title': 'Galeri Kegiatan',
        'page_subtitle': 'Kelola galeri foto kegiatan organisasi'
    }
    return render(request, 'admin/modules/organization/galeri_kegiatan.html', context)


# Organization Type API Views
@login_required
@require_http_methods(["GET"])
def organization_types_api(request):
    """API for organization types list"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    search = request.GET.get('search', '')
    
    queryset = OrganizationType.objects.all()
    
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    queryset = queryset.order_by('-created_at')
    
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'results': [
            {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'is_active': item.is_active,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M'),
                'organizations_count': item.organization_set.count()
            }
            for item in page_obj
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


# Jabatan API Views
@login_required
@require_http_methods(["GET"])
def jabatan_api(request):
    """API for jabatan list"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    search = request.GET.get('search', '')
    
    queryset = Jabatan.objects.all()
    
    if search:
        queryset = queryset.filter(
            Q(nama__icontains=search) |
            Q(deskripsi__icontains=search)
        )
    
    queryset = queryset.order_by('level', 'nama')
    
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'results': [
            {
                'id': item.id,
                'nama': item.nama,
                'deskripsi': item.deskripsi,
                'level': item.level,
                'is_active': item.is_active,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for item in page_obj
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


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def jabatan_create_api(request):
    """API for creating jabatan"""
    try:
        data = json.loads(request.body)
        
        jabatan = Jabatan.objects.create(
            nama=data['nama'],
            deskripsi=data.get('deskripsi', ''),
            level=data.get('level', 1),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Jabatan berhasil ditambahkan',
            'data': {
                'id': jabatan.id,
                'nama': jabatan.nama
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan jabatan: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def jabatan_update_api(request, jabatan_id):
    """API for updating jabatan"""
    try:
        jabatan = get_object_or_404(Jabatan, id=jabatan_id)
        data = json.loads(request.body)
        
        jabatan.nama = data.get('nama', jabatan.nama)
        jabatan.deskripsi = data.get('deskripsi', jabatan.deskripsi)
        jabatan.level = data.get('level', jabatan.level)
        jabatan.is_active = data.get('is_active', jabatan.is_active)
        jabatan.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Jabatan berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui jabatan: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def jabatan_delete_api(request, jabatan_id):
    """API for deleting jabatan"""
    try:
        jabatan = get_object_or_404(Jabatan, id=jabatan_id)
        jabatan.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Jabatan berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus jabatan: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["GET"])
def jabatan_statistics_api(request):
    """API for jabatan statistics"""
    try:
        total_jabatan = Jabatan.objects.count()
        jabatan_eksekutif = Jabatan.objects.filter(level__lte=2).count()
        jabatan_struktural = Jabatan.objects.filter(level__range=(3, 5)).count()
        jabatan_anggota = Jabatan.objects.filter(level__gte=6).count()
        
        return JsonResponse({
            'total_jabatan': total_jabatan,
            'jabatan_eksekutif': jabatan_eksekutif,
            'jabatan_struktural': jabatan_struktural,
            'jabatan_anggota': jabatan_anggota
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memuat statistik jabatan: {str(e)}'
        }, status=400)


# Periode Kepengurusan API Views
@login_required
@require_http_methods(["GET"])
def periode_kepengurusan_api(request):
    """API for periode kepengurusan list"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    search = request.GET.get('search', '')
    
    queryset = PeriodeKepengurusan.objects.all()
    
    if search:
        queryset = queryset.filter(
            Q(nama__icontains=search) |
            Q(deskripsi__icontains=search)
        )
    
    queryset = queryset.order_by('-tanggal_mulai')
    
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'results': [
            {
                'id': item.id,
                'nama': item.nama,
                'deskripsi': item.deskripsi,
                'tanggal_mulai': item.tanggal_mulai.strftime('%Y-%m-%d'),
                'tanggal_selesai': item.tanggal_selesai.strftime('%Y-%m-%d'),
                'is_active': item.is_active,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for item in page_obj
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


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def periode_kepengurusan_create_api(request):
    """API for creating periode kepengurusan"""
    try:
        data = json.loads(request.body)
        
        periode = PeriodeKepengurusan.objects.create(
            nama=data['nama'],
            deskripsi=data.get('deskripsi', ''),
            tanggal_mulai=parse_date(data['tanggal_mulai']),
            tanggal_selesai=parse_date(data['tanggal_selesai']),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Periode kepengurusan berhasil ditambahkan',
            'data': {
                'id': periode.id,
                'nama': periode.nama
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan periode kepengurusan: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def periode_kepengurusan_update_api(request, periode_id):
    """API for updating periode kepengurusan"""
    try:
        periode = get_object_or_404(PeriodeKepengurusan, id=periode_id)
        data = json.loads(request.body)
        
        periode.nama = data.get('nama', periode.nama)
        periode.deskripsi = data.get('deskripsi', periode.deskripsi)
        periode.tanggal_mulai = parse_date(data['tanggal_mulai']) if data.get('tanggal_mulai') else periode.tanggal_mulai
        periode.tanggal_selesai = parse_date(data['tanggal_selesai']) if data.get('tanggal_selesai') else periode.tanggal_selesai
        periode.is_active = data.get('is_active', periode.is_active)
        periode.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Periode kepengurusan berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui periode kepengurusan: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def periode_kepengurusan_delete_api(request, periode_id):
    """API for deleting periode kepengurusan"""
    try:
        periode = get_object_or_404(PeriodeKepengurusan, id=periode_id)
        periode.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Periode kepengurusan berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus periode kepengurusan: {str(e)}'
        }, status=400)


# Anggota Organisasi API Views
@login_required
@require_http_methods(["GET"])
def anggota_organisasi_api(request):
    """API for anggota organisasi list"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    search = request.GET.get('search', '')
    organization_id = request.GET.get('organization_id', '')
    jabatan_id = request.GET.get('jabatan_id', '')
    periode_id = request.GET.get('periode_id', '')
    
    queryset = AnggotaOrganisasi.objects.select_related('penduduk', 'organization', 'jabatan', 'periode')
    
    if search:
        queryset = queryset.filter(
            Q(penduduk__nama__icontains=search) |
            Q(penduduk__nik__icontains=search) |
            Q(organization__name__icontains=search)
        )
    
    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)
    
    if jabatan_id:
        queryset = queryset.filter(jabatan_id=jabatan_id)
    
    if periode_id:
        queryset = queryset.filter(periode_id=periode_id)
    
    queryset = queryset.order_by('-created_at')
    
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'results': [
            {
                'id': item.id,
                'penduduk_nama': item.penduduk.nama,
                'penduduk_nik': item.penduduk.nik,
                'organization_name': item.organization.name,
                'jabatan_nama': item.jabatan.nama,
                'periode_nama': item.periode.nama,
                'tanggal_bergabung': item.tanggal_bergabung.strftime('%Y-%m-%d'),
                'tanggal_keluar': item.tanggal_keluar.strftime('%Y-%m-%d') if item.tanggal_keluar else None,
                'foto_profil': item.foto_profil.url if item.foto_profil else None,
                'is_active': item.is_active,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for item in page_obj
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


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def anggota_organisasi_create_api(request):
    """API for creating anggota organisasi"""
    try:
        penduduk_id = request.POST.get('penduduk_id')
        organization_id = request.POST.get('organization_id')
        jabatan_id = request.POST.get('jabatan_id')
        periode_id = request.POST.get('periode_id')
        tanggal_bergabung = request.POST.get('tanggal_bergabung')
        tanggal_keluar = request.POST.get('tanggal_keluar')
        foto_profil = request.FILES.get('foto_profil')
        is_active = request.POST.get('is_active', 'true').lower() == 'true'
        
        anggota = AnggotaOrganisasi.objects.create(
            penduduk_id=penduduk_id,
            organization_id=organization_id,
            jabatan_id=jabatan_id,
            periode_id=periode_id,
            tanggal_bergabung=parse_date(tanggal_bergabung),
            tanggal_keluar=parse_date(tanggal_keluar) if tanggal_keluar else None,
            foto_profil=foto_profil,
            is_active=is_active
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Anggota organisasi berhasil ditambahkan',
            'data': {
                'id': anggota.id,
                'nama': anggota.penduduk.nama
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan anggota organisasi: {str(e)}'
        }, status=400)


# Galeri Kegiatan API Views
@login_required
@require_http_methods(["GET"])
def galeri_kegiatan_api(request):
    """API for galeri kegiatan list"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    search = request.GET.get('search', '')
    
    queryset = GaleriKegiatan.objects.all()
    
    if search:
        queryset = queryset.filter(
            Q(judul__icontains=search) |
            Q(deskripsi__icontains=search)
        )
    
    queryset = queryset.order_by('-tanggal_kegiatan')
    
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'results': [
            {
                'id': item.id,
                'judul': item.judul,
                'deskripsi': item.deskripsi,
                'tanggal_kegiatan': item.tanggal_kegiatan.strftime('%Y-%m-%d'),
                'foto': item.foto.url if item.foto else None,
                'is_active': item.is_active,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for item in page_obj
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


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def galeri_kegiatan_create_api(request):
    """API for creating galeri kegiatan"""
    try:
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi', '')
        tanggal_kegiatan = request.POST.get('tanggal_kegiatan')
        foto = request.FILES.get('foto')
        is_active = request.POST.get('is_active', 'true').lower() == 'true'
        
        galeri = GaleriKegiatan.objects.create(
            judul=judul,
            deskripsi=deskripsi,
            tanggal_kegiatan=parse_date(tanggal_kegiatan),
            foto=foto,
            is_active=is_active
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Galeri kegiatan berhasil ditambahkan',
            'data': {
                'id': galeri.id,
                'judul': galeri.judul
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan galeri kegiatan: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["GET"])
def galeri_kegiatan_detail_api(request, galeri_id):
    """API for galeri kegiatan detail"""
    galeri = get_object_or_404(GaleriKegiatan.objects.select_related('organization'), id=galeri_id)
    
    data = {
        'id': galeri.id,
        'judul': galeri.judul,
        'deskripsi': galeri.deskripsi,
        'organization_name': galeri.organization.name if galeri.organization else None,
        'organization_id': galeri.organization.id if galeri.organization else None,
        'tanggal_kegiatan': galeri.tanggal_kegiatan.strftime('%Y-%m-%d'),
        'lokasi': galeri.lokasi,
        'fotografer': galeri.fotografer,
        'tags': galeri.tags,
        'foto': galeri.foto.url if galeri.foto else None,
        'is_active': galeri.is_active,
        'created_at': galeri.created_at.strftime('%Y-%m-%d %H:%M'),
        'updated_at': galeri.updated_at.strftime('%Y-%m-%d %H:%M')
    }
    
    return JsonResponse(data)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def galeri_kegiatan_update_api(request, galeri_id):
    """API for updating galeri kegiatan"""
    try:
        galeri = get_object_or_404(GaleriKegiatan, id=galeri_id)
        
        galeri.judul = request.POST.get('judul', galeri.judul)
        galeri.deskripsi = request.POST.get('deskripsi', galeri.deskripsi)
        
        if request.POST.get('tanggal_kegiatan'):
            galeri.tanggal_kegiatan = parse_date(request.POST.get('tanggal_kegiatan'))
        
        if request.FILES.get('foto'):
            galeri.foto = request.FILES.get('foto')
        
        galeri.is_active = request.POST.get('is_active', str(galeri.is_active)).lower() == 'true'
        galeri.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Galeri kegiatan berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui galeri kegiatan: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def galeri_kegiatan_delete_api(request, galeri_id):
    """API for deleting galeri kegiatan"""
    try:
        galeri = get_object_or_404(GaleriKegiatan, id=galeri_id)
        galeri.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Galeri kegiatan berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus galeri kegiatan: {str(e)}'
        }, status=400)


# Struktur Organisasi API Views
@login_required
@require_http_methods(["GET"])
def struktur_organisasi_api(request):
    """API for struktur organisasi list"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    search = request.GET.get('search', '')
    
    queryset = StrukturOrganisasi.objects.select_related('organization', 'periode')
    
    if search:
        queryset = queryset.filter(
            Q(nama__icontains=search) |
            Q(organization__name__icontains=search)
        )
    
    queryset = queryset.order_by('-created_at')
    
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'results': [
            {
                'id': item.id,
                'nama': item.nama,
                'organization_name': item.organization.name,
                'periode_nama': item.periode.nama,
                'diagram': item.diagram.url if item.diagram else None,
                'is_active': item.is_active,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for item in page_obj
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


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def struktur_organisasi_create_api(request):
    """API for creating struktur organisasi"""
    try:
        nama = request.POST.get('nama')
        organization_id = request.POST.get('organization_id')
        periode_id = request.POST.get('periode_id')
        diagram = request.FILES.get('diagram')
        is_active = request.POST.get('is_active', 'true').lower() == 'true'
        
        struktur = StrukturOrganisasi.objects.create(
            nama=nama,
            organization_id=organization_id,
            periode_id=periode_id,
            diagram=diagram,
            is_active=is_active
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Struktur organisasi berhasil ditambahkan',
            'data': {
                'id': struktur.id,
                'nama': struktur.nama
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan struktur organisasi: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["GET"])
def organization_types_api(request):
    """API for organization types list"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    search = request.GET.get('search', '')
    
    queryset = OrganizationType.objects.all()
    
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    queryset = queryset.order_by('-created_at')
    
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'results': [
            {
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'is_active': item.is_active,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M'),
                'organizations_count': item.organization_set.count()
            }
            for item in page_obj
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


@login_required
@require_http_methods(["GET"])
def organization_type_detail_api(request, type_id):
    """API for organization type detail"""
    org_type = get_object_or_404(OrganizationType, id=type_id)
    
    data = {
        'id': org_type.id,
        'name': org_type.name,
        'description': org_type.description,
        'is_active': org_type.is_active,
        'created_at': org_type.created_at.strftime('%Y-%m-%d %H:%M'),
        'updated_at': org_type.updated_at.strftime('%Y-%m-%d %H:%M'),
        'organizations_count': org_type.organization_set.count()
    }
    
    return JsonResponse(data)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def organization_type_create_api(request):
    """API for creating organization type"""
    try:
        data = json.loads(request.body)
        
        org_type = OrganizationType.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Jenis organisasi berhasil ditambahkan',
            'data': {
                'id': org_type.id,
                'name': org_type.name,
                'description': org_type.description,
                'is_active': org_type.is_active
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan jenis organisasi: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def organization_type_update_api(request, type_id):
    """API for updating organization type"""
    try:
        org_type = get_object_or_404(OrganizationType, id=type_id)
        data = json.loads(request.body)
        
        org_type.name = data.get('name', org_type.name)
        org_type.description = data.get('description', org_type.description)
        org_type.is_active = data.get('is_active', org_type.is_active)
        org_type.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Jenis organisasi berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui jenis organisasi: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def organization_type_delete_api(request, type_id):
    """API for deleting organization type"""
    try:
        org_type = get_object_or_404(OrganizationType, id=type_id)
        
        # Check if type is being used
        if org_type.organization_set.exists():
            return JsonResponse({
                'success': False,
                'message': 'Jenis organisasi tidak dapat dihapus karena masih digunakan'
            }, status=400)
        
        org_type.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Jenis organisasi berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus jenis organisasi: {str(e)}'
        }, status=400)


# Organization API Views
@login_required
@require_http_methods(["GET"])
def organizations_api(request):
    """API for organizations list"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    search = request.GET.get('search', '')
    org_type_id = request.GET.get('organization_type_id', '')
    is_active = request.GET.get('is_active', '')
    
    queryset = Organization.objects.select_related('organization_type', 'leader')
    
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(leader__nama__icontains=search)
        )
    
    if org_type_id:
        queryset = queryset.filter(organization_type_id=org_type_id)
    
    if is_active:
        queryset = queryset.filter(is_active=is_active.lower() == 'true')
    
    queryset = queryset.order_by('-created_at')
    
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'results': [
            {
                'id': item.id,
                'name': item.name,
                'organization_type': item.organization_type.name,
                'organization_type_id': item.organization_type.id,
                'description': item.description,
                'established_date': item.established_date.strftime('%Y-%m-%d') if item.established_date else None,
                'leader_name': item.leader.nama if item.leader else None,
                'leader_id': item.leader.id if item.leader else None,
                'contact_phone': item.contact_phone,
                'contact_email': item.contact_email,
                'address': item.address,
                'is_active': item.is_active,
                'members_count': item.members.filter(is_active=True).count(),
                'events_count': item.events.count(),
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for item in page_obj
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


@login_required
@require_http_methods(["GET"])
def organization_detail_api(request, org_id):
    """API for organization detail"""
    organization = get_object_or_404(Organization.objects.select_related('organization_type', 'leader'), id=org_id)
    
    data = {
        'id': organization.id,
        'name': organization.name,
        'organization_type': organization.organization_type.name,
        'organization_type_id': organization.organization_type.id,
        'description': organization.description,
        'established_date': organization.established_date.strftime('%Y-%m-%d') if organization.established_date else None,
        'leader_name': organization.leader.nama if organization.leader else None,
        'leader_id': organization.leader.id if organization.leader else None,
        'contact_phone': organization.contact_phone,
        'contact_email': organization.contact_email,
        'address': organization.address,
        'is_active': organization.is_active,
        'members_count': organization.members.filter(is_active=True).count(),
        'events_count': organization.events.count(),
        'documents_count': organization.documents.count(),
        'created_at': organization.created_at.strftime('%Y-%m-%d %H:%M'),
        'updated_at': organization.updated_at.strftime('%Y-%m-%d %H:%M')
    }
    
    return JsonResponse(data)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def organization_create_api(request):
    """API for creating organization"""
    try:
        data = json.loads(request.body)
        
        organization = Organization.objects.create(
            name=data['name'],
            organization_type_id=data['organization_type_id'],
            description=data.get('description', ''),
            established_date=parse_date(data['established_date']) if data.get('established_date') else None,
            leader_id=data.get('leader_id') if data.get('leader_id') else None,
            contact_phone=data.get('contact_phone', ''),
            contact_email=data.get('contact_email', ''),
            address=data.get('address', ''),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Organisasi berhasil ditambahkan',
            'data': {
                'id': organization.id,
                'name': organization.name
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan organisasi: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def organization_update_api(request, org_id):
    """API for updating organization"""
    try:
        organization = get_object_or_404(Organization, id=org_id)
        data = json.loads(request.body)
        
        organization.name = data.get('name', organization.name)
        organization.organization_type_id = data.get('organization_type_id', organization.organization_type_id)
        organization.description = data.get('description', organization.description)
        organization.established_date = parse_date(data['established_date']) if data.get('established_date') else organization.established_date
        organization.leader_id = data.get('leader_id') if data.get('leader_id') else organization.leader_id
        organization.contact_phone = data.get('contact_phone', organization.contact_phone)
        organization.contact_email = data.get('contact_email', organization.contact_email)
        organization.address = data.get('address', organization.address)
        organization.is_active = data.get('is_active', organization.is_active)
        organization.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Organisasi berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui organisasi: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def organization_delete_api(request, org_id):
    """API for deleting organization"""
    try:
        organization = get_object_or_404(Organization, id=org_id)
        organization.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Organisasi berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus organisasi: {str(e)}'
        }, status=400)


# Organization Members API Views
@login_required
@require_http_methods(["GET"])
def organization_members_api(request):
    """API for organization members list"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    search = request.GET.get('search', '')
    organization_id = request.GET.get('organization_id', '')
    position = request.GET.get('position', '')
    is_active = request.GET.get('is_active', '')
    
    queryset = OrganizationMember.objects.select_related('organization', 'member')
    
    if search:
        queryset = queryset.filter(
            Q(member__nama__icontains=search) |
            Q(member__nik__icontains=search) |
            Q(organization__name__icontains=search)
        )
    
    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)
    
    if position:
        queryset = queryset.filter(position=position)
    
    if is_active:
        queryset = queryset.filter(is_active=is_active.lower() == 'true')
    
    queryset = queryset.order_by('-created_at')
    
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'results': [
            {
                'id': item.id,
                'organization_name': item.organization.name,
                'organization_id': item.organization.id,
                'member_name': item.member.nama,
                'member_id': item.member.id,
                'member_nik': item.member.nik,
                'position': item.position,
                'position_display': item.get_position_display(),
                'join_date': item.join_date.strftime('%Y-%m-%d'),
                'end_date': item.end_date.strftime('%Y-%m-%d') if item.end_date else None,
                'is_active': item.is_active,
                'notes': item.notes,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for item in page_obj
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


@login_required
@require_http_methods(["GET"])
def organization_member_detail_api(request, member_id):
    """API for organization member detail"""
    member = get_object_or_404(OrganizationMember.objects.select_related('organization', 'member'), id=member_id)
    
    data = {
        'id': member.id,
        'organization_name': member.organization.name,
        'organization_id': member.organization.id,
        'member_name': member.member.nama,
        'member_id': member.member.id,
        'member_nik': member.member.nik,
        'position': member.position,
        'position_display': member.get_position_display(),
        'join_date': member.join_date.strftime('%Y-%m-%d'),
        'end_date': member.end_date.strftime('%Y-%m-%d') if member.end_date else None,
        'is_active': member.is_active,
        'notes': member.notes,
        'created_at': member.created_at.strftime('%Y-%m-%d %H:%M'),
        'updated_at': member.updated_at.strftime('%Y-%m-%d %H:%M')
    }
    
    return JsonResponse(data)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def organization_member_create_api(request):
    """API for creating organization member"""
    try:
        data = json.loads(request.body)
        
        member = OrganizationMember.objects.create(
            organization_id=data['organization_id'],
            member_id=data['member_id'],
            position=data['position'],
            join_date=parse_date(data['join_date']),
            end_date=parse_date(data['end_date']) if data.get('end_date') else None,
            is_active=data.get('is_active', True),
            notes=data.get('notes', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Anggota organisasi berhasil ditambahkan',
            'data': {
                'id': member.id,
                'member_name': member.member.nama,
                'organization_name': member.organization.name
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan anggota organisasi: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def organization_member_update_api(request, member_id):
    """API for updating organization member"""
    try:
        member = get_object_or_404(OrganizationMember, id=member_id)
        data = json.loads(request.body)
        
        member.organization_id = data.get('organization_id', member.organization_id)
        member.member_id = data.get('member_id', member.member_id)
        member.position = data.get('position', member.position)
        member.join_date = parse_date(data['join_date']) if data.get('join_date') else member.join_date
        member.end_date = parse_date(data['end_date']) if data.get('end_date') else member.end_date
        member.is_active = data.get('is_active', member.is_active)
        member.notes = data.get('notes', member.notes)
        member.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Anggota organisasi berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui anggota organisasi: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def organization_member_delete_api(request, member_id):
    """API for deleting organization member"""
    try:
        member = get_object_or_404(OrganizationMember, id=member_id)
        member.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Anggota organisasi berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus anggota organisasi: {str(e)}'
        }, status=400)


# Organization Events API Views
@login_required
@require_http_methods(["GET"])
def organization_events_api(request):
    """API for organization events list"""
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    search = request.GET.get('search', '')
    organization_id = request.GET.get('organization_id', '')
    event_type = request.GET.get('event_type', '')
    is_completed = request.GET.get('is_completed', '')
    
    queryset = OrganizationEvent.objects.select_related('organization', 'created_by')
    
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )
    
    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)
    
    if event_type:
        queryset = queryset.filter(event_type=event_type)
    
    if is_completed:
        queryset = queryset.filter(is_completed=is_completed.lower() == 'true')
    
    queryset = queryset.order_by('-event_date')
    
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'results': [
            {
                'id': item.id,
                'title': item.title,
                'description': item.description,
                'organization_name': item.organization.name,
                'organization_id': item.organization.id,
                'event_type': item.event_type,
                'event_type_display': item.get_event_type_display(),
                'event_date': item.event_date.strftime('%Y-%m-%d %H:%M'),
                'location': item.location,
                'participants_count': item.participants_count,
                'budget': float(item.budget) if item.budget else None,
                'is_completed': item.is_completed,
                'created_by': item.created_by.username if item.created_by else None,
                'created_at': item.created_at.strftime('%Y-%m-%d %H:%M')
            }
            for item in page_obj
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


@login_required
@require_http_methods(["GET"])
def organization_event_detail_api(request, event_id):
    """API for organization event detail"""
    event = get_object_or_404(OrganizationEvent.objects.select_related('organization', 'created_by'), id=event_id)
    
    data = {
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'organization_name': event.organization.name,
        'organization_id': event.organization.id,
        'event_type': event.event_type,
        'event_type_display': event.get_event_type_display(),
        'event_date': event.event_date.strftime('%Y-%m-%d %H:%M'),
        'location': event.location,
        'participants_count': event.participants_count,
        'budget': float(event.budget) if event.budget else None,
        'is_completed': event.is_completed,
        'created_by': event.created_by.username if event.created_by else None,
        'created_at': event.created_at.strftime('%Y-%m-%d %H:%M'),
        'updated_at': event.updated_at.strftime('%Y-%m-%d %H:%M')
    }
    
    return JsonResponse(data)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def organization_event_create_api(request):
    """API for creating organization event"""
    try:
        data = json.loads(request.body)
        
        event = OrganizationEvent.objects.create(
            organization_id=data['organization_id'],
            title=data['title'],
            description=data.get('description', ''),
            event_type=data['event_type'],
            event_date=datetime.strptime(data['event_date'], '%Y-%m-%d %H:%M'),
            location=data.get('location', ''),
            participants_count=data.get('participants_count', 0),
            budget=data.get('budget') if data.get('budget') else None,
            is_completed=data.get('is_completed', False),
            created_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Acara organisasi berhasil ditambahkan',
            'data': {
                'id': event.id,
                'title': event.title
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan acara organisasi: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def organization_event_update_api(request, event_id):
    """API for updating organization event"""
    try:
        event = get_object_or_404(OrganizationEvent, id=event_id)
        data = json.loads(request.body)
        
        event.organization_id = data.get('organization_id', event.organization_id)
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        event.event_type = data.get('event_type', event.event_type)
        event.event_date = datetime.strptime(data['event_date'], '%Y-%m-%d %H:%M') if data.get('event_date') else event.event_date
        event.location = data.get('location', event.location)
        event.participants_count = data.get('participants_count', event.participants_count)
        event.budget = data.get('budget') if data.get('budget') else event.budget
        event.is_completed = data.get('is_completed', event.is_completed)
        event.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Acara organisasi berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui acara organisasi: {str(e)}'
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def organization_event_delete_api(request, event_id):
    """API for deleting organization event"""
    try:
        event = get_object_or_404(OrganizationEvent, id=event_id)
        event.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Acara organisasi berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus acara organisasi: {str(e)}'
        }, status=400)


# Helper API Views
@login_required
@require_http_methods(["GET"])
def organization_types_dropdown_api(request):
    """API for organization types dropdown"""
    types = OrganizationType.objects.filter(is_active=True).order_by('name')
    
    data = {
        'types': [
            {
                'id': org_type.id,
                'name': org_type.name
            }
            for org_type in types
        ]
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def organizations_dropdown_api(request):
    """API for organizations dropdown"""
    organizations = Organization.objects.filter(is_active=True).order_by('name')
    
    data = {
        'organizations': [
            {
                'id': org.id,
                'name': org.name
            }
            for org in organizations
        ]
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def residents_dropdown_api(request):
    """API for residents dropdown"""
    residents = Penduduk.objects.filter(status_kependudukan='tetap').order_by('nama')
    
    data = {
        'residents': [
            {
                'id': resident.id,
                'name': resident.nama,
                'nik': resident.nik
            }
            for resident in residents
        ]
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def organization_statistics_api(request):
    """API for organization statistics"""
    total_organizations = Organization.objects.count()
    active_organizations = Organization.objects.filter(is_active=True).count()
    total_members = OrganizationMember.objects.filter(is_active=True).count()
    total_events = OrganizationEvent.objects.count()
    completed_events = OrganizationEvent.objects.filter(is_completed=True).count()
    total_galeri = GaleriKegiatan.objects.count()
    active_galeri = GaleriKegiatan.objects.filter(is_active=True).count()
    
    # Organization types distribution
    org_types_stats = OrganizationType.objects.annotate(
        org_count=Count('organization')
    ).values('name', 'org_count')
    
    data = {
        'total_organizations': total_organizations,
        'active_organizations': active_organizations,
        'total_members': total_members,
        'total_events': total_events,
        'completed_events': completed_events,
        'total_galeri': total_galeri,
        'active_galeri': active_galeri,
        'organization_types': list(org_types_stats)
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def galeri_kegiatan_statistics_api(request):
    """API for galeri kegiatan statistics"""
    total_kegiatan = GaleriKegiatan.objects.count()
    total_foto = GaleriKegiatan.objects.exclude(foto='').count()
    kegiatan_aktif = GaleriKegiatan.objects.filter(is_active=True).count()
    total_views = 0  # This would need a views tracking system
    
    data = {
        'total_kegiatan': total_kegiatan,
        'total_foto': total_foto,
        'kegiatan_aktif': kegiatan_aktif,
        'total_views': total_views
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def galeri_kegiatan_export_api(request):
    """API for exporting galeri kegiatan to Excel"""
    try:
        # Create workbook and worksheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Galeri Kegiatan"
        
        # Headers
        headers = [
            'No', 'Judul', 'Deskripsi', 'Tanggal Kegiatan', 
            'Status', 'Tanggal Dibuat'
        ]
        
        # Write headers
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        # Get data
        galeri_list = GaleriKegiatan.objects.all().order_by('-created_at')
        
        # Write data
        for row, galeri in enumerate(galeri_list, 2):
            ws.cell(row=row, column=1, value=row-1)
            ws.cell(row=row, column=2, value=galeri.judul)
            ws.cell(row=row, column=3, value=galeri.deskripsi)
            ws.cell(row=row, column=4, value=galeri.tanggal_kegiatan.strftime('%Y-%m-%d'))
            ws.cell(row=row, column=5, value='Aktif' if galeri.is_active else 'Tidak Aktif')
            ws.cell(row=row, column=6, value=galeri.created_at.strftime('%Y-%m-%d %H:%M'))
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Save to BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        # Create response
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="galeri_kegiatan.xlsx"'
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal mengekspor data: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["GET"])
def anggota_organisasi_statistics_api(request):
    """API for anggota organisasi statistics"""
    total_anggota = AnggotaOrganisasi.objects.count()
    anggota_aktif = AnggotaOrganisasi.objects.filter(is_active=True).count()
    anggota_baru_bulan_ini = AnggotaOrganisasi.objects.filter(
        created_at__month=datetime.now().month,
        created_at__year=datetime.now().year
    ).count()
    
    # Count by organization
    org_stats = AnggotaOrganisasi.objects.values('organisasi__nama').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    data = {
        'total_anggota': total_anggota,
        'anggota_aktif': anggota_aktif,
        'anggota_baru': anggota_baru_bulan_ini,
        'top_organizations': list(org_stats)
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def jabatan_statistics_api(request):
    """API for jabatan statistics"""
    total_jabatan = Jabatan.objects.count()
    jabatan_aktif = Jabatan.objects.filter(is_active=True).count()
    jabatan_struktural = Jabatan.objects.filter(tipe='struktural').count()
    jabatan_fungsional = Jabatan.objects.filter(tipe='fungsional').count()
    
    data = {
        'total_jabatan': total_jabatan,
        'jabatan_aktif': jabatan_aktif,
        'jabatan_struktural': jabatan_struktural,
        'jabatan_fungsional': jabatan_fungsional
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def periode_kepengurusan_statistics_api(request):
    """API for periode kepengurusan statistics"""
    total_periode = PeriodeKepengurusan.objects.count()
    periode_aktif = PeriodeKepengurusan.objects.filter(is_active=True).count()
    periode_tahun_ini = PeriodeKepengurusan.objects.filter(
        tanggal_mulai__year=datetime.now().year
    ).count()
    
    data = {
        'total_periode': total_periode,
        'periode_aktif': periode_aktif,
        'periode_tahun_ini': periode_tahun_ini,
        'rata_durasi': 24  # Average duration in months
    }
    
    return JsonResponse(data)


@login_required
@require_http_methods(["GET"])
def struktur_organisasi_statistics_api(request):
    """API for struktur organisasi statistics"""
    total_struktur = StrukturOrganisasi.objects.count()
    struktur_aktif = StrukturOrganisasi.objects.filter(is_visible=True).count()
    total_organisasi = StrukturOrganisasi.objects.values('organization').distinct().count()
    
    data = {
        'total_struktur': total_struktur,
        'struktur_aktif': struktur_aktif,
        'total_organisasi': total_organisasi,
        'avg_members_per_org': round(total_struktur / max(total_organisasi, 1), 1)
    }
    
    return JsonResponse(data)


# Missing API endpoints for CRUD operations

@login_required
@require_http_methods(["POST"])
def anggota_organisasi_update_api(request, anggota_id):
    """API for updating anggota organisasi"""
    try:
        anggota = get_object_or_404(AnggotaOrganisasi, id=anggota_id)
        data = json.loads(request.body)
        
        # Update fields
        if 'organization_id' in data:
            anggota.organization_id = data['organization_id']
        if 'penduduk_id' in data:
            anggota.penduduk_id = data['penduduk_id']
        if 'jabatan_id' in data:
            anggota.jabatan_id = data['jabatan_id']
        if 'periode_id' in data:
            anggota.periode_id = data['periode_id']
        if 'status' in data:
            anggota.status = data['status']
        if 'bio' in data:
            anggota.bio = data['bio']
        
        anggota.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Anggota organisasi berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui anggota: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["DELETE"])
def anggota_organisasi_delete_api(request, anggota_id):
    """API for deleting anggota organisasi"""
    try:
        anggota = get_object_or_404(AnggotaOrganisasi, id=anggota_id)
        anggota.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Anggota organisasi berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus anggota: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["GET"])
def anggota_organisasi_export_api(request):
    """API for exporting anggota organisasi to Excel"""
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Anggota Organisasi"
        
        headers = ['No', 'Nama', 'Organisasi', 'Jabatan', 'Periode', 'Status', 'Tanggal Bergabung']
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        anggota_list = AnggotaOrganisasi.objects.select_related(
            'penduduk', 'organization', 'jabatan', 'periode'
        ).all().order_by('-created_at')
        
        for row, anggota in enumerate(anggota_list, 2):
            ws.cell(row=row, column=1, value=row-1)
            ws.cell(row=row, column=2, value=anggota.penduduk.name)
            ws.cell(row=row, column=3, value=anggota.organization.name)
            ws.cell(row=row, column=4, value=anggota.jabatan.nama_jabatan)
            ws.cell(row=row, column=5, value=anggota.periode.nama_periode)
            ws.cell(row=row, column=6, value=anggota.status.title())
            ws.cell(row=row, column=7, value=anggota.tanggal_bergabung.strftime('%Y-%m-%d'))
        
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="anggota_organisasi.xlsx"'
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal mengekspor data: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["POST"])
def jabatan_update_api(request, jabatan_id):
    """API for updating jabatan"""
    try:
        jabatan = get_object_or_404(Jabatan, id=jabatan_id)
        data = json.loads(request.body)
        
        if 'nama_jabatan' in data:
            jabatan.nama_jabatan = data['nama_jabatan']
        if 'deskripsi' in data:
            jabatan.deskripsi = data['deskripsi']
        if 'level_hierarki' in data:
            jabatan.level_hierarki = data['level_hierarki']
        if 'warna_badge' in data:
            jabatan.warna_badge = data['warna_badge']
        if 'is_active' in data:
            jabatan.is_active = data['is_active']
        
        jabatan.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Jabatan berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui jabatan: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["DELETE"])
def jabatan_delete_api(request, jabatan_id):
    """API for deleting jabatan"""
    try:
        jabatan = get_object_or_404(Jabatan, id=jabatan_id)
        jabatan.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Jabatan berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus jabatan: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["GET"])
def jabatan_export_api(request):
    """API for exporting jabatan to Excel"""
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Jabatan"
        
        headers = ['No', 'Nama Jabatan', 'Deskripsi', 'Level Hierarki', 'Status']
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        jabatan_list = Jabatan.objects.all().order_by('level_hierarki')
        
        for row, jabatan in enumerate(jabatan_list, 2):
            ws.cell(row=row, column=1, value=row-1)
            ws.cell(row=row, column=2, value=jabatan.nama_jabatan)
            ws.cell(row=row, column=3, value=jabatan.deskripsi)
            ws.cell(row=row, column=4, value=jabatan.level_hierarki)
            ws.cell(row=row, column=5, value='Aktif' if jabatan.is_active else 'Tidak Aktif')
        
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="jabatan.xlsx"'
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal mengekspor data: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["POST"])
def periode_kepengurusan_update_api(request, periode_id):
    """API for updating periode kepengurusan"""
    try:
        periode = get_object_or_404(PeriodeKepengurusan, id=periode_id)
        data = json.loads(request.body)
        
        if 'nama_periode' in data:
            periode.nama_periode = data['nama_periode']
        if 'tanggal_mulai' in data:
            periode.tanggal_mulai = data['tanggal_mulai']
        if 'tanggal_selesai' in data:
            periode.tanggal_selesai = data['tanggal_selesai']
        if 'deskripsi' in data:
            periode.deskripsi = data['deskripsi']
        if 'is_active' in data:
            periode.is_active = data['is_active']
        
        periode.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Periode kepengurusan berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui periode: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["DELETE"])
def periode_kepengurusan_delete_api(request, periode_id):
    """API for deleting periode kepengurusan"""
    try:
        periode = get_object_or_404(PeriodeKepengurusan, id=periode_id)
        periode.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Periode kepengurusan berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus periode: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["GET"])
def periode_kepengurusan_export_api(request):
    """API for exporting periode kepengurusan to Excel"""
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Periode Kepengurusan"
        
        headers = ['No', 'Nama Periode', 'Organisasi', 'Tanggal Mulai', 'Tanggal Selesai', 'Status']
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        periode_list = PeriodeKepengurusan.objects.select_related('organization').all().order_by('-tanggal_mulai')
        
        for row, periode in enumerate(periode_list, 2):
            ws.cell(row=row, column=1, value=row-1)
            ws.cell(row=row, column=2, value=periode.nama_periode)
            ws.cell(row=row, column=3, value=periode.organization.name)
            ws.cell(row=row, column=4, value=periode.tanggal_mulai.strftime('%Y-%m-%d'))
            ws.cell(row=row, column=5, value=periode.tanggal_selesai.strftime('%Y-%m-%d'))
            ws.cell(row=row, column=6, value='Aktif' if periode.is_active else 'Tidak Aktif')
        
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="periode_kepengurusan.xlsx"'
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal mengekspor data: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["POST"])
def struktur_organisasi_update_api(request, struktur_id):
    """API for updating struktur organisasi"""
    try:
        struktur = get_object_or_404(StrukturOrganisasi, id=struktur_id)
        data = json.loads(request.body)
        
        if 'posisi_x' in data:
            struktur.posisi_x = data['posisi_x']
        if 'posisi_y' in data:
            struktur.posisi_y = data['posisi_y']
        if 'urutan' in data:
            struktur.urutan = data['urutan']
        if 'is_visible' in data:
            struktur.is_visible = data['is_visible']
        
        struktur.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Struktur organisasi berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui struktur: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["DELETE"])
def struktur_organisasi_delete_api(request, struktur_id):
    """API for deleting struktur organisasi"""
    try:
        struktur = get_object_or_404(StrukturOrganisasi, id=struktur_id)
        struktur.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Struktur organisasi berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus struktur: {str(e)}'
        }, status=400)


@login_required
@require_http_methods(["GET"])
def struktur_organisasi_export_api(request):
    """API for exporting struktur organisasi to Excel"""
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Struktur Organisasi"
        
        headers = ['No', 'Organisasi', 'Nama', 'Jabatan', 'Periode', 'Urutan', 'Status']
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        struktur_list = StrukturOrganisasi.objects.select_related(
            'organization', 'anggota__penduduk', 'anggota__jabatan', 'periode'
        ).all().order_by('organization', 'urutan')
        
        for row, struktur in enumerate(struktur_list, 2):
            ws.cell(row=row, column=1, value=row-1)
            ws.cell(row=row, column=2, value=struktur.organization.name)
            ws.cell(row=row, column=3, value=struktur.anggota.penduduk.name)
            ws.cell(row=row, column=4, value=struktur.anggota.jabatan.nama_jabatan)
            ws.cell(row=row, column=5, value=struktur.periode.nama_periode if struktur.periode else '-')
            ws.cell(row=row, column=6, value=struktur.urutan)
            ws.cell(row=row, column=7, value='Terlihat' if struktur.is_visible else 'Tersembunyi')
        
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="struktur_organisasi.xlsx"'
        
        return response
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal mengekspor data: {str(e)}'
        }, status=400)
