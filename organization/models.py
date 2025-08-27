from django.db import models
from django.contrib.auth import get_user_model
from references.models import Penduduk
from PIL import Image
import os

User = get_user_model()


class OrganizationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Jenis Organisasi'
        verbose_name_plural = 'Jenis Organisasi'


class Organization(models.Model):
    name = models.CharField(max_length=200)
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    established_date = models.DateField(null=True, blank=True)
    leader = models.ForeignKey(Penduduk, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_organizations')
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Organisasi'
        verbose_name_plural = 'Organisasi'


class OrganizationMember(models.Model):
    POSITION_CHOICES = [
        ('ketua', 'Ketua'),
        ('wakil_ketua', 'Wakil Ketua'),
        ('sekretaris', 'Sekretaris'),
        ('bendahara', 'Bendahara'),
        ('anggota', 'Anggota'),
        ('pengurus', 'Pengurus'),
    ]
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    member = models.ForeignKey(Penduduk, on_delete=models.CASCADE)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    join_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.member.nama} - {self.organization.name} ({self.position})'

    class Meta:
        verbose_name = 'Anggota Organisasi'
        verbose_name_plural = 'Anggota Organisasi'
        unique_together = ['organization', 'member', 'position']


class OrganizationEvent(models.Model):
    EVENT_TYPE_CHOICES = [
        ('rapat', 'Rapat'),
        ('kegiatan', 'Kegiatan'),
        ('pelatihan', 'Pelatihan'),
        ('sosial', 'Kegiatan Sosial'),
        ('lainnya', 'Lainnya'),
    ]
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    participants_count = models.PositiveIntegerField(default=0)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.organization.name}'

    class Meta:
        verbose_name = 'Acara Organisasi'
        verbose_name_plural = 'Acara Organisasi'
        ordering = ['-event_date']


class OrganizationDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('sk', 'Surat Keputusan'),
        ('notulen', 'Notulen Rapat'),
        ('proposal', 'Proposal'),
        ('laporan', 'Laporan'),
        ('surat', 'Surat'),
        ('lainnya', 'Lainnya'),
    ]
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='organization_documents/', null=True, blank=True)
    document_date = models.DateField()
    is_public = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.organization.name}'

    class Meta:
        verbose_name = 'Dokumen Organisasi'
        verbose_name_plural = 'Dokumen Organisasi'
        ordering = ['-document_date']


class Jabatan(models.Model):
    """Model untuk jabatan dalam organisasi"""
    nama_jabatan = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True)
    level_hierarki = models.PositiveIntegerField(default=1, help_text="1=Tertinggi, semakin besar semakin rendah")
    warna_badge = models.CharField(max_length=7, default='#3B82F6', help_text="Kode warna hex untuk badge")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_jabatan

    class Meta:
        verbose_name = 'Jabatan'
        verbose_name_plural = 'Jabatan'
        ordering = ['level_hierarki', 'nama_jabatan']


class PeriodeKepengurusan(models.Model):
    """Model untuk periode kepengurusan organisasi"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='periode_kepengurusan')
    nama_periode = models.CharField(max_length=100)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    deskripsi = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nama_periode} - {self.organization.name}"

    def save(self, *args, **kwargs):
        # Jika periode ini diset aktif, nonaktifkan periode lain
        if self.is_active:
            PeriodeKepengurusan.objects.filter(
                organization=self.organization,
                is_active=True
            ).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Periode Kepengurusan'
        verbose_name_plural = 'Periode Kepengurusan'
        ordering = ['-tanggal_mulai']


class AnggotaOrganisasi(models.Model):
    """Model untuk anggota organisasi dengan foto profil"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='anggota_detail')
    penduduk = models.ForeignKey(Penduduk, on_delete=models.CASCADE)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
    periode = models.ForeignKey(PeriodeKepengurusan, on_delete=models.CASCADE)
    foto_profil = models.ImageField(upload_to='organization/profiles/', null=True, blank=True)
    nomor_anggota = models.CharField(max_length=50, blank=True)
    tanggal_bergabung = models.DateField()
    tanggal_keluar = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('aktif', 'Aktif'),
        ('non_aktif', 'Non Aktif'),
        ('keluar', 'Keluar'),
        ('pensiun', 'Pensiun')
    ], default='aktif')
    bio = models.TextField(blank=True, help_text="Biografi singkat anggota")
    kontak_whatsapp = models.CharField(max_length=20, blank=True)
    email_pribadi = models.EmailField(blank=True)
    alamat_lengkap = models.TextField(blank=True)
    pendidikan_terakhir = models.CharField(max_length=100, blank=True)
    pekerjaan = models.CharField(max_length=100, blank=True)
    keahlian = models.TextField(blank=True, help_text="Keahlian yang dimiliki")
    prestasi = models.TextField(blank=True, help_text="Prestasi yang pernah diraih")
    is_featured = models.BooleanField(default=False, help_text="Tampilkan di halaman utama")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.penduduk.nama} - {self.jabatan.nama_jabatan} ({self.organization.name})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Resize foto profil jika ada
        if self.foto_profil:
            img_path = self.foto_profil.path
            if os.path.exists(img_path):
                with Image.open(img_path) as img:
                    if img.height > 400 or img.width > 400:
                        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                        img.save(img_path, optimize=True, quality=85)

    class Meta:
        verbose_name = 'Anggota Organisasi'
        verbose_name_plural = 'Anggota Organisasi'
        unique_together = ['organization', 'penduduk', 'periode']
        ordering = ['jabatan__level_hierarki', 'penduduk__name']


class GaleriKegiatan(models.Model):
    """Model untuk galeri kegiatan organisasi"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='galeri')
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True)
    foto = models.ImageField(upload_to='organization/gallery/')
    tanggal_kegiatan = models.DateField()
    lokasi = models.CharField(max_length=200, blank=True)
    fotografer = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Pisahkan dengan koma")
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.judul} - {self.organization.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Resize foto galeri
        if self.foto:
            img_path = self.foto.path
            if os.path.exists(img_path):
                with Image.open(img_path) as img:
                    if img.height > 800 or img.width > 800:
                        img.thumbnail((800, 800), Image.Resampling.LANCZOS)
                        img.save(img_path, optimize=True, quality=90)

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    class Meta:
        verbose_name = 'Galeri Kegiatan'
        verbose_name_plural = 'Galeri Kegiatan'
        ordering = ['-tanggal_kegiatan', '-created_at']


class StrukturOrganisasi(models.Model):
    """Model untuk struktur organisasi visual"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='struktur')
    periode = models.ForeignKey(PeriodeKepengurusan, on_delete=models.CASCADE)
    anggota = models.ForeignKey(AnggotaOrganisasi, on_delete=models.CASCADE)
    posisi_x = models.IntegerField(default=0, help_text="Posisi horizontal dalam bagan")
    posisi_y = models.IntegerField(default=0, help_text="Posisi vertikal dalam bagan")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    urutan = models.PositiveIntegerField(default=1)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Struktur {self.anggota.penduduk.nama} - {self.organization.name}"

    class Meta:
        verbose_name = 'Struktur Organisasi'
        verbose_name_plural = 'Struktur Organisasi'
        unique_together = ['organization', 'periode', 'anggota']
        ordering = ['urutan', 'anggota__jabatan__level_hierarki']
