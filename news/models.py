from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from PIL import Image
import os

User = get_user_model()


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategori Berita'
        verbose_name_plural = 'Kategori Berita'
        ordering = ['name']


class NewsTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag Berita'
        verbose_name_plural = 'Tag Berita'
        ordering = ['name']


class News(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Terjadwal'),
        ('published', 'Dipublikasi'),
        ('archived', 'Diarsipkan'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Rendah'),
        ('normal', 'Normal'),
        ('high', 'Tinggi'),
        ('urgent', 'Mendesak'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news')
    tags = models.ManyToManyField(NewsTag, blank=True, related_name='news')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    featured_image = models.ImageField(upload_to='news/images/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    is_featured = models.BooleanField(default=False)
    is_breaking = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True, help_text='Tanggal untuk publikasi otomatis')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_articles')
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(default=0, help_text='Estimasi waktu baca dalam menit')
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt and self.content:
            self.excerpt = self.content[:297] + '...' if len(self.content) > 300 else self.content
        
        # Calculate reading time (average 200 words per minute)
        if self.content:
            word_count = len(self.content.split())
            self.reading_time = max(1, round(word_count / 200))
        
        super().save(*args, **kwargs)
    
    def update_counts(self):
        """Update all count fields"""
        self.likes_count = self.likes.count()
        self.comments_count = self.comments.filter(status='approved').count()
        self.shares_count = self.shares.count()
        self.save(update_fields=['likes_count', 'comments_count', 'shares_count'])
    
    def is_published(self):
        """Check if news is published"""
        from django.utils import timezone
        return (
            self.status == 'published' and 
            self.published_date and 
            self.published_date <= timezone.now()
        )
    
    def is_scheduled(self):
        """Check if news is scheduled for future publication"""
        from django.utils import timezone
        return (
            self.status == 'scheduled' and 
            self.scheduled_date and 
            self.scheduled_date > timezone.now()
        )
    
    def get_featured_image_url(self):
        """Get featured image URL or first gallery image"""
        if self.featured_image:
            return self.featured_image.url
        
        first_image = self.images.filter(is_featured=True).first()
        if not first_image:
            first_image = self.images.first()
        
        return first_image.image.url if first_image else None
    
    def get_thumbnail_url(self):
        """Get thumbnail URL"""
        first_image = self.images.filter(is_featured=True).first()
        if not first_image:
            first_image = self.images.first()
        
        return first_image.thumbnail.url if first_image and first_image.thumbnail else None

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Berita'
        verbose_name_plural = 'Berita'
        ordering = ['-published_date', '-created_at']


class NewsComment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Menunggu Moderasi'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
        ('spam', 'Spam'),
    ]
    
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    author_website = models.URLField(blank=True)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    is_author_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author_name} - {self.news.title}'

    class Meta:
        verbose_name = 'Komentar Berita'
        verbose_name_plural = 'Komentar Berita'
        ordering = ['-created_at']


class NewsView(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='view_records')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    view_date = models.DateTimeField(auto_now_add=True)
    view_duration = models.PositiveIntegerField(default=0, help_text='Duration in seconds')
    device_type = models.CharField(max_length=20, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    operating_system = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.news.title} - {self.ip_address}'

    class Meta:
        verbose_name = 'Tampilan Berita'
        verbose_name_plural = 'Tampilan Berita'
        ordering = ['-view_date']
        unique_together = ['news', 'ip_address', 'session_key']


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news/gallery/')
    thumbnail = models.ImageField(upload_to='news/thumbnails/', blank=True)
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Create thumbnail
        if self.image and not self.thumbnail:
            self.create_thumbnail()
    
    def create_thumbnail(self):
        if not self.image:
            return
            
        try:
            image = Image.open(self.image.path)
            image.thumbnail((300, 300), Image.Resampling.LANCZOS)
            
            # Save thumbnail
            thumb_name = f"thumb_{os.path.basename(self.image.name)}"
            thumb_path = os.path.join(os.path.dirname(self.image.path), 'thumbnails', thumb_name)
            
            # Create thumbnails directory if it doesn't exist
            os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
            
            image.save(thumb_path, 'JPEG', quality=85)
            self.thumbnail = f"news/thumbnails/{thumb_name}"
            super().save(update_fields=['thumbnail'])
        except Exception as e:
            pass  # Handle thumbnail creation errors gracefully
    
    def __str__(self):
        return f'{self.news.title} - Image {self.order}'
    
    class Meta:
        verbose_name = 'Gambar Berita'
        verbose_name_plural = 'Gambar Berita'
        ordering = ['order', 'created_at']


class NewsLike(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=40, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.user:
            return f'{self.user.username} likes {self.news.title}'
        return f'{self.ip_address} likes {self.news.title}'
    
    class Meta:
        verbose_name = 'Like Berita'
        verbose_name_plural = 'Like Berita'
        ordering = ['-created_at']
        unique_together = ['news', 'ip_address', 'session_key']


class NewsShare(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('email', 'Email'),
        ('copy_link', 'Copy Link'),
        ('other', 'Lainnya'),
    ]
    
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='shares')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=40, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.news.title} shared on {self.get_platform_display()}'
    
    class Meta:
        verbose_name = 'Share Berita'
        verbose_name_plural = 'Share Berita'
        ordering = ['-created_at']
