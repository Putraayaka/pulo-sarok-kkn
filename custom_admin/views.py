from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json

# Import models from all apps
from references.models import Penduduk, Dusun, Lorong
from organization.models import PerangkatDesa, LembagaAdat, PenggerakPKK, Kepemudaan, KarangTaruna
from business.models import Business
from news.models import News
from letters.models import Letter
from beneficiaries.models import Beneficiary
from posyandu.models import PosyanduLocation
from village_profile.models import VillageHistory, VillageHistoryPhoto
from documents.models import Document
from core.models import CustomUser

def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Main admin dashboard"""
    context = {
        'page_title': 'Dashboard Admin',
        'page_subtitle': 'Kelola data desa Pulosarok'
    }
    return render(request, 'admin/dashboard.html', context)

def admin_login_view(request):
    """Admin login view"""
    # Redirect if user is already logged in and is admin
    if request.user.is_authenticated and is_admin(request.user):
        return redirect('custom_admin:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and is_admin(user):
            login(request, user)
            return redirect('custom_admin:dashboard')
        else:
            messages.error(request, 'Username atau password salah, atau Anda tidak memiliki akses admin.')
    
    return render(request, 'admin/login.html')

@login_required
def admin_logout_view(request):
    """Admin logout view"""
    logout(request)
    return redirect('custom_admin:login')

# API Endpoints
@login_required
@user_passes_test(is_admin)
def dashboard_stats_api(request):
    """API endpoint for dashboard statistics"""
    try:
        # Get statistics (using is_active filter for consistency)
        total_penduduk = Penduduk.objects.filter(is_active=True).count()
        total_dusun = Dusun.objects.filter(is_active=True).count()
        # Count all organization types
        total_perangkat = PerangkatDesa.objects.count()
        total_lembaga_adat = LembagaAdat.objects.count()
        total_pkk = PenggerakPKK.objects.count()
        total_kepemudaan = Kepemudaan.objects.count()
        total_karang_taruna = KarangTaruna.objects.count()
        total_organisasi = total_perangkat + total_lembaga_adat + total_pkk + total_kepemudaan + total_karang_taruna
        total_umkm = Business.objects.count()
        
        # Gender statistics (using is_active filter for consistency)
        male_count = Penduduk.objects.filter(gender='L', is_active=True).count()
        female_count = Penduduk.objects.filter(gender='P', is_active=True).count()
        
        # Calculate percentages
        total_gender = male_count + female_count
        male_percentage = (male_count / total_gender * 100) if total_gender > 0 else 0
        female_percentage = (female_count / total_gender * 100) if total_gender > 0 else 0
        
        # Age groups (approximate based on birth date, using is_active filter)
        today = timezone.now().date()
        age_0_17 = Penduduk.objects.filter(
            birth_date__gte=today - timedelta(days=17*365),
            is_active=True
        ).count()
        age_18_60 = Penduduk.objects.filter(
            birth_date__lt=today - timedelta(days=17*365),
            birth_date__gte=today - timedelta(days=60*365),
            is_active=True
        ).count()
        age_60_plus = Penduduk.objects.filter(
            birth_date__lt=today - timedelta(days=60*365),
            is_active=True
        ).count()
        
        # Calculate average population per dusun
        avg_population_per_dusun = round(total_penduduk / total_dusun, 0) if total_dusun > 0 else 0
        
        data = {
            'total_penduduk': total_penduduk,
            'total_dusun': total_dusun,
            'total_organisasi': total_organisasi,
            'total_umkm': total_umkm,
            'male_count': male_count,
            'female_count': female_count,
            'male_percentage': round(male_percentage, 1),
            'female_percentage': round(female_percentage, 1),
            'age_0_17': age_0_17,
            'age_18_60': age_18_60,
            'age_60_plus': age_60_plus,
            'avg_population_per_dusun': avg_population_per_dusun
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
def recent_activities_api(request):
    """API endpoint for recent activities"""
    try:
        activities = []
        
        # Recent news - temporarily commented out
        # recent_news = News.objects.filter(
        #     created_at__gte=timezone.now() - timedelta(days=7)
        # ).order_by('-created_at')[:3]
        # 
        # for news in recent_news:
        #     activities.append({
        #         'description': f'Berita "{news.title}" dipublikasikan',
        #         'time_ago': get_time_ago(news.created_at),
        #         'icon': 'fas fa-newspaper text-green-600',
        #         'color': 'bg-green-100'
        #     })
        
        # Recent letters
        recent_letters = Letter.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).order_by('-created_at')[:3]
        
        for letter in recent_letters:
            activities.append({
                'description': f'Surat "{letter.subject}" dibuat',
                'time_ago': get_time_ago(letter.created_at),
                'icon': 'fas fa-envelope text-purple-600',
                'color': 'bg-purple-100'
            })
        
        # Recent organizations - check all organization types
        recent_perangkat = PerangkatDesa.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).order_by('-created_at')[:1]
        
        for perangkat in recent_perangkat:
            activities.append({
                'description': f'Perangkat Desa "{perangkat.nama}" ditambahkan',
                'time_ago': get_time_ago(perangkat.created_at),
                'icon': 'fas fa-users text-blue-600',
                'color': 'bg-blue-100'
            })
        
        recent_lembaga = LembagaAdat.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).order_by('-created_at')[:1]
        
        for lembaga in recent_lembaga:
            activities.append({
                'description': f'Lembaga Adat "{lembaga.nama_lembaga}" ditambahkan',
                'time_ago': get_time_ago(lembaga.created_at),
                'icon': 'fas fa-users text-green-600',
                'color': 'bg-green-100'
            })
        
        # Sort by time and limit to 5
        activities = sorted(activities, key=lambda x: x['time_ago'])[:5]
        
        return JsonResponse({'activities': activities})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_time_ago(datetime_obj):
    """Helper function to get human readable time ago"""
    now = timezone.now()
    diff = now - datetime_obj
    
    if diff.days > 0:
        return f"{diff.days} hari yang lalu"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} jam yang lalu"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} menit yang lalu"
    else:
        return "Baru saja"

# Module Management Views
@login_required
@user_passes_test(is_admin)
def module_view(request, module_name):
    """Generic module view for different apps"""
    module_config = {
        'references': {
            'title': 'Manajemen Referensi',
            'subtitle': 'Kelola data penduduk, dusun, dan lorong',
            'template': 'admin/modules/references/index.html'
        },
        'village_profile': {
            'title': 'Profil Desa',
            'subtitle': 'Kelola informasi profil desa',
            'template': 'admin/modules/village_profile/index.html'
        },
        'organization': {
            'title': 'Organisasi',
            'subtitle': 'Kelola data organisasi desa',
            'template': 'admin/modules/organization/index.html'
        },
        'business': {
            'title': 'UMKM',
            'subtitle': 'Kelola data usaha mikro kecil menengah',
            'template': 'admin/modules/business/index.html'
        },
        'news': {
            'title': 'Berita',
            'subtitle': 'Kelola berita dan pengumuman',
            'template': 'admin/modules/news/index.html'
        },
        'letters': {
            'title': 'Surat Menyurat',
            'subtitle': 'Kelola surat keterangan dan dokumen',
            'template': 'admin/modules/letters/index.html'
        },
        'documents': {
            'title': 'Dokumen',
            'subtitle': 'Kelola dokumen dan file',
            'template': 'admin/modules/documents/index.html'
        },
        'beneficiaries': {
            'title': 'Penerima Bantuan',
            'subtitle': 'Kelola data penerima bantuan',
            'template': 'admin/modules/beneficiaries/index.html'
        },
        'posyandu': {
            'title': 'Posyandu',
            'subtitle': 'Kelola data posyandu',
            'template': 'admin/modules/posyandu/index.html'
        },
        'events': {
            'title': 'Events',
            'subtitle': 'Kelola acara dan kegiatan desa',
            'template': 'admin/modules/events/index.html'
        },
        'services': {
            'title': 'Layanan Desa',
            'subtitle': 'Kelola layanan dan fasilitas desa',
            'template': 'admin/modules/services/index.html'
        },
        'core': {
            'title': 'Pengaturan Sistem',
            'subtitle': 'Kelola pengaturan dan konfigurasi',
            'template': 'admin/modules/core/index.html'
        }
    }
    
    if module_name not in module_config:
        messages.error(request, 'Modul tidak ditemukan')
        return redirect('custom_admin:dashboard')
    
    config = module_config[module_name]
    context = {
        'page_title': config['title'],
        'page_subtitle': config['subtitle'],
        'module_name': module_name
    }
    
    # Special handling for news module to include statistics
    if module_name == 'news':
        print("DEBUG - Accessing news module dashboard")
        try:
            from news.models import News, NewsComment, Announcement
            from django.db.models import Count
            
            # Calculate statistics
            total_news = News.objects.count()
            published_news = News.objects.filter(status='published').count()
            draft_news = News.objects.filter(status='draft').count()
            scheduled_news = News.objects.filter(status='scheduled').count()
            print(f"DEBUG - News stats: Total={total_news}, Published={published_news}, Draft={draft_news}, Scheduled={scheduled_news}")
            total_comments = NewsComment.objects.count()
            total_announcements = Announcement.objects.count()
            
            # Get recent news
            recent_news = News.objects.select_related('author', 'category').order_by('-created_at')[:5]
            
            # Get popular news (by views)
            popular_news = News.objects.select_related('author', 'category').annotate(
                total_views=Count('view_records')
            ).order_by('-total_views')[:5]
            
            context.update({
                'total_news': total_news,
                'published_news': published_news,
                'draft_news': draft_news,
                'scheduled_news': scheduled_news,
                'total_comments': total_comments,
                'total_announcements': total_announcements,
                'recent_news': recent_news,
                'popular_news': popular_news,
            })
            
            print(f"DEBUG - News statistics: total={total_news}, published={published_news}, draft={draft_news}, scheduled={scheduled_news}, comments={total_comments}")
            
        except ImportError as e:
            print(f"DEBUG - Error importing news models: {e}")
            # Set default values if models can't be imported
            context.update({
                'total_news': 0,
                'published_news': 0,
                'draft_news': 0,
                'scheduled_news': 0,
                'total_comments': 0,
                'total_announcements': 0,
                'recent_news': [],
                'popular_news': [],
            })
    
    return render(request, config['template'], context)

@login_required
@user_passes_test(is_admin)
def search_global(request):
    """Global search across all modules"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'results': []})
    
    results = []
    
    # Search in Penduduk
    penduduk_results = Penduduk.objects.filter(
        Q(nama__icontains=query) | Q(nik__icontains=query)
    )[:5]
    
    for p in penduduk_results:
        results.append({
            'title': p.nama,
            'subtitle': f'NIK: {p.nik}',
            'module': 'references',
            'type': 'penduduk',
            'id': p.id
        })
    
    # Search in Organizations (PerangkatDesa, LembagaAdat, etc.)
    perangkat_results = PerangkatDesa.objects.filter(nama__icontains=query)[:5]
    for org in perangkat_results:
        results.append({
            'title': org.nama,
            'subtitle': org.jabatan or 'Perangkat Desa',
            'module': 'organization',
            'type': 'perangkat_desa',
            'id': org.id
        })
    
    # Search in News - temporarily commented out
    # news_results = News.objects.filter(
    #     Q(title__icontains=query) | Q(content__icontains=query)
    # )[:5]
    # 
    # for news in news_results:
    #     results.append({
    #         'title': news.title,
    #         'subtitle': 'Berita',
    #         'module': 'news',
    #         'type': 'news',
    #         'id': news.id
    #     })
    
    return JsonResponse({'results': results})

@login_required
@user_passes_test(is_admin)
def system_info_api(request):
    """API endpoint for system information"""
    try:
        # Get system statistics
        total_users = CustomUser.objects.count()
        active_users = CustomUser.objects.filter(is_active=True).count()
        
        # Database size (approximate) - using active records for consistency
        total_records = (
            Penduduk.objects.filter(is_active=True).count() +
            Dusun.objects.filter(is_active=True).count() +
            Lorong.objects.filter(is_active=True).count() +
            PerangkatDesa.objects.count() +
            LembagaAdat.objects.count() +
            PenggerakPKK.objects.count() +
            Kepemudaan.objects.count() +
            KarangTaruna.objects.count() +
            Business.objects.count() +
            # News.objects.count() +  # Temporarily commented out
            Letter.objects.count() +
            Beneficiary.objects.count() +
            PosyanduLocation.objects.count() +
            Document.objects.count()
        )
        
        data = {
            'total_users': total_users,
            'active_users': active_users,
            'total_records': total_records,
            'server_status': 'online',
            'database_status': 'connected',
            'last_backup': 'Manual backup required'
        }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_admin)
def admin_profile(request):
    """Admin profile management"""
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'profile':
            # Update profile information
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            
            return JsonResponse({'success': True, 'message': 'Profil berhasil diperbarui'})
            
        elif form_type == 'password':
            # Change password
            from django.contrib.auth import update_session_auth_hash
            from django.contrib.auth.forms import PasswordChangeForm
            
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            
            # Verify current password
            if not request.user.check_password(current_password):
                return JsonResponse({'success': False, 'message': 'Password saat ini salah'})
            
            # Update password
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            
            return JsonResponse({'success': True, 'message': 'Password berhasil diubah'})
    
    context = {
        'page_title': 'Profil Admin',
        'page_subtitle': 'Kelola informasi profil Anda'
    }
    return render(request, 'admin/profile.html', context)

@login_required
@user_passes_test(is_admin)
def admin_settings(request):
    """Admin settings management"""
    context = {
        'page_title': 'Pengaturan Sistem',
        'page_subtitle': 'Kelola pengaturan dan konfigurasi sistem'
    }
    return render(request, 'admin/settings.html', context)