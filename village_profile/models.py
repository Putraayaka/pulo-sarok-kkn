from django.db import models
from django.utils import timezone


class VillageVision(models.Model):
    """Village Vision and Mission"""
    title = models.CharField(max_length=200)
    vision_text = models.TextField()
    mission_text = models.TextField()
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visi Misi Desa"
        verbose_name_plural = "Visi Misi Desa"
        ordering = ['-effective_date']

    def __str__(self):
        return f"{self.title} ({self.effective_date})"


class VillageHistory(models.Model):
    """Village History"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    period_start = models.CharField(max_length=50, blank=True, null=True)
    period_end = models.CharField(max_length=50, blank=True, null=True)
    historical_image = models.ImageField(upload_to='village_history/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sejarah Desa"
        verbose_name_plural = "Sejarah Desa"
        ordering = ['period_start']

    def __str__(self):
        return self.title


class VillageMap(models.Model):
    """Village Map and Geographic Information"""
    MAP_TYPE_CHOICES = [
        ('ADMINISTRATIVE', 'Peta Administrasi'),
        ('TOPOGRAPHIC', 'Peta Topografi'),
        ('LAND_USE', 'Peta Penggunaan Lahan'),
        ('TOURISM', 'Peta Wisata'),
    ]

    title = models.CharField(max_length=200)
    map_type = models.CharField(max_length=20, choices=MAP_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    map_image = models.ImageField(upload_to='village_maps/')
    map_file = models.FileField(upload_to='village_maps/files/', blank=True, null=True, help_text="PDF or other map files")
    coordinates_center_lat = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    coordinates_center_lng = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    zoom_level = models.IntegerField(default=15)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Peta Desa"
        verbose_name_plural = "Peta Desa"

    def __str__(self):
        return f"{self.title} ({self.get_map_type_display()})"


class VillageGeography(models.Model):
    """Village Geographic and Demographic Information"""
    total_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total area in hectares")
    agricultural_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    residential_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    forest_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    water_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    altitude_min = models.IntegerField(blank=True, null=True, help_text="Minimum altitude in meters")
    altitude_max = models.IntegerField(blank=True, null=True, help_text="Maximum altitude in meters")
    climate_type = models.CharField(max_length=100, blank=True, null=True)
    rainfall_average = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Average rainfall in mm/year")
    temperature_min = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    temperature_max = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    boundaries_north = models.CharField(max_length=200, blank=True, null=True)
    boundaries_south = models.CharField(max_length=200, blank=True, null=True)
    boundaries_east = models.CharField(max_length=200, blank=True, null=True)
    boundaries_west = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Geografi Desa"
        verbose_name_plural = "Geografi Desa"

    def __str__(self):
        return f"Geografi Desa - {self.total_area} Ha"


class GoogleMapsEmblem(models.Model):
    """Google Maps Emblem for Village"""
    title = models.CharField(max_length=200, default="Emblem Desa Pulosarok")
    description = models.TextField(blank=True, null=True, help_text="Deskripsi tentang emblem desa")
    
    # Koordinat Google Maps
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=8, 
        help_text="Latitude koordinat emblem di Google Maps"
    )
    longitude = models.DecimalField(
        max_digits=11, 
        decimal_places=8, 
        help_text="Longitude koordinat emblem di Google Maps"
    )
    zoom_level = models.IntegerField(
        default=15, 
        help_text="Level zoom Google Maps (1-20)"
    )
    
    # Informasi emblem
    emblem_size = models.CharField(
        max_length=20,
        choices=[
            ('small', 'Kecil'),
            ('medium', 'Sedang'),
            ('large', 'Besar'),
        ],
        default='medium',
        help_text="Ukuran emblem di peta"
    )
    
    # Status dan metadata
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True, help_text="Tampilkan emblem di peta")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Google Maps Emblem"
        verbose_name_plural = "Google Maps Emblem"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.latitude}, {self.longitude})"
    
    @property
    def google_maps_url(self):
        """Generate Google Maps URL for this emblem location"""
        return f"https://www.google.com/maps?q={self.latitude},{self.longitude}&z={self.zoom_level}"
    
    @property
    def coordinates_display(self):
        """Display coordinates in a readable format"""
        return f"Lat: {self.latitude}, Lng: {self.longitude}"
