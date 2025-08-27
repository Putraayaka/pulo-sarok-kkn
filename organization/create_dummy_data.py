#!/usr/bin/env python
"""
Script untuk membuat data dummy untuk semua model organisasi
Jalankan dengan: python manage.py shell < organization/create_dummy_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
from faker import Faker
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from organization.models import (
    OrganizationType, Organization, OrganizationMember, 
    OrganizationEvent, OrganizationDocument, Jabatan, 
    PeriodeKepengurusan, AnggotaOrganisasi, GaleriKegiatan, 
    StrukturOrganisasi
)
from references.models import Penduduk

fake = Faker('id_ID')  # Indonesian locale

def create_dummy_data():
    print("Membuat data dummy untuk organisasi...")
    
    # 1. Buat OrganizationType (minimal 10)
    print("1. Membuat OrganizationType...")
    org_types_data = [
        {'name': 'Badan Permusyawaratan Desa', 'description': 'Lembaga perwakilan masyarakat desa'},
        {'name': 'Pemberdayaan Kesejahteraan Keluarga', 'description': 'Organisasi pemberdayaan perempuan'},
        {'name': 'Karang Taruna', 'description': 'Organisasi kepemudaan desa'},
        {'name': 'Lembaga Pemberdayaan Masyarakat', 'description': 'Lembaga pemberdayaan masyarakat desa'},
        {'name': 'Rukun Tetangga', 'description': 'Organisasi tingkat RT'},
        {'name': 'Rukun Warga', 'description': 'Organisasi tingkat RW'},
        {'name': 'Kelompok Tani', 'description': 'Organisasi petani desa'},
        {'name': 'Posyandu', 'description': 'Pos pelayanan terpadu kesehatan'},
        {'name': 'Majelis Taklim', 'description': 'Organisasi keagamaan'},
        {'name': 'Koperasi Desa', 'description': 'Koperasi ekonomi desa'},
        {'name': 'Tim Penggerak PKK', 'description': 'Tim penggerak pemberdayaan kesejahteraan keluarga'},
        {'name': 'Kelompok Usaha Bersama', 'description': 'Kelompok usaha ekonomi masyarakat'}
    ]
    
    org_types = []
    for data in org_types_data:
        org_type, created = OrganizationType.objects.get_or_create(
            name=data['name'],
            defaults={
                'description': data['description'],
                'is_active': True
            }
        )
        org_types.append(org_type)
        if created:
            print(f"   - Created: {org_type.name}")
    
    # 2. Buat Jabatan (minimal 15)
    print("2. Membuat Jabatan...")
    jabatan_data = [
        {'nama': 'Ketua', 'tipe': 'struktural', 'level': 1},
        {'nama': 'Wakil Ketua', 'tipe': 'struktural', 'level': 2},
        {'nama': 'Sekretaris', 'tipe': 'struktural', 'level': 3},
        {'nama': 'Bendahara', 'tipe': 'struktural', 'level': 3},
        {'nama': 'Koordinator Bidang', 'tipe': 'struktural', 'level': 4},
        {'nama': 'Anggota', 'tipe': 'struktural', 'level': 5},
        {'nama': 'Ketua Bidang Pendidikan', 'tipe': 'fungsional', 'level': 3},
        {'nama': 'Ketua Bidang Kesehatan', 'tipe': 'fungsional', 'level': 3},
        {'nama': 'Ketua Bidang Ekonomi', 'tipe': 'fungsional', 'level': 3},
        {'nama': 'Ketua Bidang Sosial', 'tipe': 'fungsional', 'level': 3},
        {'nama': 'Ketua Bidang Keagamaan', 'tipe': 'fungsional', 'level': 3},
        {'nama': 'Ketua Bidang Olahraga', 'tipe': 'fungsional', 'level': 3},
        {'nama': 'Koordinator Wilayah', 'tipe': 'fungsional', 'level': 4},
        {'nama': 'Penasihat', 'tipe': 'struktural', 'level': 1},
        {'nama': 'Pembina', 'tipe': 'struktural', 'level': 1}
    ]
    
    jabatan_list = []
    for data in jabatan_data:
        jabatan, created = Jabatan.objects.get_or_create(
            nama_jabatan=data['nama'],
            defaults={
                'deskripsi': f"Jabatan {data['nama']} dalam organisasi",
                'level_hierarki': data['level'],
                'is_active': True
            }
        )
        jabatan_list.append(jabatan)
        if created:
            print(f"   - Created: {jabatan.nama_jabatan}")
    
    # 3. Buat Organization (minimal 12)
    print("3. Membuat Organization...")
    organizations = []
    for i, org_type in enumerate(org_types):
        org, created = Organization.objects.get_or_create(
            name=f"{org_type.name} Desa Pulosarok",
            defaults={
                'organization_type': org_type,
                'description': f"Organisasi {org_type.name} di Desa Pulosarok yang bergerak dalam bidang {org_type.description.lower()}",
                'established_date': fake.date_between(start_date='-10y', end_date='today'),
                'contact_phone': fake.phone_number(),
                'contact_email': fake.email(),
                'address': f"Desa Pulosarok, {fake.address()}",
                'is_active': True
            }
        )
        organizations.append(org)
        if created:
            print(f"   - Created: {org.name}")
    
    # 4. Buat PeriodeKepengurusan (minimal 15)
    print("4. Membuat PeriodeKepengurusan...")
    periode_list = []
    for org in organizations:
        # Buat 1-2 periode per organisasi
        for i in range(random.randint(1, 2)):
            start_year = 2020 + i * 3
            end_year = start_year + 3
            
            periode, created = PeriodeKepengurusan.objects.get_or_create(
                nama_periode=f"Periode {start_year}-{end_year}",
                organization=org,
                defaults={
                    'tanggal_mulai': datetime(start_year, 1, 1).date(),
                    'tanggal_selesai': datetime(end_year, 12, 31).date(),
                    'deskripsi': f"Periode kepengurusan {org.name} tahun {start_year}-{end_year}",
                    'is_active': end_year >= 2024
                }
            )
            periode_list.append(periode)
            if created:
                print(f"   - Created: {periode.nama_periode} - {org.name}")
    
    # 5. Ambil data penduduk yang sudah ada
    print("5. Mengambil data penduduk...")
    penduduk_list = list(Penduduk.objects.all()[:50])
    if len(penduduk_list) < 10:
        print("   Tidak cukup data penduduk. Silakan buat data penduduk terlebih dahulu.")
        return
    
    # 6. Buat AnggotaOrganisasi (minimal 50)
    print("6. Membuat AnggotaOrganisasi...")
    anggota_count = 0
    for org in organizations:
        # Setiap organisasi punya 3-8 anggota
        num_members = random.randint(3, 8)
        selected_penduduk = random.sample(penduduk_list, min(num_members, len(penduduk_list)))
        
        for penduduk in selected_penduduk:
            jabatan = random.choice(jabatan_list)
            periode = random.choice([p for p in periode_list if p.organization == org])
            
            # Cek apakah kombinasi sudah ada untuk menghindari duplikasi
            if not AnggotaOrganisasi.objects.filter(
                organization=org,
                penduduk=penduduk,
                periode=periode
            ).exists():
                anggota, created = AnggotaOrganisasi.objects.get_or_create(
                    penduduk=penduduk,
                    organization=org,
                    periode=periode,
                    defaults={
                        'jabatan': jabatan,
                        'tanggal_bergabung': fake.date_between(start_date=periode.tanggal_mulai, end_date='today'),
                        'status': random.choice(['aktif', 'aktif', 'aktif', 'non_aktif']),  # 75% aktif
                        'bio': f"Anggota {jabatan.nama_jabatan} {org.name}"
                    }
                )
                if created:
                    anggota_count += 1
    
    print(f"   - Created {anggota_count} anggota organisasi")
    
    # 7. Buat StrukturOrganisasi (minimal 30)
    print("7. Membuat StrukturOrganisasi...")
    struktur_count = 0
    for org in organizations:
        periode_aktif = periode_list[-1] if periode_list else None
        anggota_org = AnggotaOrganisasi.objects.filter(organization=org, status='aktif')
        
        for anggota in anggota_org[:5]:  # Ambil 5 anggota per organisasi untuk struktur
            struktur, created = StrukturOrganisasi.objects.get_or_create(
                organization=org,
                anggota=anggota,
                defaults={
                    'periode': periode_aktif,
                    'urutan': random.randint(1, 10),
                    'is_visible': True
                }
            )
            if created:
                struktur_count += 1
    
    print(f"   - Created {struktur_count} struktur organisasi")
    
    # 8. Buat GaleriKegiatan (minimal 20)
    print("8. Membuat GaleriKegiatan...")
    kegiatan_titles = [
        'Rapat Koordinasi Bulanan', 'Pelatihan Keterampilan', 'Gotong Royong Bersih Desa',
        'Sosialisasi Program Kerja', 'Bakti Sosial', 'Peringatan Hari Kemerdekaan',
        'Festival Budaya Desa', 'Lomba Kreativitas', 'Penyuluhan Kesehatan',
        'Pelatihan Wirausaha', 'Kerja Bakti Lingkungan', 'Rapat Evaluasi',
        'Pelatihan Teknologi', 'Seminar Pendidikan', 'Kegiatan Olahraga Bersama',
        'Perayaan Hari Besar', 'Workshop Keterampilan', 'Musyawarah Desa',
        'Pelatihan Pertanian', 'Kegiatan Keagamaan', 'Donor Darah',
        'Pelatihan Komputer', 'Lomba Desa', 'Pameran Produk Lokal'
    ]
    
    galeri_count = 0
    for i, title in enumerate(kegiatan_titles):
        org = random.choice(organizations)
        
        galeri, created = GaleriKegiatan.objects.get_or_create(
            judul=f"{title} {org.name}",
            organization=org,
            defaults={
                'deskripsi': f"Dokumentasi kegiatan {title.lower()} yang diselenggarakan oleh {org.name}. Kegiatan ini bertujuan untuk meningkatkan partisipasi masyarakat dan mengembangkan potensi desa.",
                'foto': f'organization/gallery/dummy_{i}.jpg',
                'tanggal_kegiatan': fake.date_between(start_date='-2y', end_date='today'),
                'lokasi': fake.city(),
                'fotografer': fake.name(),
                'tags': ', '.join(fake.words(nb=3)),
                'is_featured': random.choice([True, False]),
                'view_count': random.randint(0, 1000)
            }
        )
        if created:
            galeri_count += 1
    
    print(f"   - Created {galeri_count} galeri kegiatan")
    
    # 9. Buat OrganizationEvent (minimal 25)
    print("9. Membuat OrganizationEvent...")
    event_count = 0
    event_types = ['meeting', 'training', 'social', 'cultural', 'sports']
    
    for org in organizations:
        # Setiap organisasi punya 2-4 event
        for i in range(random.randint(2, 4)):
            event_date = fake.date_time_between(start_date='-1y', end_date='+6m')
            
            event, created = OrganizationEvent.objects.get_or_create(
                title=f"{random.choice(kegiatan_titles)} {org.name}",
                organization=org,
                event_date=event_date,
                defaults={
                    'description': f"Event yang diselenggarakan oleh {org.name} untuk meningkatkan kualitas organisasi dan pelayanan kepada masyarakat.",
                    'event_type': random.choice(event_types),
                    'location': f"Balai Desa Pulosarok / {fake.address()}",
                    'participants_count': random.randint(10, 100),
                    'budget': random.randint(500000, 5000000),
                    'is_completed': event_date.replace(tzinfo=None) < datetime.now()
                }
            )
            if created:
                event_count += 1
    
    print(f"   - Created {event_count} organization events")
    
    print("\n=== SUMMARY ===")
    print(f"OrganizationType: {OrganizationType.objects.count()}")
    print(f"Organization: {Organization.objects.count()}")
    print(f"Jabatan: {Jabatan.objects.count()}")
    print(f"PeriodeKepengurusan: {PeriodeKepengurusan.objects.count()}")
    print(f"AnggotaOrganisasi: {AnggotaOrganisasi.objects.count()}")
    print(f"StrukturOrganisasi: {StrukturOrganisasi.objects.count()}")
    print(f"GaleriKegiatan: {GaleriKegiatan.objects.count()}")
    print(f"OrganizationEvent: {OrganizationEvent.objects.count()}")
    print(f"Penduduk: {Penduduk.objects.count()}")
    
    print("\nData dummy berhasil dibuat!")

if __name__ == '__main__':
    create_dummy_data()