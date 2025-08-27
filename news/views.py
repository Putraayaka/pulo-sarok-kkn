from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.urls import reverse
import json
import csv
import openpyxl
from io import BytesIO
from datetime import datetime, timedelta

from .models import (
    NewsCategory, NewsTag, News, NewsComment, NewsView, 
    NewsImage, NewsLike, NewsShare
)
from .forms import (
    NewsCategoryForm, NewsTagForm, NewsForm, NewsCommentForm, 
    NewsSearchForm, NewsImageForm, NewsImageFormSet, 
    NewsCommentModerationForm, BulkNewsActionForm, NewsImportForm
)


@login_required
def news_admin(request):
    """Main admin view for news management"""
    # Get statistics
    total_news = News.objects.count()
    published_news = News.objects.filter(status='published').count()
    draft_news = News.objects.filter(status='draft').count()
    scheduled_news = News.objects.filter(status='scheduled').count()
    total_views = NewsView.objects.count()
    total_likes = NewsLike.objects.count()
    total_comments = NewsComment.objects.filter(moderation_status='approved').count()
    
    # Recent news
    recent_news = News.objects.select_related('category', 'author').order_by('-created_at')[:5]
    
    # Popular news (by views)
    popular_news = News.objects.filter(status='published').order_by('-views_count')[:5]
    
    # Recent comments
    recent_comments = NewsComment.objects.select_related('news').filter(
        moderation_status='pending'
    ).order_by('-created_at')[:5]
    
    context = {
        'page_title': 'Berita',
        'page_subtitle': 'Kelola berita dan artikel desa',
        'total_news': total_news,
        'published_news': published_news,
        'draft_news': draft_news,
        'scheduled_news': scheduled_news,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'recent_news': recent_news,
        'popular_news': popular_news,
        'recent_comments': recent_comments,
    }
    
    return render(request, 'admin/modules/news/index.html', context)


@login_required
def news_list(request):
    """List all news with filtering and pagination"""
    news_list = News.objects.select_related('category', 'author').prefetch_related('tags')
    
    # Search and filtering
    search_form = NewsSearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        tags = search_form.cleaned_data.get('tags')
        date_from = search_form.cleaned_data.get('date_from')
        date_to = search_form.cleaned_data.get('date_to')
        
        if query:
            news_list = news_list.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(excerpt__icontains=query)
            )
        
        if category:
            news_list = news_list.filter(category=category)
        
        if tags:
            news_list = news_list.filter(tags__in=tags).distinct()
        
        if date_from:
            news_list = news_list.filter(created_at__gte=date_from)
        
        if date_to:
            news_list = news_list.filter(created_at__lte=date_to)
    
    # Status filtering
    status = request.GET.get('status')
    if status:
        news_list = news_list.filter(status=status)
    
    # Ordering
    order_by = request.GET.get('order_by', '-created_at')
    news_list = news_list.order_by(order_by)
    
    # Pagination
    paginator = Paginator(news_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Bulk action form
    bulk_form = BulkNewsActionForm()
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'bulk_form': bulk_form,
        'current_status': status,
        'current_order': order_by,
    }
    
    return render(request, 'admin/modules/news/list.html', context)


@login_required
def news_create(request):
    """Create new news"""
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        image_formset = NewsImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and image_formset.is_valid():
            with transaction.atomic():
                news = form.save(commit=False)
                news.author = request.user
                news.slug = slugify(news.title)
                
                # Calculate reading time
                news.reading_time = news.calculate_reading_time()
                
                news.save()
                form.save_m2m()  # Save many-to-many relationships (tags)
                
                # Save images
                image_formset.instance = news
                image_formset.save()
                
                messages.success(request, f'Berita "{news.title}" berhasil dibuat.')
                return redirect('news:detail', pk=news.pk)
    else:
        form = NewsForm()
        image_formset = NewsImageFormSet()
    
    context = {
        'form': form,
        'image_formset': image_formset,
        'action': 'create',
    }
    
    return render(request, 'admin/modules/news/form.html', context)


@login_required
def news_detail(request, pk):
    """View news detail"""
    news = get_object_or_404(News.objects.select_related('category', 'author').prefetch_related('tags', 'images'), pk=pk)
    
    # Get comments
    comments = news.comments.filter(moderation_status='approved').order_by('-created_at')
    pending_comments = news.comments.filter(moderation_status='pending').count()
    
    # Get related news
    related_news = News.objects.filter(
        category=news.category,
        status='published'
    ).exclude(pk=news.pk)[:5]
    
    context = {
        'news': news,
        'comments': comments,
        'pending_comments': pending_comments,
        'related_news': related_news,
    }
    
    return render(request, 'admin/modules/news/detail.html', context)


@login_required
def news_edit(request, pk):
    """Edit existing news"""
    news = get_object_or_404(News, pk=pk)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        image_formset = NewsImageFormSet(request.POST, request.FILES, instance=news)
        
        if form.is_valid() and image_formset.is_valid():
            with transaction.atomic():
                news = form.save(commit=False)
                
                # Update slug if title changed
                if 'title' in form.changed_data:
                    news.slug = slugify(news.title)
                
                # Recalculate reading time if content changed
                if 'content' in form.changed_data:
                    news.reading_time = news.calculate_reading_time()
                
                news.save()
                form.save_m2m()
                
                # Save images
                image_formset.save()
                
                messages.success(request, f'Berita "{news.title}" berhasil diperbarui.')
                return redirect('news:detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
        image_formset = NewsImageFormSet(instance=news)
    
    context = {
        'form': form,
        'image_formset': image_formset,
        'news': news,
        'action': 'edit',
    }
    
    return render(request, 'admin/modules/news/form.html', context)


@login_required
@require_POST
def news_delete(request, pk):
    """Delete news"""
    news = get_object_or_404(News, pk=pk)
    title = news.title
    
    # Delete associated images from storage
    for image in news.images.all():
        if image.image:
            default_storage.delete(image.image.name)
        if image.thumbnail:
            default_storage.delete(image.thumbnail.name)
    
    news.delete()
    messages.success(request, f'Berita "{title}" berhasil dihapus.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': f'Berita "{title}" berhasil dihapus.'})
    
    return redirect('news:list')


@login_required
@require_POST
def news_bulk_action(request):
    """Handle bulk actions on news"""
    form = BulkNewsActionForm(request.POST)
    
    if form.is_valid():
        action = form.cleaned_data['action']
        selected_ids = form.cleaned_data['selected_news'].split(',')
        
        try:
            selected_ids = [int(id.strip()) for id in selected_ids if id.strip()]
            news_queryset = News.objects.filter(id__in=selected_ids)
            
            if action == 'publish':
                news_queryset.update(status='published', published_date=timezone.now())
                messages.success(request, f'{news_queryset.count()} berita berhasil dipublikasikan.')
            
            elif action == 'draft':
                news_queryset.update(status='draft')
                messages.success(request, f'{news_queryset.count()} berita berhasil dijadikan draft.')
            
            elif action == 'archive':
                news_queryset.update(status='archived')
                messages.success(request, f'{news_queryset.count()} berita berhasil diarsipkan.')
            
            elif action == 'featured':
                news_queryset.update(is_featured=True)
                messages.success(request, f'{news_queryset.count()} berita berhasil dijadikan featured.')
            
            elif action == 'unfeatured':
                news_queryset.update(is_featured=False)
                messages.success(request, f'{news_queryset.count()} berita berhasil dihapus dari featured.')
            
            elif action == 'delete':
                # Delete associated images
                for news in news_queryset:
                    for image in news.images.all():
                        if image.image:
                            default_storage.delete(image.image.name)
                        if image.thumbnail:
                            default_storage.delete(image.thumbnail.name)
                
                count = news_queryset.count()
                news_queryset.delete()
                messages.success(request, f'{count} berita berhasil dihapus.')
            
        except ValueError:
            messages.error(request, 'ID berita tidak valid.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
    
    return redirect('news:list')


@csrf_exempt
@require_POST
def news_like(request, pk):
    """Like/unlike news"""
    news = get_object_or_404(News, pk=pk)
    
    # Get user info
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    session_key = request.session.session_key
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Check if already liked
    like_filter = {'news': news}
    if user:
        like_filter['user'] = user
    else:
        like_filter['ip_address'] = ip_address
        like_filter['session_key'] = session_key
    
    existing_like = NewsLike.objects.filter(**like_filter).first()
    
    if existing_like:
        # Unlike
        existing_like.delete()
        liked = False
    else:
        # Like
        NewsLike.objects.create(
            news=news,
            user=user,
            ip_address=ip_address,
            session_key=session_key,
            user_agent=user_agent
        )
        liked = True
    
    # Update likes count
    news.update_likes_count()
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes_count': news.likes_count
    })


@csrf_exempt
@require_POST
def news_share(request, pk):
    """Record news share"""
    news = get_object_or_404(News, pk=pk)
    platform = request.POST.get('platform', 'unknown')
    
    # Get user info
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get('REMOTE_ADDR')
    session_key = request.session.session_key
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    referrer = request.META.get('HTTP_REFERER', '')
    
    # Record share
    NewsShare.objects.create(
        news=news,
        platform=platform,
        user=user,
        ip_address=ip_address,
        session_key=session_key,
        user_agent=user_agent,
        referrer=referrer
    )
    
    # Update shares count
    news.update_shares_count()
    
    return JsonResponse({
        'success': True,
        'shares_count': news.shares_count
    })


@login_required
def news_comments(request, pk):
    """Manage news comments"""
    news = get_object_or_404(News, pk=pk)
    
    # Get comments with pagination
    comments_list = news.comments.select_related('user').order_by('-created_at')
    
    # Filter by moderation status
    status = request.GET.get('status')
    if status:
        comments_list = comments_list.filter(moderation_status=status)
    
    paginator = Paginator(comments_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'news': news,
        'page_obj': page_obj,
        'current_status': status,
    }
    
    return render(request, 'admin/modules/news/comments.html', context)


@login_required
@require_POST
def comment_moderate(request, comment_id):
    """Moderate comment (approve/reject)"""
    comment = get_object_or_404(NewsComment, pk=comment_id)
    action = request.POST.get('action')
    
    if action == 'approve':
        comment.moderation_status = 'approved'
        comment.moderated_by = request.user
        comment.moderated_at = timezone.now()
        comment.save()
        
        # Update comments count
        comment.news.update_comments_count()
        
        messages.success(request, 'Komentar berhasil disetujui.')
    
    elif action == 'reject':
        comment.moderation_status = 'rejected'
        comment.moderated_by = request.user
        comment.moderated_at = timezone.now()
        comment.save()
        
        messages.success(request, 'Komentar berhasil ditolak.')
    
    elif action == 'delete':
        comment.delete()
        messages.success(request, 'Komentar berhasil dihapus.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('news:comments', pk=comment.news.pk)


@login_required
def news_import(request):
    """Import news from file"""
    if request.method == 'POST':
        form = NewsImportForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = form.cleaned_data['file']
            
            try:
                imported_count = 0
                errors = []
                
                if file.name.endswith('.csv'):
                    # Handle CSV import
                    decoded_file = file.read().decode('utf-8')
                    csv_reader = csv.DictReader(decoded_file.splitlines())
                    
                    for row_num, row in enumerate(csv_reader, start=2):
                        try:
                            # Create news from CSV row
                            news = News(
                                title=row.get('title', ''),
                                content=row.get('content', ''),
                                excerpt=row.get('excerpt', ''),
                                author=request.user,
                                status=row.get('status', 'draft')
                            )
                            
                            # Set category if provided
                            category_name = row.get('category')
                            if category_name:
                                category, created = NewsCategory.objects.get_or_create(
                                    name=category_name,
                                    defaults={'slug': slugify(category_name)}
                                )
                                news.category = category
                            
                            news.slug = slugify(news.title)
                            news.reading_time = news.calculate_reading_time()
                            news.save()
                            
                            # Add tags if provided
                            tags_str = row.get('tags', '')
                            if tags_str:
                                tag_names = [tag.strip() for tag in tags_str.split(',')]
                                for tag_name in tag_names:
                                    if tag_name:
                                        tag, created = NewsTag.objects.get_or_create(
                                            name=tag_name,
                                            defaults={'slug': slugify(tag_name)}
                                        )
                                        news.tags.add(tag)
                            
                            imported_count += 1
                            
                        except Exception as e:
                            errors.append(f'Baris {row_num}: {str(e)}')
                
                elif file.name.endswith(('.xlsx', '.xls')):
                    # Handle Excel import
                    workbook = openpyxl.load_workbook(file)
                    worksheet = workbook.active
                    
                    # Assume first row is header
                    headers = [cell.value for cell in worksheet[1]]
                    
                    for row_num, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
                        try:
                            row_data = dict(zip(headers, row))
                            
                            news = News(
                                title=row_data.get('title', ''),
                                content=row_data.get('content', ''),
                                excerpt=row_data.get('excerpt', ''),
                                author=request.user,
                                status=row_data.get('status', 'draft')
                            )
                            
                            # Set category if provided
                            category_name = row_data.get('category')
                            if category_name:
                                category, created = NewsCategory.objects.get_or_create(
                                    name=category_name,
                                    defaults={'slug': slugify(category_name)}
                                )
                                news.category = category
                            
                            news.slug = slugify(news.title)
                            news.reading_time = news.calculate_reading_time()
                            news.save()
                            
                            # Add tags if provided
                            tags_str = row_data.get('tags', '')
                            if tags_str:
                                tag_names = [tag.strip() for tag in str(tags_str).split(',')]
                                for tag_name in tag_names:
                                    if tag_name:
                                        tag, created = NewsTag.objects.get_or_create(
                                            name=tag_name,
                                            defaults={'slug': slugify(tag_name)}
                                        )
                                        news.tags.add(tag)
                            
                            imported_count += 1
                            
                        except Exception as e:
                            errors.append(f'Baris {row_num}: {str(e)}')
                
                if imported_count > 0:
                    messages.success(request, f'{imported_count} berita berhasil diimpor.')
                
                if errors:
                    error_msg = 'Beberapa baris gagal diimpor:\n' + '\n'.join(errors[:10])
                    if len(errors) > 10:
                        error_msg += f'\n... dan {len(errors) - 10} error lainnya'
                    messages.warning(request, error_msg)
                
                return redirect('news:list')
                
            except Exception as e:
                messages.error(request, f'Gagal mengimpor file: {str(e)}')
    
    else:
        form = NewsImportForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'admin/modules/news/import.html', context)


@login_required
def news_export(request):
    """Export news to Excel"""
    # Get filtered news
    news_list = News.objects.select_related('category', 'author').prefetch_related('tags')
    
    # Apply filters from request
    status = request.GET.get('status')
    if status:
        news_list = news_list.filter(status=status)
    
    category_id = request.GET.get('category')
    if category_id:
        news_list = news_list.filter(category_id=category_id)
    
    # Create Excel file
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'News Export'
    
    # Headers
    headers = [
        'ID', 'Judul', 'Kategori', 'Tags', 'Status', 'Prioritas',
        'Featured', 'Breaking', 'Views', 'Likes', 'Comments',
        'Penulis', 'Tanggal Dibuat', 'Tanggal Publikasi'
    ]
    
    for col, header in enumerate(headers, 1):
        worksheet.cell(row=1, column=col, value=header)
    
    # Data
    for row, news in enumerate(news_list, 2):
        worksheet.cell(row=row, column=1, value=news.id)
        worksheet.cell(row=row, column=2, value=news.title)
        worksheet.cell(row=row, column=3, value=news.category.name if news.category else '')
        worksheet.cell(row=row, column=4, value=', '.join([tag.name for tag in news.tags.all()]))
        worksheet.cell(row=row, column=5, value=news.get_status_display())
        worksheet.cell(row=row, column=6, value=news.get_priority_display())
        worksheet.cell(row=row, column=7, value='Ya' if news.is_featured else 'Tidak')
        worksheet.cell(row=row, column=8, value='Ya' if news.is_breaking else 'Tidak')
        worksheet.cell(row=row, column=9, value=news.views_count)
        worksheet.cell(row=row, column=10, value=news.likes_count)
        worksheet.cell(row=row, column=11, value=news.comments_count)
        worksheet.cell(row=row, column=12, value=news.author.get_full_name() or news.author.username)
        worksheet.cell(row=row, column=13, value=news.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.cell(row=row, column=14, value=news.published_date.strftime('%Y-%m-%d %H:%M:%S') if news.published_date else '')
    
    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="news_export_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    
    # Save workbook to response
    workbook.save(response)
    
    return response


# News Category API Views
@login_required
@require_http_methods(["GET"])
def news_category_list_api(request):
    """API to get list of news categories"""
    try:
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        queryset = NewsCategory.objects.annotate(
            news_count=Count('news')
        )
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': item.id,
                    'name': item.name,
                    'description': item.description,
                    'slug': item.slug,
                    'color': item.color,
                    'is_active': item.is_active,
                    'news_count': item.news_count,
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
def news_category_detail_api(request, pk):
    """API to get news category detail"""
    try:
        category = get_object_or_404(NewsCategory, pk=pk)
        
        data = {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'slug': category.slug,
            'color': category.color,
            'is_active': category.is_active,
            'created_at': category.created_at.strftime('%d/%m/%Y %H:%M'),
            'updated_at': category.updated_at.strftime('%d/%m/%Y %H:%M')
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def news_category_create_api(request):
    """API to create new news category"""
    try:
        data = json.loads(request.body)
        
        category = NewsCategory.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            color=data.get('color', '#007bff'),
            is_active=data.get('is_active', True)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Kategori berhasil ditambahkan',
            'data': {
                'id': category.id,
                'name': category.name
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def news_category_update_api(request, pk):
    """API to update news category"""
    try:
        category = get_object_or_404(NewsCategory, pk=pk)
        data = json.loads(request.body)
        
        category.name = data['name']
        category.description = data.get('description', '')
        category.color = data.get('color', '#007bff')
        category.is_active = data.get('is_active', True)
        category.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Kategori berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def news_category_delete_api(request, pk):
    """API to delete news category"""
    try:
        category = get_object_or_404(NewsCategory, pk=pk)
        
        # Check if category has news
        if category.news.exists():
            return JsonResponse({
                'error': 'Kategori tidak dapat dihapus karena masih memiliki berita'
            }, status=400)
        
        category.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Kategori berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# News Tag API Views
@login_required
@require_http_methods(["GET"])
def news_tag_list_api(request):
    """API to get list of news tags"""
    try:
        search = request.GET.get('search', '')
        
        queryset = NewsTag.objects.annotate(
            news_count=Count('news')
        )
        
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        data = {
            'results': [
                {
                    'id': item.id,
                    'name': item.name,
                    'slug': item.slug,
                    'news_count': item.news_count,
                    'created_at': item.created_at.strftime('%d/%m/%Y %H:%M')
                }
                for item in queryset
            ]
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def news_tag_create_api(request):
    """API to create new news tag"""
    try:
        data = json.loads(request.body)
        
        tag = NewsTag.objects.create(
            name=data['name']
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Tag berhasil ditambahkan',
            'data': {
                'id': tag.id,
                'name': tag.name
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def news_tag_delete_api(request, pk):
    """API to delete news tag"""
    try:
        tag = get_object_or_404(NewsTag, pk=pk)
        tag.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Tag berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# News API Views
@login_required
@require_http_methods(["GET"])
def news_list_api(request):
    """API to get list of news"""
    try:
        search = request.GET.get('search', '')
        category_id = request.GET.get('category_id', '')
        status = request.GET.get('status', '')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        queryset = News.objects.select_related('category', 'author').prefetch_related('tags')
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        if status:
            queryset = queryset.filter(status=status)
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': item.id,
                    'title': item.title,
                    'slug': item.slug,
                    'category': item.category.name,
                    'category_color': item.category.color,
                    'author': item.author.get_full_name() or item.author.username,
                    'status': item.status,
                    'priority': item.priority,
                    'is_featured': item.is_featured,
                    'is_breaking': item.is_breaking,
                    'published_date': item.published_date.strftime('%d/%m/%Y %H:%M') if item.published_date else None,
                    'views_count': item.views_count,
                    'likes_count': item.likes_count,
                    'created_at': item.created_at.strftime('%d/%m/%Y %H:%M'),
                    'tags': [tag.name for tag in item.tags.all()]
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
def news_detail_api(request, pk):
    """API to get news detail"""
    try:
        news = get_object_or_404(News.objects.select_related('category', 'author').prefetch_related('tags'), pk=pk)
        
        data = {
            'id': news.id,
            'title': news.title,
            'slug': news.slug,
            'category_id': news.category.id,
            'category': news.category.name,
            'content': news.content,
            'excerpt': news.excerpt,
            'featured_image': news.featured_image.url if news.featured_image else None,
            'status': news.status,
            'priority': news.priority,
            'is_featured': news.is_featured,
            'is_breaking': news.is_breaking,
            'published_date': news.published_date.strftime('%Y-%m-%dT%H:%M') if news.published_date else None,
            'author': news.author.get_full_name() or news.author.username,
            'views_count': news.views_count,
            'likes_count': news.likes_count,
            'meta_title': news.meta_title,
            'meta_description': news.meta_description,
            'tags': [{'id': tag.id, 'name': tag.name} for tag in news.tags.all()],
            'created_at': news.created_at.strftime('%d/%m/%Y %H:%M'),
            'updated_at': news.updated_at.strftime('%d/%m/%Y %H:%M')
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def news_create_api(request):
    """API to create new news"""
    try:
        data = json.loads(request.body)
        
        news = News.objects.create(
            title=data['title'],
            category_id=data['category_id'],
            content=data['content'],
            excerpt=data.get('excerpt', ''),
            status=data.get('status', 'draft'),
            priority=data.get('priority', 'normal'),
            is_featured=data.get('is_featured', False),
            is_breaking=data.get('is_breaking', False),
            published_date=data.get('published_date') if data.get('published_date') else None,
            author=request.user,
            meta_title=data.get('meta_title', ''),
            meta_description=data.get('meta_description', '')
        )
        
        # Add tags
        if 'tag_ids' in data:
            news.tags.set(data['tag_ids'])
        
        return JsonResponse({
            'success': True,
            'message': 'Berita berhasil ditambahkan',
            'data': {
                'id': news.id,
                'title': news.title
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["PUT"])
def news_update_api(request, pk):
    """API to update news"""
    try:
        news = get_object_or_404(News, pk=pk)
        data = json.loads(request.body)
        
        news.title = data['title']
        news.category_id = data['category_id']
        news.content = data['content']
        news.excerpt = data.get('excerpt', '')
        news.status = data.get('status', 'draft')
        news.priority = data.get('priority', 'normal')
        news.is_featured = data.get('is_featured', False)
        news.is_breaking = data.get('is_breaking', False)
        news.published_date = data.get('published_date') if data.get('published_date') else None
        news.meta_title = data.get('meta_title', '')
        news.meta_description = data.get('meta_description', '')
        news.save()
        
        # Update tags
        if 'tag_ids' in data:
            news.tags.set(data['tag_ids'])
        
        return JsonResponse({
            'success': True,
            'message': 'Berita berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def news_delete_api(request, pk):
    """API to delete news"""
    try:
        news = get_object_or_404(News, pk=pk)
        news.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Berita berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# News Comment API Views
@login_required
@require_http_methods(["GET"])
def news_comment_list_api(request):
    """API to get list of news comments"""
    try:
        search = request.GET.get('search', '')
        news_id = request.GET.get('news_id', '')
        status = request.GET.get('status', '')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        queryset = NewsComment.objects.select_related('news')
        
        if search:
            queryset = queryset.filter(
                Q(author_name__icontains=search) |
                Q(content__icontains=search) |
                Q(news__title__icontains=search)
            )
        
        if news_id:
            queryset = queryset.filter(news_id=news_id)
        
        if status:
            queryset = queryset.filter(status=status)
        
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        data = {
            'results': [
                {
                    'id': item.id,
                    'news_title': item.news.title,
                    'author_name': item.author_name,
                    'author_email': item.author_email,
                    'content': item.content[:100] + '...' if len(item.content) > 100 else item.content,
                    'status': item.status,
                    'is_author_verified': item.is_author_verified,
                    'created_at': item.created_at.strftime('%d/%m/%Y %H:%M'),
                    'parent_id': item.parent.id if item.parent else None
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
@csrf_exempt
@require_http_methods(["PUT"])
def news_comment_update_status_api(request, pk):
    """API to update comment status"""
    try:
        comment = get_object_or_404(NewsComment, pk=pk)
        data = json.loads(request.body)
        
        comment.status = data['status']
        comment.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Status komentar berhasil diperbarui'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def news_comment_delete_api(request, pk):
    """API to delete comment"""
    try:
        comment = get_object_or_404(NewsComment, pk=pk)
        comment.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Komentar berhasil dihapus'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Statistics API
@login_required
@require_http_methods(["GET"])
def news_statistics_api(request):
    """API to get news statistics"""
    try:
        total_news = News.objects.count()
        published_news = News.objects.filter(status='published').count()
        draft_news = News.objects.filter(status='draft').count()
        total_categories = NewsCategory.objects.filter(is_active=True).count()
        total_tags = NewsTag.objects.count()
        total_comments = NewsComment.objects.count()
        pending_comments = NewsComment.objects.filter(status='pending').count()
        total_views = NewsView.objects.count()
        
        data = {
            'total_news': total_news,
            'published_news': published_news,
            'draft_news': draft_news,
            'total_categories': total_categories,
            'total_tags': total_tags,
            'total_comments': total_comments,
            'pending_comments': pending_comments,
            'total_views': total_views
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Helper APIs for dropdowns
@login_required
@require_http_methods(["GET"])
def news_categories_dropdown_api(request):
    """API to get categories for dropdown"""
    try:
        categories = NewsCategory.objects.filter(is_active=True).values('id', 'name', 'color')
        return JsonResponse({'results': list(categories)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def news_tags_dropdown_api(request):
    """API to get tags for dropdown"""
    try:
        tags = NewsTag.objects.values('id', 'name')
        return JsonResponse({'results': list(tags)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def news_dropdown_api(request):
    """API to get news for dropdown"""
    try:
        news = News.objects.filter(status='published').values('id', 'title')
        return JsonResponse({'results': list(news)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Template Views
@login_required
def news_create_view(request):
    """View for create news template"""
    context = {
        'page_title': 'Tambah Berita',
        'page_subtitle': 'Buat berita baru',
    }
    return render(request, 'admin/modules/news/create.html', context)


@login_required
def news_edit_view(request, pk):
    """View for edit news template"""
    news = get_object_or_404(News, pk=pk)
    context = {
        'page_title': 'Edit Berita',
        'page_subtitle': f'Edit berita: {news.title}',
        'news': news,
    }
    return render(request, 'admin/modules/news/edit.html', context)


@login_required
def news_view_detail(request, pk):
    """View for news detail template"""
    news = get_object_or_404(News, pk=pk)
    context = {
        'page_title': 'Detail Berita',
        'page_subtitle': news.title,
        'news': news,
    }
    return render(request, 'admin/modules/news/view.html', context)


@login_required
def news_list_view(request):
    """View for news list template"""
    context = {
        'page_title': 'Daftar Berita',
        'page_subtitle': 'Kelola semua berita',
    }
    return render(request, 'admin/modules/news/list.html', context)


@login_required
def news_category_view(request):
    """View for news category template"""
    context = {
        'page_title': 'Kategori Berita',
        'page_subtitle': 'Kelola kategori berita',
    }
    return render(request, 'admin/modules/news/category.html', context)


@login_required
def news_media_view(request):
    """View for news media template"""
    context = {
        'page_title': 'Galeri Media',
        'page_subtitle': 'Kelola media berita',
    }
    return render(request, 'admin/modules/news/media.html', context)
