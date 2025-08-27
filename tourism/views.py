from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
import json

from .models import (
    TourismCategory, TourismLocation, TourismGallery, 
    TourismReview, TourismRating, TourismEvent, 
    TourismPackage, TourismFAQ
)
from .forms import (
    TourismCategoryForm, TourismLocationForm, TourismGalleryForm,
    TourismReviewForm, TourismRatingForm, TourismEventForm,
    TourismPackageForm, TourismFAQForm
)

# ==================== DASHBOARD & LIST VIEWS ====================

def tourism_dashboard(request):
    """Dashboard utama untuk wisata"""
    context = {
        'total_locations': TourismLocation.objects.filter(is_active=True).count(),
        'total_categories': TourismCategory.objects.filter(is_active=True).count(),
        'featured_locations': TourismLocation.objects.filter(featured=True, is_active=True)[:6],
        'recent_locations': TourismLocation.objects.filter(is_active=True).order_by('-created_at')[:6],
        'upcoming_events': TourismEvent.objects.filter(
            start_date__gte=timezone.now(),
            is_active=True
        ).order_by('start_date')[:5],
        'categories': TourismCategory.objects.filter(is_active=True)[:8],
    }
    return render(request, 'tourism/dashboard.html', context)

def tourism_list(request):
    """Daftar semua lokasi wisata"""
    locations = TourismLocation.objects.filter(is_active=True, status='published')
    
    # Filtering
    category_id = request.GET.get('category')
    location_type = request.GET.get('type')
    search_query = request.GET.get('search')
    
    if category_id:
        locations = locations.filter(category_id=category_id)
    
    if location_type:
        locations = locations.filter(location_type=location_type)
    
    if search_query:
        locations = locations.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(locations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'locations': page_obj,
        'categories': TourismCategory.objects.filter(is_active=True),
        'location_types': TourismLocation.LOCATION_TYPE_CHOICES,
        'current_category': category_id,
        'current_type': location_type,
        'search_query': search_query,
    }
    return render(request, 'tourism/location_list.html', context)

def tourism_detail(request, slug):
    """Detail lokasi wisata"""
    location = get_object_or_404(TourismLocation, slug=slug, is_active=True, status='published')
    
    # Get related data
    gallery = location.gallery.filter(is_active=True).order_by('order')
    reviews = location.reviews.filter(is_approved=True).order_by('-created_at')
    events = location.events.filter(is_active=True, start_date__gte=timezone.now()).order_by('start_date')
    packages = location.packages.filter(is_active=True).order_by('price')
    faqs = location.faqs.filter(is_active=True).order_by('order')
    
    # Get user's existing review and rating
    user_review = None
    user_rating = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        user_rating = location.ratings.filter(user=request.user).first()
    
    context = {
        'location': location,
        'gallery': gallery,
        'reviews': reviews,
        'events': events,
        'packages': packages,
        'faqs': faqs,
        'user_review': user_review,
        'user_rating': user_rating,
        'review_form': TourismReviewForm(),
        'rating_form': TourismRatingForm(),
    }
    return render(request, 'tourism/location_detail.html', context)

# ==================== CATEGORY VIEWS ====================

def category_list(request):
    """Daftar kategori wisata"""
    categories = TourismCategory.objects.filter(is_active=True)
    context = {
        'categories': categories,
    }
    return render(request, 'tourism/category_list.html', context)

def category_detail(request, category_id):
    """Detail kategori dengan daftar lokasi wisata"""
    category = get_object_or_404(TourismCategory, id=category_id, is_active=True)
    locations = TourismLocation.objects.filter(
        category=category, 
        is_active=True, 
        status='published'
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(locations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'locations': page_obj,
    }
    return render(request, 'tourism/category_detail.html', context)

# ==================== EVENT VIEWS ====================

def event_list(request):
    """Daftar semua event wisata"""
    events = TourismEvent.objects.filter(is_active=True)
    
    # Filtering
    event_type = request.GET.get('type')
    upcoming = request.GET.get('upcoming', 'true')
    
    if event_type:
        events = events.filter(event_type=event_type)
    
    if upcoming == 'true':
        events = events.filter(start_date__gte=timezone.now())
    elif upcoming == 'false':
        events = events.filter(start_date__lt=timezone.now())
    
    events = events.order_by('start_date')
    
    # Pagination
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'events': page_obj,
        'event_types': TourismEvent.EVENT_TYPE_CHOICES,
        'current_type': event_type,
        'upcoming': upcoming,
    }
    return render(request, 'tourism/event_list.html', context)

def event_detail(request, event_id):
    """Detail event wisata"""
    event = get_object_or_404(TourismEvent, id=event_id, is_active=True)
    context = {
        'event': event,
    }
    return render(request, 'tourism/event_detail.html', context)

# ==================== PACKAGE VIEWS ====================

def package_list(request):
    """Daftar semua paket wisata"""
    packages = TourismPackage.objects.filter(is_active=True)
    
    # Filtering
    package_type = request.GET.get('type')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    if package_type:
        packages = packages.filter(package_type=package_type)
    
    if price_min:
        packages = packages.filter(price__gte=float(price_min))
    
    if price_max:
        packages = packages.filter(price__lte=float(price_max))
    
    packages = packages.order_by('price')
    
    # Pagination
    paginator = Paginator(packages, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'packages': page_obj,
        'package_types': TourismPackage.PACKAGE_TYPE_CHOICES,
        'current_type': package_type,
        'price_min': price_min,
        'price_max': price_max,
    }
    return render(request, 'tourism/package_list.html', context)

def package_detail(request, package_id):
    """Detail paket wisata"""
    package = get_object_or_404(TourismPackage, id=package_id, is_active=True)
    context = {
        'package': package,
    }
    return render(request, 'tourism/package_detail.html', context)

# ==================== REVIEW & RATING VIEWS ====================

@login_required
def submit_review(request, location_id):
    """Submit review untuk lokasi wisata"""
    if request.method == 'POST':
        location = get_object_or_404(TourismLocation, id=location_id)
        form = TourismReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.tourism_location = location
            review.user = request.user
            review.is_approved = True  # Auto-approve for now
            review.save()
            
            messages.success(request, 'Review berhasil dikirim!')
        else:
            messages.error(request, 'Terjadi kesalahan dalam mengirim review.')
    
    return redirect('tourism:location_detail', slug=location.location.slug)

@login_required
def submit_rating(request, location_id):
    """Submit rating untuk lokasi wisata"""
    if request.method == 'POST':
        location = get_object_or_404(TourismLocation, id=location_id)
        form = TourismRatingForm(request.POST)
        
        if form.is_valid():
            rating, created = TourismRating.objects.update_or_create(
                tourism_location=location,
                user=request.user,
                defaults=form.cleaned_data
            )
            
            messages.success(request, 'Rating berhasil disimpan!')
        else:
            messages.error(request, 'Terjadi kesalahan dalam menyimpan rating.')
    
    return redirect('tourism:location_detail', slug=location.slug)

# ==================== SEARCH & FILTER VIEWS ====================

def search_tourism(request):
    """Search wisata dengan filter advanced"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    location_type = request.GET.get('type', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    rating = request.GET.get('rating', '')
    
    locations = TourismLocation.objects.filter(is_active=True, status='published')
    
    if query:
        locations = locations.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(full_description__icontains=query) |
            Q(address__icontains=query)
        )
    
    if category:
        locations = locations.filter(category_id=category)
    
    if location_type:
        locations = locations.filter(location_type=location_type)
    
    if rating:
        locations = locations.filter(ratings__rating__gte=int(rating))
    
    # Remove duplicates
    locations = locations.distinct()
    
    # Pagination
    paginator = Paginator(locations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'locations': page_obj,
        'categories': TourismCategory.objects.filter(is_active=True),
        'location_types': TourismLocation.LOCATION_TYPE_CHOICES,
        'search_params': {
            'q': query,
            'category': category,
            'type': location_type,
            'rating': rating,
        }
    }
    return render(request, 'tourism/search_results.html', context)

# ==================== API VIEWS ====================

@csrf_exempt
def api_locations(request):
    """API endpoint untuk daftar lokasi wisata"""
    if request.method == 'GET':
        locations = TourismLocation.objects.filter(is_active=True, status='published')
        
        # Basic filtering
        category = request.GET.get('category')
        if category:
            locations = locations.filter(category_id=category)
        
        # Convert to JSON
        data = []
        for location in locations[:50]:  # Limit to 50 results
            data.append({
                'id': location.id,
                'title': location.title,
                'slug': location.slug,
                'short_description': location.short_description,
                'address': location.address,
                'category': location.category.name,
                'location_type': location.location_type,
                'average_rating': location.average_rating,
                'total_reviews': location.total_reviews,
                'image_url': location.gallery.filter(is_featured=True).first().image.url if location.gallery.filter(is_featured=True).first() else None,
            })
        
        return JsonResponse({'locations': data})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_location_detail(request, location_id):
    """API endpoint untuk detail lokasi wisata"""
    if request.method == 'GET':
        try:
            location = TourismLocation.objects.get(id=location_id, is_active=True, status='published')
            
            # Get gallery
            gallery = []
            for item in location.gallery.filter(is_active=True):
                gallery.append({
                    'id': item.id,
                    'title': item.title,
                    'media_type': item.media_type,
                    'image_url': item.image.url if item.image else None,
                    'video_url': item.video_url,
                    'caption': item.caption,
                })
            
            # Get reviews
            reviews = []
            for review in location.reviews.filter(is_approved=True)[:10]:
                reviews.append({
                    'id': review.id,
                    'user': review.user.username,
                    'rating': review.rating,
                    'title': review.title,
                    'comment': review.comment,
                    'visit_date': review.visit_date.isoformat() if review.visit_date else None,
                    'created_at': review.created_at.isoformat(),
                })
            
            data = {
                'id': location.id,
                'title': location.title,
                'slug': location.slug,
                'short_description': location.short_description,
                'full_description': location.full_description,
                'address': location.address,
                'latitude': float(location.latitude) if location.latitude else None,
                'longitude': float(location.longitude) if location.longitude else None,
                'opening_hours': location.opening_hours,
                'entry_fee': float(location.entry_fee) if location.entry_fee else None,
                'contact_phone': location.contact_phone,
                'contact_email': location.contact_email,
                'website': location.website,
                'category': location.category.name,
                'location_type': location.location_type,
                'average_rating': location.average_rating,
                'total_reviews': location.total_reviews,
                'gallery': gallery,
                'reviews': reviews,
            }
            
            return JsonResponse(data)
        
        except TourismLocation.DoesNotExist:
            return JsonResponse({'error': 'Location not found'}, status=404)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# ==================== ADMIN VIEWS ====================

@login_required
def admin_dashboard(request):
    """Dashboard admin untuk wisata"""
    context = {
        'total_locations': TourismLocation.objects.count(),
        'total_categories': TourismCategory.objects.count(),
        'total_reviews': TourismReview.objects.count(),
        'total_events': TourismEvent.objects.count(),
        'total_packages': TourismPackage.objects.count(),
        'recent_locations': TourismLocation.objects.order_by('-created_at')[:5],
        'pending_reviews': TourismReview.objects.filter(is_approved=False)[:5],
        'upcoming_events': TourismEvent.objects.filter(
            start_date__gte=timezone.now(),
            is_active=True
        ).order_by('start_date')[:5],
    }
    return render(request, 'tourism/admin/dashboard.html', context)

@login_required
def admin_location_list(request):
    """Admin list lokasi wisata"""
    locations = TourismLocation.objects.all().order_by('-created_at')
    
    # Search
    search = request.GET.get('search', '')
    if search:
        locations = locations.filter(
            Q(title__icontains=search) |
            Q(category__name__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(locations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'locations': page_obj,
        'search': search,
    }
    return render(request, 'tourism/admin/location_list.html', context)

@login_required
def admin_location_create(request):
    """Admin create lokasi wisata"""
    if request.method == 'POST':
        form = TourismLocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.created_by = request.user
            location.updated_by = request.user
            location.save()
            messages.success(request, 'Lokasi wisata berhasil dibuat!')
            return redirect('tourism:admin_location_list')
    else:
        form = TourismLocationForm()
    
    context = {
        'form': form,
        'title': 'Tambah Lokasi Wisata Baru',
    }
    return render(request, 'tourism/admin/location_form.html', context)

@login_required
def admin_location_edit(request, location_id):
    """Admin edit lokasi wisata"""
    location = get_object_or_404(TourismLocation, id=location_id)
    
    if request.method == 'POST':
        form = TourismLocationForm(request.POST, instance=location)
        if form.is_valid():
            location = form.save(commit=False)
            location.updated_by = request.user
            location.save()
            messages.success(request, 'Lokasi wisata berhasil diupdate!')
            return redirect('tourism:admin_location_list')
    else:
        form = TourismLocationForm(instance=location)
    
    context = {
        'form': form,
        'location': location,
        'title': f'Edit Lokasi Wisata: {location.title}',
    }
    return render(request, 'tourism/admin/location_form.html', context)

@login_required
def admin_location_delete(request, location_id):
    """Admin delete lokasi wisata"""
    location = get_object_or_404(TourismLocation, id=location_id)
    
    if request.method == 'POST':
        location.delete()
        messages.success(request, 'Lokasi wisata berhasil dihapus!')
        return redirect('tourism:admin_location_list')
    
    context = {
        'location': location,
    }
    return render(request, 'tourism/admin/location_confirm_delete.html', context)

# ==================== HELPER FUNCTIONS ====================

def get_tourism_stats():
    """Get statistics for tourism"""
    stats = {
        'total_locations': TourismLocation.objects.filter(is_active=True).count(),
        'total_categories': TourismCategory.objects.filter(is_active=True).count(),
        'total_reviews': TourismReview.objects.filter(is_approved=True).count(),
        'total_events': TourismEvent.objects.filter(is_active=True).count(),
        'total_packages': TourismPackage.objects.filter(is_active=True).count(),
        'average_rating': TourismRating.objects.aggregate(Avg('rating'))['rating__avg'] or 0,
        'top_categories': TourismCategory.objects.filter(
            is_active=True
        ).annotate(
            location_count=Count('tourismlocation')
        ).order_by('-location_count')[:5],
    }
    return stats
