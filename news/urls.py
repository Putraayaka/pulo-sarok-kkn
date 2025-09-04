from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # News module view - redirect to dashboard
    path('', views.news_admin, name='news_admin'),
    
    # News template views
    path('create/', views.news_create_view, name='news_create_view'),
    path('edit/<int:pk>/', views.news_edit_view, name='news_edit_view'),
    path('view/<int:pk>/', views.news_view_detail, name='news_view_detail'),
    path('list/', views.news_list_view, name='news_list_view'),
    
    # Admin-specific URLs (non-API) - Updated to match dashboard structure
    path('admin/', views.news_admin, name='admin_index'),
    path('admin/view/<int:pk>/', views.news_view_detail, name='admin_view'),
    path('admin/edit/<int:pk>/', views.news_edit_view, name='admin_edit'),
    path('admin/duplicate/<int:pk>/', views.news_duplicate_view, name='admin_duplicate'),
    path('admin/delete/<int:pk>/', views.news_delete_view, name='admin_delete'),
    path('admin/publish/<int:pk>/', views.news_publish_view, name='admin_publish'),
    path('admin/unpublish/<int:pk>/', views.news_unpublish_view, name='admin_unpublish'),
    path('admin/bulk-action/', views.news_bulk_action_view, name='admin_bulk_action'),
    
    # Media management URLs (non-API) - Updated to match dashboard structure
    path('media/', views.news_media_view, name='news_media_view'),
    path('media/upload/', views.news_media_upload_view, name='news_media_upload_view'),
    path('media/<int:pk>/', views.news_media_detail_view, name='admin_media_detail'),
    path('media/<int:pk>/update/', views.news_media_update_view, name='admin_media_update'),
    path('media/<int:pk>/delete/', views.news_media_delete_view, name='admin_media_delete'),
    path('media/bulk-delete/', views.news_media_bulk_delete_view, name='admin_media_bulk_delete'),
    path('media/bulk-download/', views.news_media_bulk_download_view, name='admin_media_bulk_download'),
    
    # Category management URLs (non-API) - Updated to match dashboard structure
    path('categories/', views.news_category_view, name='news_category_view'),
    path('categories/create/', views.news_category_create_view, name='admin_category_create'),
    path('categories/<int:pk>/', views.news_category_detail_view, name='admin_category_detail'),
    path('categories/<int:pk>/update/', views.news_category_update_view, name='admin_category_update'),
    path('categories/<int:pk>/delete/', views.news_category_delete_view, name='admin_category_delete'),
    
    # Announcement management URLs (admin) - Updated to match dashboard structure
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcement/create/', views.announcement_create, name='announcement_create'),
    path('announcement/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcement/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcement/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
    
    # Public announcement URLs
    path('public/announcements/', views.public_announcement_list, name='public_announcement_list'),
    path('public/announcement/<slug:slug>/', views.public_announcement_detail, name='public_announcement_detail'),
    
    # Public news URLs (tanpa autentikasi)
    path('public/news/', views.public_news_list, name='public_news_list'),
    path('public/news/<slug:slug>/', views.public_news_detail, name='public_news_detail'),
    path('public/news/featured/', views.public_featured_news, name='public_featured_news'),
    
    # NewsCategory APIs
    path('api/categories/', views.news_category_list_api, name='newscategory_list'),
    path('api/categories/<int:pk>/', views.news_category_detail_api, name='newscategory_detail'),
    path('api/categories/create/', views.news_category_create_api, name='newscategory_create'),
    path('api/categories/<int:pk>/update/', views.news_category_update_api, name='newscategory_update'),
    path('api/categories/<int:pk>/delete/', views.news_category_delete_api, name='newscategory_delete'),
    path('api/categories/statistics/', views.news_category_statistics_api, name='news_category_statistics'),
    
    # NewsTag APIs
    path('api/tags/', views.news_tag_list_api, name='newstag_list'),
    path('api/tags/search/', views.news_tag_search_api, name='newstag_search'),
    path('api/tags/create/', views.news_tag_create_api, name='newstag_create'),
    path('api/tags/<int:pk>/delete/', views.news_tag_delete_api, name='newstag_delete'),
    
    # News APIs
    path('api/news/', views.news_list_api, name='news_list'),
    path('api/news/<int:pk>/', views.news_detail_api, name='news_detail'),
    path('api/news/create/', views.news_create_api, name='news_create'),
    path('api/news/<int:pk>/update/', views.news_update_api, name='news_update'),
    path('api/news/<int:pk>/delete/', views.news_delete_api, name='news_delete'),
    path('api/news/<int:pk>/duplicate/', views.news_duplicate_api, name='news_duplicate_api'),
    path('api/news/bulk-action/', views.news_bulk_action_api, name='news_bulk_action'),
    
    # NewsComment APIs
    path('api/comments/', views.news_comment_list_api, name='newscomment_list'),
    path('api/comments/<int:pk>/update-status/', views.news_comment_update_status_api, name='newscomment_update_status'),
    path('api/comments/<int:pk>/delete/', views.news_comment_delete_api, name='newscomment_delete'),
    
    # Dropdown APIs
    path('api/categories/dropdown/', views.news_categories_dropdown_api, name='news_categories_dropdown'),
    path('api/tags/dropdown/', views.news_tags_dropdown_api, name='news_tags_dropdown'),
    path('api/news/dropdown/', views.news_dropdown_api, name='news_dropdown'),
    
    # Statistics API
    path('api/statistics/', views.news_statistics_api, name='news_statistics'),
    
    # Media APIs
    path('api/media/', views.news_media_list_api, name='news_media_list_api'),
    path('api/media/upload/', views.news_media_upload_api, name='news_media_upload_api'),
    path('api/video/upload/', views.news_video_upload_api, name='news_video_upload_api'),
    path('api/gallery/upload/', views.news_gallery_upload_api, name='news_gallery_upload_api'),
    path('api/media/<int:pk>/', views.news_media_detail_api, name='news_media_detail_api'),
    path('api/media/<int:pk>/update/', views.news_media_update_api, name='news_media_update_api'),
    path('api/media/<int:pk>/delete/', views.news_media_delete_api, name='news_media_delete_api'),
    path('api/media/bulk-action/', views.news_media_bulk_action_api, name='news_media_bulk_action_api'),
    path('api/media/statistics/', views.news_media_statistics_api, name='news_media_statistics_api'),
]