from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from references.models import Penduduk
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

User = get_user_model()


class EventCategory(models.Model):
    """Model untuk kategori event"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nama Kategori')
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Icon FontAwesome')
    color = models.CharField(max_length=20, default='blue', verbose_name='Warna')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategori Event'
        verbose_name_plural = 'Kategori Event'
        ordering = ['name']


class Event(models.Model):
    """Model untuk event"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('ongoing', 'Berlangsung'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Rendah'),
        ('normal', 'Normal'),
        ('high', 'Tinggi'),
        ('urgent', 'Mendesak'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200, verbose_name='Judul Event')
    slug = models.SlugField(max_length=250, unique=True, blank=True, verbose_name='Slug')
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, verbose_name='Kategori')
    description = models.TextField(verbose_name='Deskripsi Event')
    short_description = models.TextField(max_length=300, blank=True, verbose_name='Deskripsi Singkat')
    
    # Date and Time
    start_date = models.DateField(verbose_name='Tanggal Mulai')
    end_date = models.DateField(verbose_name='Tanggal Selesai')
    start_time = models.TimeField(verbose_name='Waktu Mulai')
    end_time = models.TimeField(verbose_name='Waktu Selesai')
    
    # Location
    location = models.CharField(max_length=200, verbose_name='Lokasi Event')
    address = models.TextField(blank=True, verbose_name='Alamat Lengkap')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='Latitude')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name='Longitude')
    
    # Capacity and Registration
    max_participants = models.PositiveIntegerField(default=0, verbose_name='Maksimal Peserta')
    current_participants = models.PositiveIntegerField(default=0, verbose_name='Peserta Saat Ini')
    allow_registration = models.BooleanField(default=True, verbose_name='Izinkan Pendaftaran')
    registration_deadline = models.DateTimeField(null=True, blank=True, verbose_name='Deadline Pendaftaran')
    
    # Cost and Requirements
    is_free = models.BooleanField(default=True, verbose_name='Event Gratis')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Biaya Event')
    requirements = models.TextField(blank=True, verbose_name='Persyaratan Peserta')
    
    # Contact Information
    contact_person = models.CharField(max_length=100, blank=True, verbose_name='Contact Person')
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name='No. HP Contact')
    contact_email = models.EmailField(blank=True, verbose_name='Email Contact')
    
    # Status and Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Status')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal', verbose_name='Prioritas')
    
    # Media
    featured_image = models.ImageField(upload_to='events/images/', null=True, blank=True, verbose_name='Gambar Utama')
    gallery_images = models.JSONField(default=list, blank=True, verbose_name='Galeri Gambar')
    
    # Additional Fields
    tags = models.CharField(max_length=500, blank=True, verbose_name='Tags (pisahkan dengan koma)')
    notes = models.TextField(blank=True, verbose_name='Catatan')
    is_featured = models.BooleanField(default=False, verbose_name='Event Unggulan')
    
    # Metadata
    views_count = models.PositiveIntegerField(default=0, verbose_name='Jumlah Dilihat')
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, 
                                validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name='Rating')
    total_ratings = models.PositiveIntegerField(default=0, verbose_name='Total Rating')
    
    # Timestamps
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Dibuat Oleh')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Dipublikasi')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def is_registration_open(self):
        """Check if registration is still open"""
        if not self.allow_registration:
            return False
        if self.registration_deadline:
            return timezone.now() <= self.registration_deadline
        return self.status == 'published' and self.current_participants < self.max_participants

    def is_full(self):
        """Check if event is full"""
        if self.max_participants == 0:
            return False
        return self.current_participants >= self.max_participants

    def get_remaining_capacity(self):
        """Get remaining capacity"""
        if self.max_participants == 0:
            return float('inf')
        return max(0, self.max_participants - self.current_participants)

    def get_duration_days(self):
        """Get event duration in days"""
        return (self.end_date - self.start_date).days + 1

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Event'
        ordering = ['-start_date', '-created_at']


class EventParticipant(models.Model):
    """Model untuk peserta event"""
    STATUS_CHOICES = [
        ('pending', 'Menunggu Konfirmasi'),
        ('confirmed', 'Dikonfirmasi'),
        ('attended', 'Hadir'),
        ('absent', 'Tidak Hadir'),
        ('cancelled', 'Dibatalkan'),
    ]
    
    REGISTRATION_SOURCE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('phone', 'Telepon'),
        ('walk_in', 'Datang Langsung'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants', verbose_name='Event')
    participant = models.ForeignKey(Penduduk, on_delete=models.CASCADE, verbose_name='Peserta')
    
    # Registration Details
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Daftar')
    registration_source = models.CharField(max_length=20, choices=REGISTRATION_SOURCE_CHOICES, default='online', verbose_name='Sumber Pendaftaran')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    
    # Additional Information
    phone = models.CharField(max_length=20, blank=True, verbose_name='No. HP')
    email = models.EmailField(blank=True, verbose_name='Email')
    emergency_contact = models.CharField(max_length=100, blank=True, verbose_name='Kontak Darurat')
    emergency_phone = models.CharField(max_length=20, blank=True, verbose_name='No. HP Darurat')
    
    # Special Requirements
    special_needs = models.TextField(blank=True, verbose_name='Kebutuhan Khusus')
    dietary_restrictions = models.TextField(blank=True, verbose_name='Pantangan Makanan')
    
    # Attendance
    check_in_time = models.DateTimeField(null=True, blank=True, verbose_name='Waktu Check-in')
    check_out_time = models.DateTimeField(null=True, blank=True, verbose_name='Waktu Check-out')
    
    # Payment
    payment_status = models.CharField(max_length=20, choices=[
        ('unpaid', 'Belum Bayar'),
        ('paid', 'Sudah Bayar'),
        ('partial', 'Bayar Sebagian'),
        ('refunded', 'Dikembalikan'),
    ], default='unpaid', verbose_name='Status Pembayaran')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Jumlah Bayar')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Bayar')
    
    # Notes
    notes = models.TextField(blank=True, verbose_name='Catatan')
    
    # Timestamps
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Didaftarkan Oleh')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.participant.nama} - {self.event.title}"

    class Meta:
        verbose_name = 'Peserta Event'
        verbose_name_plural = 'Peserta Event'
        unique_together = ['event', 'participant']
        ordering = ['-registration_date']


class EventRegistration(models.Model):
    """Model untuk pendaftaran event (untuk non-penduduk)"""
    STATUS_CHOICES = [
        ('pending', 'Menunggu Konfirmasi'),
        ('confirmed', 'Dikonfirmasi'),
        ('rejected', 'Ditolak'),
        ('cancelled', 'Dibatalkan'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations', verbose_name='Event')
    
    # Personal Information
    full_name = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    phone = models.CharField(max_length=20, verbose_name='No. HP')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.TextField(verbose_name='Alamat')
    
    # Additional Information
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='Usia')
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Laki-laki'),
        ('female', 'Perempuan'),
    ], blank=True, verbose_name='Jenis Kelamin')
    
    # Registration Details
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Daftar')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    
    # Special Requirements
    special_needs = models.TextField(blank=True, verbose_name='Kebutuhan Khusus')
    dietary_restrictions = models.TextField(blank=True, verbose_name='Pantangan Makanan')
    
    # Notes
    notes = models.TextField(blank=True, verbose_name='Catatan')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"

    class Meta:
        verbose_name = 'Pendaftaran Event'
        verbose_name_plural = 'Pendaftaran Event'
        ordering = ['-registration_date']


class EventFeedback(models.Model):
    """Model untuk feedback event"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedbacks', verbose_name='Event')
    participant = models.ForeignKey(EventParticipant, on_delete=models.CASCADE, verbose_name='Peserta')
    
    # Rating and Feedback
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Rating')
    comment = models.TextField(blank=True, verbose_name='Komentar')
    
    # Categories
    organization_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], 
                                                   null=True, blank=True, verbose_name='Rating Organisasi')
    venue_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], 
                                             null=True, blank=True, verbose_name='Rating Lokasi')
    content_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], 
                                               null=True, blank=True, verbose_name='Rating Konten')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback {self.participant.participant.nama} - {self.event.title}"

    class Meta:
        verbose_name = 'Feedback Event'
        verbose_name_plural = 'Feedback Event'
        unique_together = ['event', 'participant']
        ordering = ['-created_at']


class EventSchedule(models.Model):
    """Model untuk jadwal detail event"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedules', verbose_name='Event')
    
    # Schedule Details
    title = models.CharField(max_length=200, verbose_name='Judul Aktivitas')
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    start_time = models.TimeField(verbose_name='Waktu Mulai')
    end_time = models.TimeField(verbose_name='Waktu Selesai')
    
    # Location and Speaker
    location = models.CharField(max_length=200, blank=True, verbose_name='Lokasi')
    speaker = models.CharField(max_length=200, blank=True, verbose_name='Pembicara')
    
    # Order
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.event.title}"

    class Meta:
        verbose_name = 'Jadwal Event'
        verbose_name_plural = 'Jadwal Event'
        ordering = ['order', 'start_time']


class EventDocument(models.Model):
    """Model untuk dokumen event"""
    DOCUMENT_TYPE_CHOICES = [
        ('proposal', 'Proposal'),
        ('budget', 'Anggaran'),
        ('report', 'Laporan'),
        ('certificate', 'Sertifikat'),
        ('photo', 'Foto'),
        ('video', 'Video'),
        ('other', 'Lainnya'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='documents', verbose_name='Event')
    
    # Document Details
    title = models.CharField(max_length=200, verbose_name='Judul Dokumen')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, verbose_name='Jenis Dokumen')
    file = models.FileField(upload_to='events/documents/', verbose_name='File')
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    
    # Metadata
    file_size = models.PositiveIntegerField(null=True, blank=True, verbose_name='Ukuran File (bytes)')
    download_count = models.PositiveIntegerField(default=0, verbose_name='Jumlah Download')
    is_public = models.BooleanField(default=False, verbose_name='Publik')
    
    # Timestamps
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Diupload Oleh')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.event.title}"

    def get_file_size_display(self):
        """Get human readable file size"""
        if self.file_size:
            if self.file_size < 1024:
                return f'{self.file_size} B'
            elif self.file_size < 1024 * 1024:
                return f'{self.file_size / 1024:.1f} KB'
            else:
                return f'{self.file_size / (1024 * 1024):.1f} MB'
        return 'Unknown'

    class Meta:
        verbose_name = 'Dokumen Event'
        verbose_name_plural = 'Dokumen Event'
        ordering = ['-created_at']
