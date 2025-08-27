from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize
from django.db import transaction
import json
from datetime import datetime, timedelta

from .models import (
    Event, EventCategory, EventParticipant, EventRegistration,
    EventFeedback, EventSchedule, EventDocument
)
from references.models import Penduduk


# ============= MAIN VIEWS =============

@login_required
def events_dashboard(request):
    """Main events dashboard"""
    context = {
        'page_title': 'Dashboard Events',
        'page_subtitle': 'Kelola acara dan kegiatan desa'
    }
    return render(request, 'admin/modules/events/index.html', context)


@login_required
def events_list(request):
    """Events list view"""
    context = {
        'page_title': 'Daftar Events',
        'page_subtitle': 'Kelola semua events'
    }
    return render(request, 'admin/modules/events/list.html', context)


@login_required
def events_calendar(request):
    """Events calendar view"""
    context = {
        'page_title': 'Kalender Events',
        'page_subtitle': 'Lihat jadwal events dalam kalender'
    }
    return render(request, 'admin/modules/events/calendar.html', context)


@login_required
def events_categories(request):
    """Events categories management"""
    context = {
        'page_title': 'Kategori Events',
        'page_subtitle': 'Kelola kategori events'
    }
    return render(request, 'admin/modules/events/categories.html', context)


@login_required
def events_participants(request):
    """Events participants management"""
    context = {
        'page_title': 'Peserta Events',
        'page_subtitle': 'Kelola data peserta events'
    }
    return render(request, 'admin/modules/events/participants.html', context)


@login_required
def events_reports(request):
    """Events reports and analytics"""
    context = {
        'page_title': 'Laporan Events',
        'page_subtitle': 'Analisis dan laporan events'
    }
    return render(request, 'admin/modules/events/reports.html', context)


# ============= API VIEWS =============

@login_required
def events_stats_api(request):
    """Get events statistics"""
    try:
        # Basic counts
        total_events = Event.objects.count()
        active_events = Event.objects.filter(status='published').count()
        ongoing_events = Event.objects.filter(status='ongoing').count()
        completed_events = Event.objects.filter(status='completed').count()
        
        # Participant counts
        total_participants = EventParticipant.objects.count()
        confirmed_participants = EventParticipant.objects.filter(status='confirmed').count()
        attended_participants = EventParticipant.objects.filter(status='attended').count()
        
        # Category distribution
        category_stats = EventCategory.objects.annotate(
            event_count=Count('event')
        ).values('name', 'event_count', 'color')
        
        # Status distribution
        status_stats = Event.objects.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Monthly events
        current_month = timezone.now().month
        current_year = timezone.now().year
        monthly_events = Event.objects.filter(
            start_date__month=current_month,
            start_date__year=current_year
        ).count()
        
        # Recent events
        recent_events = Event.objects.filter(
            start_date__gte=timezone.now().date()
        ).order_by('start_date')[:5]
        
        recent_data = []
        for event in recent_events:
            recent_data.append({
                'id': event.id,
                'title': event.title,
                'start_date': event.start_date.strftime('%Y-%m-%d'),
                'category': event.category.name,
                'status': event.status
            })
        
        return JsonResponse({
            'total_events': total_events,
            'active_events': active_events,
            'ongoing_events': ongoing_events,
            'completed_events': completed_events,
            'total_participants': total_participants,
            'confirmed_participants': confirmed_participants,
            'attended_participants': attended_participants,
            'monthly_events': monthly_events,
            'category_stats': list(category_stats),
            'status_stats': list(status_stats),
            'recent_events': recent_data
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal memuat statistik events: {str(e)}'
        }, status=500)


@login_required
def events_list_api(request):
    """Get events list with pagination and filters"""
    try:
        # Get parameters
        page = request.GET.get('page', 1)
        per_page = int(request.GET.get('per_page', 10))
        search = request.GET.get('search', '')
        category = request.GET.get('category', '')
        status = request.GET.get('status', '')
        date_from = request.GET.get('date_from', '')
        date_to = request.GET.get('date_to', '')
        
        # Base queryset
        events = Event.objects.select_related('category', 'created_by')
        
        # Apply filters
        if search:
            events = events.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search) |
                Q(contact_person__icontains=search)
            )
        
        if category:
            events = events.filter(category_id=category)
        
        if status:
            events = events.filter(status=status)
        
        if date_from:
            events = events.filter(start_date__gte=date_from)
        
        if date_to:
            events = events.filter(start_date__lte=date_to)
        
        # Order by
        events = events.order_by('-start_date', '-created_at')
        
        # Pagination
        paginator = Paginator(events, per_page)
        page_obj = paginator.get_page(page)
        
        # Prepare data
        data = []
        for event in page_obj:
            data.append({
                'id': event.id,
                'title': event.title,
                'category': event.category.name,
                'start_date': event.start_date.strftime('%Y-%m-%d'),
                'end_date': event.end_date.strftime('%Y-%m-%d'),
                'start_time': event.start_time.strftime('%H:%M'),
                'end_time': event.end_time.strftime('%H:%M'),
                'location': event.location,
                'status': event.status,
                'priority': event.priority,
                'current_participants': event.current_participants,
                'max_participants': event.max_participants,
                'is_featured': event.is_featured,
                'is_free': event.is_free,
                'cost': float(event.cost) if event.cost else 0,
                'views_count': event.views_count,
                'rating': float(event.rating) if event.rating else 0,
                'created_at': event.created_at.strftime('%Y-%m-%d %H:%M'),
                'created_by': event.created_by.username if event.created_by else '-'
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
        
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal memuat daftar events: {str(e)}'
        }, status=500)


@login_required
def event_detail_api(request, event_id):
    """Get event detail"""
    try:
        event = get_object_or_404(Event, id=event_id)
        
        # Increment view count
        event.views_count += 1
        event.save(update_fields=['views_count'])
        
        data = {
            'id': event.id,
            'title': event.title,
            'slug': event.slug,
            'category': {
                'id': event.category.id,
                'name': event.category.name,
                'color': event.category.color
            },
            'description': event.description,
            'short_description': event.short_description,
            'start_date': event.start_date.strftime('%Y-%m-%d'),
            'end_date': event.end_date.strftime('%Y-%m-%d'),
            'start_time': event.start_time.strftime('%H:%M'),
            'end_time': event.end_time.strftime('%H:%M'),
            'location': event.location,
            'address': event.address,
            'latitude': float(event.latitude) if event.latitude else None,
            'longitude': float(event.longitude) if event.longitude else None,
            'max_participants': event.max_participants,
            'current_participants': event.current_participants,
            'allow_registration': event.allow_registration,
            'registration_deadline': event.registration_deadline.strftime('%Y-%m-%d %H:%M') if event.registration_deadline else None,
            'is_free': event.is_free,
            'cost': float(event.cost) if event.cost else 0,
            'requirements': event.requirements,
            'contact_person': event.contact_person,
            'contact_phone': event.contact_phone,
            'contact_email': event.contact_email,
            'status': event.status,
            'priority': event.priority,
            'featured_image': event.featured_image.url if event.featured_image else None,
            'gallery_images': event.gallery_images,
            'tags': event.tags,
            'notes': event.notes,
            'is_featured': event.is_featured,
            'views_count': event.views_count,
            'rating': float(event.rating) if event.rating else 0,
            'total_ratings': event.total_ratings,
            'published_at': event.published_at.strftime('%Y-%m-%d %H:%M') if event.published_at else None,
            'created_at': event.created_at.strftime('%Y-%m-%d %H:%M'),
            'created_by': event.created_by.username if event.created_by else '-'
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal memuat detail event: {str(e)}'
        }, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def event_create_api(request):
    """Create new event"""
    try:
        data = json.loads(request.body)
        
        with transaction.atomic():
            event = Event.objects.create(
                title=data['title'],
                category_id=data['category'],
                description=data['description'],
                short_description=data.get('short_description', ''),
                start_date=data['start_date'],
                end_date=data['end_date'],
                start_time=data['start_time'],
                end_time=data['end_time'],
                location=data['location'],
                address=data.get('address', ''),
                max_participants=data.get('max_participants', 0),
                allow_registration=data.get('allow_registration', True),
                is_free=data.get('is_free', True),
                cost=data.get('cost', 0),
                requirements=data.get('requirements', ''),
                contact_person=data.get('contact_person', ''),
                contact_phone=data.get('contact_phone', ''),
                contact_email=data.get('contact_email', ''),
                status=data.get('status', 'draft'),
                priority=data.get('priority', 'normal'),
                tags=data.get('tags', ''),
                notes=data.get('notes', ''),
                is_featured=data.get('is_featured', False),
                created_by=request.user
            )
            
            # Handle featured image if provided
            if 'featured_image' in data and data['featured_image']:
                # Handle file upload logic here
                pass
            
            return JsonResponse({
                'success': True,
                'message': 'Event berhasil dibuat',
                'event_id': event.id
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Gagal membuat event: {str(e)}'
        }, status=500)


@csrf_exempt
@login_required
@require_http_methods(["PUT"])
def event_update_api(request, event_id):
    """Update event"""
    try:
        event = get_object_or_404(Event, id=event_id)
        data = json.loads(request.body)
        
        with transaction.atomic():
            # Update fields
            event.title = data['title']
            event.category_id = data['category']
            event.description = data['description']
            event.short_description = data.get('short_description', '')
            event.start_date = data['start_date']
            event.end_date = data['end_date']
            event.start_time = data['start_time']
            event.end_time = data['end_time']
            event.location = data['location']
            event.address = data.get('address', '')
            event.max_participants = data.get('max_participants', 0)
            event.allow_registration = data.get('allow_registration', True)
            event.is_free = data.get('is_free', True)
            event.cost = data.get('cost', 0)
            event.requirements = data.get('requirements', '')
            event.contact_person = data.get('contact_person', '')
            event.contact_phone = data.get('contact_phone', '')
            event.contact_email = data.get('contact_email', '')
            event.status = data.get('status', 'draft')
            event.priority = data.get('priority', 'normal')
            event.tags = data.get('tags', '')
            event.notes = data.get('notes', '')
            event.is_featured = data.get('is_featured', False)
            
            event.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Event berhasil diupdate'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Gagal mengupdate event: {str(e)}'
        }, status=500)


@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def event_delete_api(request, event_id):
    """Delete event"""
    try:
        event = get_object_or_404(Event, id=event_id)
        
        # Check if event has participants
        if event.participants.exists():
            return JsonResponse({
                'success': False,
                'error': 'Event tidak dapat dihapus karena masih memiliki peserta'
            }, status=400)
        
        event.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Event berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Gagal menghapus event: {str(e)}'
        }, status=500)


# ============= CATEGORY API VIEWS =============

@login_required
def categories_list_api(request):
    """Get categories list"""
    try:
        categories = EventCategory.objects.filter(is_active=True).order_by('name')
        
        data = []
        for category in categories:
            data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'icon': category.icon,
                'color': category.color,
                'event_count': category.event_set.count()
            })
        
        return JsonResponse({'results': data})
        
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal memuat kategori: {str(e)}'
        }, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def category_create_api(request):
    """Create new category"""
    try:
        data = json.loads(request.body)
        
        category = EventCategory.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            icon=data.get('icon', ''),
            color=data.get('color', 'blue')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Kategori berhasil dibuat',
            'category_id': category.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Gagal membuat kategori: {str(e)}'
        }, status=500)


# ============= PARTICIPANT API VIEWS =============

@login_required
def participants_list_api(request):
    """Get participants list"""
    try:
        # Get parameters
        page = request.GET.get('page', 1)
        per_page = int(request.GET.get('per_page', 10))
        event_id = request.GET.get('event_id', '')
        status = request.GET.get('status', '')
        search = request.GET.get('search', '')
        
        # Base queryset
        participants = EventParticipant.objects.select_related('event', 'participant', 'created_by')
        
        # Apply filters
        if event_id:
            participants = participants.filter(event_id=event_id)
        
        if status:
            participants = participants.filter(status=status)
        
        if search:
            participants = participants.filter(
                Q(participant__nama__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search) |
                Q(event__title__icontains=search)
            )
        
        # Order by
        participants = participants.order_by('-registration_date')
        
        # Pagination
        paginator = Paginator(participants, per_page)
        page_obj = paginator.get_page(page)
        
        # Prepare data
        data = []
        for participant in page_obj:
            data.append({
                'id': participant.id,
                'event_title': participant.event.title,
                'participant_name': participant.participant.nama,
                'phone': participant.phone,
                'email': participant.email,
                'status': participant.status,
                'registration_source': participant.registration_source,
                'registration_date': participant.registration_date.strftime('%Y-%m-%d %H:%M'),
                'payment_status': participant.payment_status,
                'payment_amount': float(participant.payment_amount),
                'check_in_time': participant.check_in_time.strftime('%Y-%m-%d %H:%M') if participant.check_in_time else None,
                'created_by': participant.created_by.username if participant.created_by else '-'
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
        
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal memuat daftar peserta: {str(e)}'
        }, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def participant_create_api(request):
    """Create new participant"""
    try:
        data = json.loads(request.body)
        
        # Check if participant already exists for this event
        if EventParticipant.objects.filter(
            event_id=data['event_id'],
            participant_id=data['participant_id']
        ).exists():
            return JsonResponse({
                'success': False,
                'error': 'Peserta sudah terdaftar untuk event ini'
            }, status=400)
        
        participant = EventParticipant.objects.create(
            event_id=data['event_id'],
            participant_id=data['participant_id'],
            registration_source=data.get('registration_source', 'online'),
            status=data.get('status', 'pending'),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            emergency_contact=data.get('emergency_contact', ''),
            emergency_phone=data.get('emergency_phone', ''),
            special_needs=data.get('special_needs', ''),
            dietary_restrictions=data.get('dietary_restrictions', ''),
            payment_status=data.get('payment_status', 'unpaid'),
            payment_amount=data.get('payment_amount', 0),
            notes=data.get('notes', ''),
            created_by=request.user
        )
        
        # Update event participant count
        event = participant.event
        event.current_participants = event.participants.count()
        event.save(update_fields=['current_participants'])
        
        return JsonResponse({
            'success': True,
            'message': 'Peserta berhasil didaftarkan',
            'participant_id': participant.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Gagal mendaftarkan peserta: {str(e)}'
        }, status=500)


# ============= HELPER API VIEWS =============

@login_required
def get_events_for_dropdown(request):
    """Get events for dropdown selection"""
    try:
        events = Event.objects.filter(status='published').order_by('title')
        
        data = []
        for event in events:
            data.append({
                'id': event.id,
                'title': event.title,
                'start_date': event.start_date.strftime('%Y-%m-%d')
            })
        
        return JsonResponse({'results': data})
        
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal memuat events: {str(e)}'
        }, status=500)


@login_required
def get_penduduk_for_dropdown(request):
    """Get penduduk for dropdown selection"""
    try:
        search = request.GET.get('search', '')
        
        penduduk = Penduduk.objects.all()
        if search:
            penduduk = penduduk.filter(nama__icontains=search)
        
        penduduk = penduduk.order_by('nama')[:20]  # Limit results
        
        data = []
        for p in penduduk:
            data.append({
                'id': p.id,
                'nama': p.nama,
                'nik': p.nik,
                'alamat': p.alamat
            })
        
        return JsonResponse({'results': data})
        
    except Exception as e:
        return JsonResponse({
            'error': f'Gagal memuat penduduk: {str(e)}'
        }, status=500)


@login_required
def export_events_excel(request):
    """Export events to Excel"""
    try:
        # Get events data
        events = Event.objects.select_related('category').order_by('-start_date')
        
        # Create Excel file logic here
        # This is a placeholder - implement actual Excel export
        
        return JsonResponse({
            'success': True,
            'message': 'Export Excel berhasil dibuat'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Gagal export Excel: {str(e)}'
        }, status=500)


@login_required
def export_events_pdf(request):
    """Export events to PDF"""
    try:
        # Get events data
        events = Event.objects.select_related('category').order_by('-start_date')
        
        # Create PDF file logic here
        # This is a placeholder - implement actual PDF export
        
        return JsonResponse({
            'success': True,
            'message': 'Export PDF berhasil dibuat'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Gagal export PDF: {str(e)}'
        }, status=500)
