from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # News module view
    path('', views.news_admin, name='news_admin'),
    
    # News template views
    path('create/', views.news_create_view, name='news_create_view'),
    path('edit/<int:pk>/', views.news_edit_view, name='news_edit_view'),
    path('view/<int:pk>/', views.news_view_detail, name='news_view_detail'),
    path('list/', views.news_list_view, name='news_list_view'),
    path('category/', views.news_category_view, name='news_category_view'),
    path('media/', views.news_media_view, name='news_media_view'),
    
    # NewsCategory APIs
    path('categories/', views.news_category_list_api, name='newscategory_list'),
    path('categories/<int:pk>/', views.news_category_detail_api, name='newscategory_detail'),
    path('categories/create/', views.news_category_create_api, name='newscategory_create'),
    path('categories/<int:pk>/update/', views.news_category_update_api, name='newscategory_update'),
    path('categories/<int:pk>/delete/', views.news_category_delete_api, name='newscategory_delete'),
    
    # NewsTag APIs
    path('tags/', views.news_tag_list_api, name='newstag_list'),
    path('tags/create/', views.news_tag_create_api, name='newstag_create'),
    path('tags/<int:pk>/delete/', views.news_tag_delete_api, name='newstag_delete'),
    
    # News APIs
    path('news/', views.news_list_api, name='news_list'),
    path('news/<int:pk>/', views.news_detail_api, name='news_detail'),
    path('news/create/', views.news_create_api, name='news_create'),
    path('news/<int:pk>/update/', views.news_update_api, name='news_update'),
    path('news/<int:pk>/delete/', views.news_delete_api, name='news_delete'),
    
    # NewsComment APIs
    path('comments/', views.news_comment_list_api, name='newscomment_list'),
    path('comments/<int:pk>/update-status/', views.news_comment_update_status_api, name='newscomment_update_status'),
    path('comments/<int:pk>/delete/', views.news_comment_delete_api, name='newscomment_delete'),
    
    # Dropdown APIs
    path('categories/dropdown/', views.news_categories_dropdown_api, name='news_categories_dropdown'),
    path('tags/dropdown/', views.news_tags_dropdown_api, name='news_tags_dropdown'),
    path('news/dropdown/', views.news_dropdown_api, name='news_dropdown'),
    
    # Statistics API
    path('statistics/', views.news_statistics_api, name='news_statistics'),
]