from django.db import models
from django.utils import timezone


class Dusun(models.Model):
    """Dusun/Hamlet reference data"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    area_size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Area in hectares")
    population_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dusun"
        verbose_name_plural = "Dusun"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Lorong(models.Model):
    """Lorong/Street reference data"""
    dusun = models.ForeignKey(Dusun, on_delete=models.CASCADE, related_name='lorongs')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Length in meters")
    house_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lorong"
        verbose_name_plural = "Lorong"
        unique_together = ['dusun', 'code']

    def __str__(self):
        return f"{self.name} - {self.dusun.name}"


class Penduduk(models.Model):
    """Population/Resident data"""
    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('BELUM_KAWIN', 'Belum Kawin'),
        ('KAWIN', 'Kawin'),
        ('CERAI_HIDUP', 'Cerai Hidup'),
        ('CERAI_MATI', 'Cerai Mati'),
    ]

    nik = models.CharField(max_length=16, unique=True, verbose_name="NIK")
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_place = models.CharField(max_length=100)
    birth_date = models.DateField()
    religion = models.CharField(max_length=50)
    education = models.CharField(max_length=50, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=15, choices=MARITAL_STATUS_CHOICES)
    dusun = models.ForeignKey(Dusun, on_delete=models.CASCADE, related_name='residents')
    lorong = models.ForeignKey(Lorong, on_delete=models.CASCADE, related_name='residents', blank=True, null=True)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Penduduk"
        verbose_name_plural = "Penduduk"

    def __str__(self):
        return f"{self.name} ({self.nik})"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class DisabilitasType(models.Model):
    """Disability type reference"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Jenis Disabilitas"
        verbose_name_plural = "Jenis Disabilitas"

    def __str__(self):
        return self.name


class DisabilitasData(models.Model):
    """Disability data for residents"""
    SEVERITY_CHOICES = [
        ('RINGAN', 'Ringan'),
        ('SEDANG', 'Sedang'),
        ('BERAT', 'Berat'),
    ]

    penduduk = models.ForeignKey(Penduduk, on_delete=models.CASCADE, related_name='disabilities')
    disability_type = models.ForeignKey(DisabilitasType, on_delete=models.CASCADE)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    description = models.TextField(blank=True, null=True)
    diagnosis_date = models.DateField(blank=True, null=True)
    needs_assistance = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Data Disabilitas"
        verbose_name_plural = "Data Disabilitas"
        unique_together = ['penduduk', 'disability_type']

    def __str__(self):
        return f"{self.penduduk.name} - {self.disability_type.name}"


class ReligionReference(models.Model):
    """Religion reference data"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Agama"
        verbose_name_plural = "Agama"

    def __str__(self):
        return self.name
