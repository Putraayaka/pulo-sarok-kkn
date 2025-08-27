from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, date
import json

from .models import (
    PosyanduLocation, PosyanduSchedule, HealthRecord, 
    Immunization, NutritionData
)
from references.models import Penduduk


@login_required
def posyandu_module(request):
    """Main posyandu module view"""
    context = {
        'page_title': 'Manajemen Posyandu',
        'page_subtitle': 'Kelola data posyandu, jadwal, dan kesehatan'
    }
    return render(request, 'admin/modules/posyandu.html', context)


# ============= POSYANDU LOCATION VIEWS =============

@login_required
def posyandu_location_list(request):
    """List posyandu locations with pagination and search"""
    search = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    
    locations = PosyanduLocation.objects.all()
    
    if search:
        locations = locations.filter(
            Q(name__icontains=search) |
            Q(address__icontains=search) |
            Q(coordinator__nama__icontains=search)
        )
    
    locations = locations.select_related('coordinator').order_by('-created_at')
    
    paginator = Paginator(locations, per_page)
    page_obj = paginator.get_page(page)
    
    data = []
    for location in page_obj:
        data.append({
            'id': location.id,
            'name': location.name,
            'address': location.address,
            'coordinator': location.coordinator.nama if location.coordinator else '-',
            'contact_phone': location.contact_phone,
            'capacity': location.capacity,
            'facilities': location.facilities,
            'is_active': location.is_active,
            'established_date': location.established_date.strftime('%Y-%m-%d') if location.established_date else '-',
            'created_at': location.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({
        'results': data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })


@login_required
def posyandu_location_detail(request, location_id):
    """Get posyandu location detail"""
    location = get_object_or_404(PosyanduLocation, id=location_id)
    
    data = {
        'id': location.id,
        'name': location.name,
        'address': location.address,
        'coordinator_id': location.coordinator.id if location.coordinator else None,
        'coordinator_name': location.coordinator.nama if location.coordinator else '-',
        'contact_phone': location.contact_phone,
        'capacity': location.capacity,
        'facilities': location.facilities,
        'is_active': location.is_active,
        'established_date': location.established_date.strftime('%Y-%m-%d') if location.established_date else '',
        'created_at': location.created_at.strftime('%Y-%m-%d %H:%M')
    }
    
    return JsonResponse({'data': data})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def posyandu_location_create(request):
    """Create new posyandu location"""
    try:
        data = json.loads(request.body)
        
        coordinator = None
        if data.get('coordinator_id'):
            coordinator = get_object_or_404(Penduduk, id=data['coordinator_id'])
        
        established_date = None
        if data.get('established_date'):
            established_date = datetime.strptime(data['established_date'], '%Y-%m-%d').date()
        
        location = PosyanduLocation.objects.create(
            name=data['name'],
            address=data['address'],
            coordinator=coordinator,
            contact_phone=data.get('contact_phone', ''),
            capacity=data.get('capacity', 50),
            facilities=data.get('facilities', ''),
            is_active=data.get('is_active', True),
            established_date=established_date
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Lokasi posyandu berhasil ditambahkan',
            'data': {
                'id': location.id,
                'name': location.name
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan lokasi posyandu: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def posyandu_location_update(request, location_id):
    """Update posyandu location"""
    try:
        location = get_object_or_404(PosyanduLocation, id=location_id)
        data = json.loads(request.body)
        
        coordinator = None
        if data.get('coordinator_id'):
            coordinator = get_object_or_404(Penduduk, id=data['coordinator_id'])
        
        established_date = None
        if data.get('established_date'):
            established_date = datetime.strptime(data['established_date'], '%Y-%m-%d').date()
        
        location.name = data['name']
        location.address = data['address']
        location.coordinator = coordinator
        location.contact_phone = data.get('contact_phone', '')
        location.capacity = data.get('capacity', 50)
        location.facilities = data.get('facilities', '')
        location.is_active = data.get('is_active', True)
        location.established_date = established_date
        location.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Lokasi posyandu berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui lokasi posyandu: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def posyandu_location_delete(request, location_id):
    """Delete posyandu location"""
    try:
        location = get_object_or_404(PosyanduLocation, id=location_id)
        location_name = location.name
        location.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Lokasi posyandu "{location_name}" berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus lokasi posyandu: {str(e)}'
        }, status=400)


# ============= POSYANDU SCHEDULE VIEWS =============

@login_required
def posyandu_schedule_list(request):
    """List posyandu schedules with pagination and search"""
    search = request.GET.get('search', '')
    location_id = request.GET.get('location_id', '')
    activity_type = request.GET.get('activity_type', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    
    schedules = PosyanduSchedule.objects.all()
    
    if search:
        schedules = schedules.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(location__name__icontains=search)
        )
    
    if location_id:
        schedules = schedules.filter(location_id=location_id)
    
    if activity_type:
        schedules = schedules.filter(activity_type=activity_type)
    
    schedules = schedules.select_related('location', 'created_by').order_by('-schedule_date', 'start_time')
    
    paginator = Paginator(schedules, per_page)
    page_obj = paginator.get_page(page)
    
    data = []
    for schedule in page_obj:
        data.append({
            'id': schedule.id,
            'title': schedule.title,
            'description': schedule.description,
            'location_name': schedule.location.name,
            'activity_type': schedule.get_activity_type_display(),
            'schedule_date': schedule.schedule_date.strftime('%Y-%m-%d'),
            'start_time': schedule.start_time.strftime('%H:%M'),
            'end_time': schedule.end_time.strftime('%H:%M'),
            'target_participants': schedule.target_participants,
            'actual_participants': schedule.actual_participants,
            'is_completed': schedule.is_completed,
            'created_by': schedule.created_by.username if schedule.created_by else '-',
            'created_at': schedule.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({
        'results': data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })


@login_required
def posyandu_schedule_detail(request, schedule_id):
    """Get posyandu schedule detail"""
    schedule = get_object_or_404(PosyanduSchedule, id=schedule_id)
    
    data = {
        'id': schedule.id,
        'location_id': schedule.location.id,
        'location_name': schedule.location.name,
        'activity_type': schedule.activity_type,
        'title': schedule.title,
        'description': schedule.description,
        'schedule_date': schedule.schedule_date.strftime('%Y-%m-%d'),
        'start_time': schedule.start_time.strftime('%H:%M'),
        'end_time': schedule.end_time.strftime('%H:%M'),
        'target_participants': schedule.target_participants,
        'actual_participants': schedule.actual_participants,
        'notes': schedule.notes,
        'is_completed': schedule.is_completed,
        'created_by': schedule.created_by.username if schedule.created_by else '-',
        'created_at': schedule.created_at.strftime('%Y-%m-%d %H:%M')
    }
    
    return JsonResponse({'data': data})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def posyandu_schedule_create(request):
    """Create new posyandu schedule"""
    try:
        data = json.loads(request.body)
        
        location = get_object_or_404(PosyanduLocation, id=data['location_id'])
        schedule_date = datetime.strptime(data['schedule_date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        
        schedule = PosyanduSchedule.objects.create(
            location=location,
            activity_type=data['activity_type'],
            title=data['title'],
            description=data.get('description', ''),
            schedule_date=schedule_date,
            start_time=start_time,
            end_time=end_time,
            target_participants=data.get('target_participants', 0),
            actual_participants=data.get('actual_participants', 0),
            notes=data.get('notes', ''),
            is_completed=data.get('is_completed', False),
            created_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Jadwal posyandu berhasil ditambahkan',
            'data': {
                'id': schedule.id,
                'title': schedule.title
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan jadwal posyandu: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def posyandu_schedule_update(request, schedule_id):
    """Update posyandu schedule"""
    try:
        schedule = get_object_or_404(PosyanduSchedule, id=schedule_id)
        data = json.loads(request.body)
        
        location = get_object_or_404(PosyanduLocation, id=data['location_id'])
        schedule_date = datetime.strptime(data['schedule_date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        
        schedule.location = location
        schedule.activity_type = data['activity_type']
        schedule.title = data['title']
        schedule.description = data.get('description', '')
        schedule.schedule_date = schedule_date
        schedule.start_time = start_time
        schedule.end_time = end_time
        schedule.target_participants = data.get('target_participants', 0)
        schedule.actual_participants = data.get('actual_participants', 0)
        schedule.notes = data.get('notes', '')
        schedule.is_completed = data.get('is_completed', False)
        schedule.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Jadwal posyandu berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui jadwal posyandu: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def posyandu_schedule_delete(request, schedule_id):
    """Delete posyandu schedule"""
    try:
        schedule = get_object_or_404(PosyanduSchedule, id=schedule_id)
        schedule_title = schedule.title
        schedule.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Jadwal "{schedule_title}" berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus jadwal: {str(e)}'
        }, status=400)


# ============= HEALTH RECORD VIEWS =============

@login_required
def health_record_list(request):
    """List health records with pagination and search"""
    search = request.GET.get('search', '')
    patient_type = request.GET.get('patient_type', '')
    posyandu_id = request.GET.get('posyandu_id', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    
    records = HealthRecord.objects.all()
    
    if search:
        records = records.filter(
            Q(patient__nama__icontains=search) |
            Q(patient__nik__icontains=search) |
            Q(diagnosis__icontains=search) |
            Q(complaints__icontains=search)
        )
    
    if patient_type:
        records = records.filter(patient_type=patient_type)
    
    if posyandu_id:
        records = records.filter(posyandu_id=posyandu_id)
    
    records = records.select_related('patient', 'posyandu', 'recorded_by').order_by('-visit_date')
    
    paginator = Paginator(records, per_page)
    page_obj = paginator.get_page(page)
    
    data = []
    for record in page_obj:
        data.append({
            'id': record.id,
            'patient_name': record.patient.nama,
            'patient_nik': record.patient.nik,
            'posyandu_name': record.posyandu.name,
            'patient_type': record.get_patient_type_display(),
            'visit_date': record.visit_date.strftime('%Y-%m-%d'),
            'weight': float(record.weight) if record.weight else None,
            'height': float(record.height) if record.height else None,
            'blood_pressure': record.blood_pressure,
            'temperature': float(record.temperature) if record.temperature else None,
            'complaints': record.complaints,
            'diagnosis': record.diagnosis,
            'treatment': record.treatment,
            'next_visit': record.next_visit.strftime('%Y-%m-%d') if record.next_visit else None,
            'recorded_by': record.recorded_by.username if record.recorded_by else '-',
            'created_at': record.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({
        'results': data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })


# ============= IMMUNIZATION VIEWS =============

@login_required
def immunization_list(request):
    """List immunizations with pagination and search"""
    search = request.GET.get('search', '')
    vaccine_type = request.GET.get('vaccine_type', '')
    posyandu_id = request.GET.get('posyandu_id', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    
    immunizations = Immunization.objects.all()
    
    if search:
        immunizations = immunizations.filter(
            Q(patient__nama__icontains=search) |
            Q(patient__nik__icontains=search) |
            Q(vaccine_name__icontains=search)
        )
    
    if vaccine_type:
        immunizations = immunizations.filter(vaccine_type=vaccine_type)
    
    if posyandu_id:
        immunizations = immunizations.filter(posyandu_id=posyandu_id)
    
    immunizations = immunizations.select_related('patient', 'posyandu', 'administered_by').order_by('-immunization_date')
    
    paginator = Paginator(immunizations, per_page)
    page_obj = paginator.get_page(page)
    
    data = []
    for immunization in page_obj:
        data.append({
            'id': immunization.id,
            'patient_name': immunization.patient.nama,
            'patient_nik': immunization.patient.nik,
            'posyandu_name': immunization.posyandu.name,
            'vaccine_type': immunization.get_vaccine_type_display(),
            'vaccine_name': immunization.vaccine_name,
            'dose_number': immunization.dose_number,
            'immunization_date': immunization.immunization_date.strftime('%Y-%m-%d'),
            'batch_number': immunization.batch_number,
            'expiry_date': immunization.expiry_date.strftime('%Y-%m-%d') if immunization.expiry_date else None,
            'side_effects': immunization.side_effects,
            'next_dose_date': immunization.next_dose_date.strftime('%Y-%m-%d') if immunization.next_dose_date else None,
            'administered_by': immunization.administered_by.username if immunization.administered_by else '-',
            'created_at': immunization.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({
        'results': data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })


# ============= NUTRITION DATA VIEWS =============

@login_required
def nutrition_data_list(request):
    """List nutrition data with pagination and search"""
    search = request.GET.get('search', '')
    nutrition_status = request.GET.get('nutrition_status', '')
    posyandu_id = request.GET.get('posyandu_id', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    
    nutrition_data = NutritionData.objects.all()
    
    if search:
        nutrition_data = nutrition_data.filter(
            Q(patient__nama__icontains=search) |
            Q(patient__nik__icontains=search)
        )
    
    if nutrition_status:
        nutrition_data = nutrition_data.filter(nutrition_status=nutrition_status)
    
    if posyandu_id:
        nutrition_data = nutrition_data.filter(posyandu_id=posyandu_id)
    
    nutrition_data = nutrition_data.select_related('patient', 'posyandu', 'recorded_by').order_by('-measurement_date')
    
    paginator = Paginator(nutrition_data, per_page)
    page_obj = paginator.get_page(page)
    
    data = []
    for nutrition in page_obj:
        data.append({
            'id': nutrition.id,
            'patient_name': nutrition.patient.nama,
            'patient_nik': nutrition.patient.nik,
            'posyandu_name': nutrition.posyandu.name,
            'measurement_date': nutrition.measurement_date.strftime('%Y-%m-%d'),
            'age_months': nutrition.age_months,
            'weight': float(nutrition.weight),
            'height': float(nutrition.height),
            'head_circumference': float(nutrition.head_circumference) if nutrition.head_circumference else None,
            'arm_circumference': float(nutrition.arm_circumference) if nutrition.arm_circumference else None,
            'nutrition_status': nutrition.get_nutrition_status_display(),
            'vitamin_a_given': nutrition.vitamin_a_given,
            'iron_supplement_given': nutrition.iron_supplement_given,
            'notes': nutrition.notes,
            'recorded_by': nutrition.recorded_by.username if nutrition.recorded_by else '-',
            'created_at': nutrition.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({
        'results': data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })


# ============= STATISTICS API =============

@login_required
def posyandu_stats(request):
    """Get posyandu statistics"""
    try:
        # Basic counts
        total_locations = PosyanduLocation.objects.filter(is_active=True).count()
        total_schedules = PosyanduSchedule.objects.count()
        total_health_records = HealthRecord.objects.count()
        total_immunizations = Immunization.objects.count()
        
        # New specific counts for dashboard
        total_kader = PosyanduKader.objects.filter(status='aktif').count()
        total_ibu_hamil = IbuHamil.objects.filter(status_aktif=True).count()
        total_stunting = StuntingData.objects.count()
        
        # Count balita (children under 5 years old)
        today = date.today()
        balita = Penduduk.objects.filter(
            tanggal_lahir__gte=today.replace(year=today.year-5)
        ).count()
        
        # Count lansia (elderly 60+ years old)
        lansia = Penduduk.objects.filter(
            tanggal_lahir__lte=today.replace(year=today.year-60)
        ).count()
        
        # Recent activities
        recent_schedules = PosyanduSchedule.objects.filter(
            schedule_date__gte=date.today()
        ).count()
        
        # Patient type distribution
        patient_types = HealthRecord.objects.values('patient_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Nutrition status distribution
        nutrition_status = NutritionData.objects.values('nutrition_status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Vaccine type distribution
        vaccine_types = Immunization.objects.values('vaccine_type').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Stunting status distribution
        stunting_status = StuntingData.objects.values('status_stunting').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Pregnancy risk distribution
        pregnancy_risk = IbuHamil.objects.values('risiko_kehamilan').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return JsonResponse({
            'total_locations': total_locations,
            'total_schedules': total_schedules,
            'total_health_records': total_health_records,
            'total_immunizations': total_immunizations,
            'total_kader': total_kader,
            'total_ibu_hamil': total_ibu_hamil,
            'total_balita': balita,
            'total_lansia': lansia,
            'total_stunting': total_stunting,
            'recent_schedules': recent_schedules,
            'patient_types': list(patient_types),
            'nutrition_status': list(nutrition_status),
            'vaccine_types': list(vaccine_types),
            'stunting_status': list(stunting_status),
            'pregnancy_risk': list(pregnancy_risk)
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal memuat statistik posyandu: {str(e)}'
        }, status=500)


# ============= HELPER VIEWS =============

@login_required
def get_posyandu_locations(request):
    """Get all active posyandu locations for dropdown"""
    locations = PosyanduLocation.objects.filter(is_active=True).values('id', 'name')
    return JsonResponse({'locations': list(locations)})


@login_required
def get_residents_for_posyandu(request):
    """Get residents for posyandu selection"""
    search = request.GET.get('search', '')
    residents = Penduduk.objects.all()
    
    if search:
        residents = residents.filter(
            Q(nama__icontains=search) |
            Q(nik__icontains=search)
        )
    
    residents = residents.values('id', 'nama', 'nik', 'tanggal_lahir', 'jenis_kelamin')[:20]
    
    data = []
    for resident in residents:
        age = None
        if resident['tanggal_lahir']:
            today = date.today()
            age = today.year - resident['tanggal_lahir'].year
            if today.month < resident['tanggal_lahir'].month or \
               (today.month == resident['tanggal_lahir'].month and today.day < resident['tanggal_lahir'].day):
                age -= 1
        
        data.append({
            'id': resident['id'],
            'nama': resident['nama'],
            'nik': resident['nik'],
            'age': age,
            'jenis_kelamin': resident['jenis_kelamin']
        })
    
    return JsonResponse({'residents': data})


@login_required
def posyandu_dashboard(request):
    """Main posyandu dashboard"""
    context = {
        'page_title': 'Dashboard Posyandu',
        'page_subtitle': 'Overview data posyandu dan kesehatan'
    }
    return render(request, 'admin/modules/posyandu/index.html', context)

@login_required
def kader_admin(request):
    """Kader Posyandu admin page"""
    context = {
        'page_title': 'Input Kader Posyandu',
        'page_subtitle': 'Kelola data kader posyandu'
    }
    return render(request, 'admin/modules/posyandu/kader.html', context)

@login_required
def ibu_hamil_admin(request):
    """Ibu Hamil admin page"""
    context = {
        'page_title': 'Input Data Ibu Hamil',
        'page_subtitle': 'Kelola data ibu hamil'
    }
    return render(request, 'admin/modules/posyandu/ibu_hamil.html', context)

@login_required
def view_balita(request):
    """View Balita page"""
    context = {
        'page_title': 'View Data Balita',
        'page_subtitle': 'Lihat dan kelola data balita'
    }
    return render(request, 'admin/modules/posyandu/balita.html', context)

@login_required
def view_lansia(request):
    """View Lansia page"""
    context = {
        'page_title': 'View Data Lansia',
        'page_subtitle': 'Lihat dan kelola data lansia'
    }
    return render(request, 'admin/modules/posyandu/lansia.html', context)

@login_required
def stunting_admin(request):
    """Stunting admin page"""
    context = {
        'page_title': 'Input Data Stunting',
        'page_subtitle': 'Kelola data stunting balita'
    }
    return render(request, 'admin/modules/posyandu/stunting.html', context)


# ============= PEMERIKSAAN IBU HAMIL API VIEWS =============

@login_required
def pemeriksaan_ibu_hamil_list_api(request):
    """List pemeriksaan ibu hamil"""
    ibu_hamil_id = request.GET.get('ibu_hamil_id', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    
    pemeriksaan = PemeriksaanIbuHamil.objects.all()
    
    if ibu_hamil_id:
        pemeriksaan = pemeriksaan.filter(ibu_hamil_id=ibu_hamil_id)
    
    pemeriksaan = pemeriksaan.select_related('ibu_hamil__penduduk', 'pemeriksa').order_by('-tanggal_periksa')
    
    paginator = Paginator(pemeriksaan, per_page)
    page_obj = paginator.get_page(page)
    
    data = []
    for p in page_obj:
        data.append({
            'id': p.id,
            'ibu_nama': p.ibu_hamil.penduduk.nama,
            'tanggal_periksa': p.tanggal_periksa.strftime('%Y-%m-%d'),
            'usia_kehamilan': p.usia_kehamilan,
            'berat_badan': float(p.berat_badan),
            'tekanan_darah': p.tekanan_darah,
            'hemoglobin': float(p.hemoglobin) if p.hemoglobin else None,
            'tablet_fe': p.tablet_fe,
            'imunisasi_tt': p.imunisasi_tt,
            'keluhan': p.keluhan,
            'pemeriksa': p.pemeriksa.username if p.pemeriksa else '-',
            'created_at': p.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({
        'results': data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def pemeriksaan_ibu_hamil_create_api(request):
    """Create pemeriksaan ibu hamil"""
    try:
        data = json.loads(request.body)
        
        ibu_hamil = get_object_or_404(IbuHamil, id=data['ibu_hamil_id'])
        tanggal_periksa = datetime.strptime(data['tanggal_periksa'], '%Y-%m-%d').date()
        
        pemeriksaan = PemeriksaanIbuHamil.objects.create(
            ibu_hamil=ibu_hamil,
            tanggal_periksa=tanggal_periksa,
            usia_kehamilan=data['usia_kehamilan'],
            berat_badan=data['berat_badan'],
            tekanan_darah=data['tekanan_darah'],
            tinggi_fundus=data.get('tinggi_fundus'),
            lingkar_lengan_atas=data.get('lingkar_lengan_atas'),
            hemoglobin=data.get('hemoglobin'),
            protein_urin=data.get('protein_urin', ''),
            tablet_fe=data.get('tablet_fe', False),
            imunisasi_tt=data.get('imunisasi_tt', False),
            keluhan=data.get('keluhan', ''),
            anjuran=data.get('anjuran', ''),
            pemeriksa=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Data pemeriksaan berhasil ditambahkan',
            'data': {'id': pemeriksaan.id}
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan data pemeriksaan: {str(e)}'
        }, status=400)


# ============= KADER API VIEWS =============

@login_required
def kader_list_api(request):
    """List kader posyandu with pagination and search"""
    search = request.GET.get('search', '')
    posyandu_id = request.GET.get('posyandu_id', '')
    status = request.GET.get('status', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    
    kaders = PosyanduKader.objects.all()
    
    if search:
        kaders = kaders.filter(
            Q(penduduk__nama__icontains=search) |
            Q(penduduk__nik__icontains=search) |
            Q(posyandu__name__icontains=search)
        )
    
    if posyandu_id:
        kaders = kaders.filter(posyandu_id=posyandu_id)
    
    if status:
        kaders = kaders.filter(status=status)
    
    kaders = kaders.select_related('penduduk', 'posyandu').order_by('-created_at')
    
    paginator = Paginator(kaders, per_page)
    page_obj = paginator.get_page(page)
    
    data = []
    for kader in page_obj:
        data.append({
            'id': kader.id,
            'nama': kader.penduduk.nama,
            'nik': kader.penduduk.nik,
            'posyandu': kader.posyandu.name,
            'jabatan': kader.get_jabatan_display(),
            'nomor_hp': kader.nomor_hp,
            'tanggal_mulai': kader.tanggal_mulai.strftime('%Y-%m-%d'),
            'tanggal_selesai': kader.tanggal_selesai.strftime('%Y-%m-%d') if kader.tanggal_selesai else None,
            'status': kader.get_status_display(),
            'created_at': kader.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({
        'results': data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })


@login_required
def kader_detail_api(request, kader_id):
    """Get kader detail"""
    kader = get_object_or_404(PosyanduKader, id=kader_id)
    
    data = {
        'id': kader.id,
        'penduduk_id': kader.penduduk.id,
        'nama': kader.penduduk.nama,
        'nik': kader.penduduk.nik,
        'posyandu_id': kader.posyandu.id,
        'posyandu_name': kader.posyandu.name,
        'jabatan': kader.jabatan,
        'nomor_hp': kader.nomor_hp,
        'tanggal_mulai': kader.tanggal_mulai.strftime('%Y-%m-%d'),
        'tanggal_selesai': kader.tanggal_selesai.strftime('%Y-%m-%d') if kader.tanggal_selesai else '',
        'status': kader.status,
        'keterangan': kader.keterangan,
        'created_at': kader.created_at.strftime('%Y-%m-%d %H:%M')
    }
    
    return JsonResponse({'data': data})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def kader_create_api(request):
    """Create new kader"""
    try:
        data = json.loads(request.body)
        
        penduduk = get_object_or_404(Penduduk, id=data['penduduk_id'])
        posyandu = get_object_or_404(PosyanduLocation, id=data['posyandu_id'])
        
        tanggal_mulai = datetime.strptime(data['tanggal_mulai'], '%Y-%m-%d').date()
        tanggal_selesai = None
        if data.get('tanggal_selesai'):
            tanggal_selesai = datetime.strptime(data['tanggal_selesai'], '%Y-%m-%d').date()
        
        kader = PosyanduKader.objects.create(
            penduduk=penduduk,
            posyandu=posyandu,
            jabatan=data['jabatan'],
            nomor_hp=data.get('nomor_hp', ''),
            tanggal_mulai=tanggal_mulai,
            tanggal_selesai=tanggal_selesai,
            status=data.get('status', 'aktif'),
            keterangan=data.get('keterangan', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Kader berhasil ditambahkan',
            'data': {'id': kader.id, 'nama': kader.penduduk.nama}
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan kader: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def kader_update_api(request, kader_id):
    """Update kader"""
    try:
        kader = get_object_or_404(PosyanduKader, id=kader_id)
        data = json.loads(request.body)
        
        penduduk = get_object_or_404(Penduduk, id=data['penduduk_id'])
        posyandu = get_object_or_404(PosyanduLocation, id=data['posyandu_id'])
        
        tanggal_mulai = datetime.strptime(data['tanggal_mulai'], '%Y-%m-%d').date()
        tanggal_selesai = None
        if data.get('tanggal_selesai'):
            tanggal_selesai = datetime.strptime(data['tanggal_selesai'], '%Y-%m-%d').date()
        
        kader.penduduk = penduduk
        kader.posyandu = posyandu
        kader.jabatan = data['jabatan']
        kader.nomor_hp = data.get('nomor_hp', '')
        kader.tanggal_mulai = tanggal_mulai
        kader.tanggal_selesai = tanggal_selesai
        kader.status = data.get('status', 'aktif')
        kader.keterangan = data.get('keterangan', '')
        kader.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Kader berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui kader: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def kader_delete_api(request, kader_id):
    """Delete kader"""
    try:
        kader = get_object_or_404(PosyanduKader, id=kader_id)
        kader_name = kader.penduduk.nama
        kader.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Kader "{kader_name}" berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus kader: {str(e)}'
        }, status=400)


# ============= IBU HAMIL API VIEWS =============

@login_required
def ibu_hamil_list_api(request):
    """List ibu hamil with pagination and search"""
    search = request.GET.get('search', '')
    posyandu_id = request.GET.get('posyandu_id', '')
    risiko = request.GET.get('risiko', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    
    ibu_hamil = IbuHamil.objects.filter(status_aktif=True)
    
    if search:
        ibu_hamil = ibu_hamil.filter(
            Q(penduduk__nama__icontains=search) |
            Q(penduduk__nik__icontains=search) |
            Q(nomor_buku_kia__icontains=search)
        )
    
    if posyandu_id:
        ibu_hamil = ibu_hamil.filter(posyandu_id=posyandu_id)
    
    if risiko:
        ibu_hamil = ibu_hamil.filter(risiko_kehamilan=risiko)
    
    ibu_hamil = ibu_hamil.select_related('penduduk', 'posyandu').order_by('-created_at')
    
    paginator = Paginator(ibu_hamil, per_page)
    page_obj = paginator.get_page(page)
    
    data = []
    for ibu in page_obj:
        data.append({
            'id': ibu.id,
            'nama': ibu.penduduk.nama,
            'nik': ibu.penduduk.nik,
            'posyandu': ibu.posyandu.name,
            'usia_kehamilan': ibu.usia_kehamilan,
            'tanggal_hpht': ibu.tanggal_hpht.strftime('%Y-%m-%d'),
            'tanggal_perkiraan_lahir': ibu.tanggal_perkiraan_lahir.strftime('%Y-%m-%d'),
            'riwayat_kehamilan': ibu.get_riwayat_kehamilan_display(),
            'risiko_kehamilan': ibu.get_risiko_kehamilan_display(),
            'nomor_buku_kia': ibu.nomor_buku_kia,
            'created_at': ibu.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({
        'results': data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })


@login_required
def ibu_hamil_detail_api(request, ibu_id):
    """Get ibu hamil detail"""
    ibu = get_object_or_404(IbuHamil, id=ibu_id)
    
    data = {
        'id': ibu.id,
        'penduduk_id': ibu.penduduk.id,
        'nama': ibu.penduduk.nama,
        'nik': ibu.penduduk.nik,
        'posyandu_id': ibu.posyandu.id,
        'posyandu_name': ibu.posyandu.name,
        'tanggal_hpht': ibu.tanggal_hpht.strftime('%Y-%m-%d'),
        'usia_kehamilan': ibu.usia_kehamilan,
        'tanggal_perkiraan_lahir': ibu.tanggal_perkiraan_lahir.strftime('%Y-%m-%d'),
        'riwayat_kehamilan': ibu.riwayat_kehamilan,
        'berat_badan_sebelum_hamil': float(ibu.berat_badan_sebelum_hamil) if ibu.berat_badan_sebelum_hamil else None,
        'tinggi_badan': float(ibu.tinggi_badan) if ibu.tinggi_badan else None,
        'golongan_darah': ibu.golongan_darah,
        'riwayat_penyakit': ibu.riwayat_penyakit,
        'risiko_kehamilan': ibu.risiko_kehamilan,
        'nomor_buku_kia': ibu.nomor_buku_kia,
        'keterangan': ibu.keterangan,
        'created_at': ibu.created_at.strftime('%Y-%m-%d %H:%M')
    }
    
    return JsonResponse({'data': data})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def ibu_hamil_create_api(request):
    """Create new ibu hamil"""
    try:
        data = json.loads(request.body)
        
        penduduk = get_object_or_404(Penduduk, id=data['penduduk_id'])
        posyandu = get_object_or_404(PosyanduLocation, id=data['posyandu_id'])
        
        tanggal_hpht = datetime.strptime(data['tanggal_hpht'], '%Y-%m-%d').date()
        
        ibu = IbuHamil.objects.create(
            penduduk=penduduk,
            posyandu=posyandu,
            tanggal_hpht=tanggal_hpht,
            usia_kehamilan=data['usia_kehamilan'],
            riwayat_kehamilan=data['riwayat_kehamilan'],
            berat_badan_sebelum_hamil=data.get('berat_badan_sebelum_hamil'),
            tinggi_badan=data.get('tinggi_badan'),
            golongan_darah=data.get('golongan_darah', ''),
            riwayat_penyakit=data.get('riwayat_penyakit', ''),
            risiko_kehamilan=data.get('risiko_kehamilan', 'rendah'),
            nomor_buku_kia=data.get('nomor_buku_kia', ''),
            keterangan=data.get('keterangan', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Data ibu hamil berhasil ditambahkan',
            'data': {'id': ibu.id, 'nama': ibu.penduduk.nama}
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan data ibu hamil: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def ibu_hamil_update_api(request, ibu_id):
    """Update ibu hamil"""
    try:
        ibu = get_object_or_404(IbuHamil, id=ibu_id)
        data = json.loads(request.body)
        
        penduduk = get_object_or_404(Penduduk, id=data['penduduk_id'])
        posyandu = get_object_or_404(PosyanduLocation, id=data['posyandu_id'])
        
        tanggal_hpht = datetime.strptime(data['tanggal_hpht'], '%Y-%m-%d').date()
        
        ibu.penduduk = penduduk
        ibu.posyandu = posyandu
        ibu.tanggal_hpht = tanggal_hpht
        ibu.usia_kehamilan = data['usia_kehamilan']
        ibu.riwayat_kehamilan = data['riwayat_kehamilan']
        ibu.berat_badan_sebelum_hamil = data.get('berat_badan_sebelum_hamil')
        ibu.tinggi_badan = data.get('tinggi_badan')
        ibu.golongan_darah = data.get('golongan_darah', '')
        ibu.riwayat_penyakit = data.get('riwayat_penyakit', '')
        ibu.risiko_kehamilan = data.get('risiko_kehamilan', 'rendah')
        ibu.nomor_buku_kia = data.get('nomor_buku_kia', '')
        ibu.keterangan = data.get('keterangan', '')
        ibu.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Data ibu hamil berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui data ibu hamil: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def ibu_hamil_delete_api(request, ibu_id):
    """Delete ibu hamil"""
    try:
        ibu = get_object_or_404(IbuHamil, id=ibu_id)
        ibu_name = ibu.penduduk.nama
        ibu.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Data ibu hamil "{ibu_name}" berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus data ibu hamil: {str(e)}'
        }, status=400)


# ============= BALITA API VIEWS =============

@login_required
def balita_list_api(request):
    """List balita data using nutrition data"""
    search = request.GET.get('search', '')
    posyandu_id = request.GET.get('posyandu_id', '')
    nutrition_status = request.GET.get('nutrition_status', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    
    # Get balita from penduduk based on age
    today = date.today()
    balita = Penduduk.objects.filter(
        tanggal_lahir__gte=today.replace(year=today.year-5)
    )
    
    if search:
        balita = balita.filter(
            Q(nama__icontains=search) |
            Q(nik__icontains=search)
        )
    
    balita = balita.order_by('nama')
    
    paginator = Paginator(balita, per_page)
    page_obj = paginator.get_page(page)
    
    data = []
    for b in page_obj:
        age_months = 0
        if b.tanggal_lahir:
            age_months = (today.year - b.tanggal_lahir.year) * 12 + (today.month - b.tanggal_lahir.month)
        
        # Get latest nutrition data
        latest_nutrition = NutritionData.objects.filter(patient=b).first()
        
        data.append({
            'id': b.id,
            'nama': b.nama,
            'nik': b.nik,
            'tanggal_lahir': b.tanggal_lahir.strftime('%Y-%m-%d') if b.tanggal_lahir else None,
            'age_months': age_months,
            'jenis_kelamin': b.jenis_kelamin,
            'latest_weight': float(latest_nutrition.weight) if latest_nutrition else None,
            'latest_height': float(latest_nutrition.height) if latest_nutrition else None,
            'nutrition_status': latest_nutrition.get_nutrition_status_display() if latest_nutrition else 'Belum diukur',
            'last_measurement': latest_nutrition.measurement_date.strftime('%Y-%m-%d') if latest_nutrition else None
        })
    
    return JsonResponse({
        'results': data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })


# ============= LANSIA API VIEWS =============

@login_required
def lansia_list_api(request):
    """List lansia data using health records"""
    search = request.GET.get('search', '')
    posyandu_id = request.GET.get('posyandu_id', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    
    # Get lansia from penduduk based on age (60+ years)
    today = date.today()
    lansia = Penduduk.objects.filter(
        tanggal_lahir__lte=today.replace(year=today.year-60)
    )
    
    if search:
        lansia = lansia.filter(
            Q(nama__icontains=search) |
            Q(nik__icontains=search)
        )
    
    lansia = lansia.order_by('nama')
    
    paginator = Paginator(lansia, per_page)
    page_obj = paginator.get_page(page)
    
    data = []
    for l in page_obj:
        age = 0
        if l.tanggal_lahir:
            age = today.year - l.tanggal_lahir.year
            if today.month < l.tanggal_lahir.month or (today.month == l.tanggal_lahir.month and today.day < l.tanggal_lahir.day):
                age -= 1
        
        # Get latest health record
        latest_record = HealthRecord.objects.filter(patient=l, patient_type='lansia').first()
        
        data.append({
            'id': l.id,
            'nama': l.nama,
            'nik': l.nik,
            'tanggal_lahir': l.tanggal_lahir.strftime('%Y-%m-%d') if l.tanggal_lahir else None,
            'age': age,
            'jenis_kelamin': l.jenis_kelamin,
            'latest_weight': float(latest_record.weight) if latest_record and latest_record.weight else None,
            'latest_height': float(latest_record.height) if latest_record and latest_record.height else None,
            'blood_pressure': latest_record.blood_pressure if latest_record else None,
            'last_visit': latest_record.visit_date.strftime('%Y-%m-%d') if latest_record else None
        })
    
    return JsonResponse({
        'results': data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })


# ============= STUNTING API VIEWS =============

@login_required
def stunting_list_api(request):
    """List stunting data with pagination and search"""
    search = request.GET.get('search', '')
    posyandu_id = request.GET.get('posyandu_id', '')
    status_stunting = request.GET.get('status_stunting', '')
    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    
    stunting_data = StuntingData.objects.all()
    
    if search:
        stunting_data = stunting_data.filter(
            Q(balita__nama__icontains=search) |
            Q(balita__nik__icontains=search)
        )
    
    if posyandu_id:
        stunting_data = stunting_data.filter(posyandu_id=posyandu_id)
    
    if status_stunting:
        stunting_data = stunting_data.filter(status_stunting=status_stunting)
    
    stunting_data = stunting_data.select_related('balita', 'posyandu', 'recorded_by').order_by('-tanggal_ukur')
    
    paginator = Paginator(stunting_data, per_page)
    page_obj = paginator.get_page(page)
    
    data = []
    for stunting in page_obj:
        data.append({
            'id': stunting.id,
            'nama_balita': stunting.balita.nama,
            'nik_balita': stunting.balita.nik,
            'posyandu': stunting.posyandu.name,
            'tanggal_ukur': stunting.tanggal_ukur.strftime('%Y-%m-%d'),
            'usia_bulan': stunting.usia_bulan,
            'tinggi_badan': float(stunting.tinggi_badan),
            'berat_badan': float(stunting.berat_badan),
            'z_score_tb_u': float(stunting.z_score_tb_u),
            'status_stunting': stunting.get_status_stunting_display(),
            'asi_eksklusif': stunting.asi_eksklusif,
            'riwayat_bblr': stunting.riwayat_bblr,
            'intervensi_diberikan': stunting.get_intervensi_diberikan_display() if stunting.intervensi_diberikan else None,
            'follow_up_date': stunting.follow_up_date.strftime('%Y-%m-%d') if stunting.follow_up_date else None,
            'recorded_by': stunting.recorded_by.username if stunting.recorded_by else '-',
            'created_at': stunting.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({
        'results': data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    })


@login_required
def stunting_detail_api(request, stunting_id):
    """Get stunting detail"""
    stunting = get_object_or_404(StuntingData, id=stunting_id)
    
    data = {
        'id': stunting.id,
        'balita_id': stunting.balita.id,
        'nama_balita': stunting.balita.nama,
        'nik_balita': stunting.balita.nik,
        'posyandu_id': stunting.posyandu.id,
        'posyandu_name': stunting.posyandu.name,
        'tanggal_ukur': stunting.tanggal_ukur.strftime('%Y-%m-%d'),
        'usia_bulan': stunting.usia_bulan,
        'tinggi_badan': float(stunting.tinggi_badan),
        'berat_badan': float(stunting.berat_badan),
        'z_score_tb_u': float(stunting.z_score_tb_u),
        'z_score_bb_u': float(stunting.z_score_bb_u) if stunting.z_score_bb_u else None,
        'z_score_bb_tb': float(stunting.z_score_bb_tb) if stunting.z_score_bb_tb else None,
        'status_stunting': stunting.status_stunting,
        'asi_eksklusif': stunting.asi_eksklusif,
        'riwayat_bblr': stunting.riwayat_bblr,
        'riwayat_penyakit': stunting.riwayat_penyakit,
        'intervensi_diberikan': stunting.intervensi_diberikan,
        'hasil_intervensi': stunting.hasil_intervensi,
        'follow_up_date': stunting.follow_up_date.strftime('%Y-%m-%d') if stunting.follow_up_date else '',
        'keterangan': stunting.keterangan,
        'created_at': stunting.created_at.strftime('%Y-%m-%d %H:%M')
    }
    
    return JsonResponse({'data': data})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def stunting_create_api(request):
    """Create new stunting data"""
    try:
        data = json.loads(request.body)
        
        balita = get_object_or_404(Penduduk, id=data['balita_id'])
        posyandu = get_object_or_404(PosyanduLocation, id=data['posyandu_id'])
        
        tanggal_ukur = datetime.strptime(data['tanggal_ukur'], '%Y-%m-%d').date()
        follow_up_date = None
        if data.get('follow_up_date'):
            follow_up_date = datetime.strptime(data['follow_up_date'], '%Y-%m-%d').date()
        
        stunting = StuntingData.objects.create(
            balita=balita,
            posyandu=posyandu,
            tanggal_ukur=tanggal_ukur,
            usia_bulan=data['usia_bulan'],
            tinggi_badan=data['tinggi_badan'],
            berat_badan=data['berat_badan'],
            z_score_tb_u=data['z_score_tb_u'],
            z_score_bb_u=data.get('z_score_bb_u'),
            z_score_bb_tb=data.get('z_score_bb_tb'),
            status_stunting=data['status_stunting'],
            asi_eksklusif=data.get('asi_eksklusif', False),
            riwayat_bblr=data.get('riwayat_bblr', False),
            riwayat_penyakit=data.get('riwayat_penyakit', ''),
            intervensi_diberikan=data.get('intervensi_diberikan', ''),
            hasil_intervensi=data.get('hasil_intervensi', ''),
            follow_up_date=follow_up_date,
            keterangan=data.get('keterangan', ''),
            recorded_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Data stunting berhasil ditambahkan',
            'data': {'id': stunting.id, 'nama': stunting.balita.nama}
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menambahkan data stunting: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def stunting_update_api(request, stunting_id):
    """Update stunting data"""
    try:
        stunting = get_object_or_404(StuntingData, id=stunting_id)
        data = json.loads(request.body)
        
        balita = get_object_or_404(Penduduk, id=data['balita_id'])
        posyandu = get_object_or_404(PosyanduLocation, id=data['posyandu_id'])
        
        tanggal_ukur = datetime.strptime(data['tanggal_ukur'], '%Y-%m-%d').date()
        follow_up_date = None
        if data.get('follow_up_date'):
            follow_up_date = datetime.strptime(data['follow_up_date'], '%Y-%m-%d').date()
        
        stunting.balita = balita
        stunting.posyandu = posyandu
        stunting.tanggal_ukur = tanggal_ukur
        stunting.usia_bulan = data['usia_bulan']
        stunting.tinggi_badan = data['tinggi_badan']
        stunting.berat_badan = data['berat_badan']
        stunting.z_score_tb_u = data['z_score_tb_u']
        stunting.z_score_bb_u = data.get('z_score_bb_u')
        stunting.z_score_bb_tb = data.get('z_score_bb_tb')
        stunting.status_stunting = data['status_stunting']
        stunting.asi_eksklusif = data.get('asi_eksklusif', False)
        stunting.riwayat_bblr = data.get('riwayat_bblr', False)
        stunting.riwayat_penyakit = data.get('riwayat_penyakit', '')
        stunting.intervensi_diberikan = data.get('intervensi_diberikan', '')
        stunting.hasil_intervensi = data.get('hasil_intervensi', '')
        stunting.follow_up_date = follow_up_date
        stunting.keterangan = data.get('keterangan', '')
        stunting.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Data stunting berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal memperbarui data stunting: {str(e)}'
        }, status=400)


@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def stunting_delete_api(request, stunting_id):
    """Delete stunting data"""
    try:
        stunting = get_object_or_404(StuntingData, id=stunting_id)
        balita_name = stunting.balita.nama
        stunting.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Data stunting "{balita_name}" berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Gagal menghapus data stunting: {str(e)}'
        }, status=400)
