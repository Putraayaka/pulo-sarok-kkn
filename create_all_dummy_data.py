#!/usr/bin/env python
"""
Script untuk membuat data dummy untuk semua model Django
Minimal 3 entries untuk setiap model
"""

import os
import sys
import django
from datetime import datetime, timedelta, date
from django.utils import timezone
from faker import Faker
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

# Import models
from business.models import (
    BusinessCategory, Business, BusinessOwner, BusinessProduct, BusinessFinance,
    Koperasi, BUMG, UKM, Aset, LayananJasa, JenisKoperasi
)
from beneficiaries.models import (
    BeneficiaryCategory, Beneficiary, Aid, AidDistribution, 
    BeneficiaryVerification, TarafKehidupan, DataBantuan,
    DokumenGampong, Berita, LetterTemplate, Surat
)
from documents.models import (
    DocumentType, Document, DocumentRequest, DocumentTemplate, DocumentApproval
)
from events.models import (
    EventCategory, Event, EventParticipant, EventRegistration,
    EventFeedback, EventSchedule, EventDocument
)
from news.models import (
    NewsCategory, News, NewsTag
)
from organization.models import (
    Organization, PerangkatDesa, LembagaAdat, PenggerakPKK, Kepemudaan, KarangTaruna
)
from posyandu.models import (
    PosyanduLocation, PosyanduSchedule, HealthRecord, Immunization, NutritionData,
    PosyanduKader, IbuHamil, PemeriksaanIbuHamil, StuntingData
)
from references.models import (
    Dusun, Lorong, Penduduk, DisabilitasType, DisabilitasData, ReligionReference
)
from tourism.models import (
    TourismCategory, TourismLocation, TourismGallery, TourismReview,
    TourismEvent, TourismRating, TourismPackage, TourismFAQ
)
from village_profile.models import (
    VillageHistory, VillageHistoryPhoto
)
from core.models import (
    CustomUser, UserProfile, UMKMBusiness, WhatsAppBotConfig,
    SystemSettings, WebsiteSettings, ModuleSettings, APIEndpoint, Message
)
from django.contrib.auth import get_user_model

User = get_user_model()
fake = Faker('id_ID')  # Indonesian locale

def create_business_dummy_data():
    print("\n=== MEMBUAT DATA DUMMY BUSINESS ===")
    
    # Business Categories
    print("1. Membuat Business Categories...")
    categories_data = [
        {'name': 'Kuliner', 'description': 'Usaha makanan dan minuman'},
        {'name': 'Kerajinan', 'description': 'Usaha kerajinan tangan'},
        {'name': 'Pertanian', 'description': 'Usaha pertanian dan perkebunan'},
        {'name': 'Perdagangan', 'description': 'Usaha perdagangan umum'},
    ]
    
    for cat_data in categories_data:
        category, created = BusinessCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"   ✓ Created: {category.name}")
    
    # UKM
    print("2. Membuat UKM...")
    categories = list(BusinessCategory.objects.all())
    
    ukm_data = [
        {
            'nama_usaha': 'Warung Makan Bu Sari',
            'pemilik': 'Sari Wulandari',
            'nik_pemilik': '1234567890123456',
            'alamat_usaha': 'Jl. Raya Desa No. 15',
            'alamat_pemilik': 'Jl. Raya Desa No. 15',
            'jenis_usaha': 'Kuliner',
            'skala_usaha': 'mikro',
            'modal_awal': 5000000,
            'omzet_bulanan': 2000000,
            'jumlah_karyawan': 3,
            'tanggal_mulai': date(2018, 1, 15),
            'telepon': '081234567890',
            'produk_utama': 'Nasi gudeg, ayam goreng, sayur lodeh',
            'target_pasar': 'Masyarakat lokal dan wisatawan',
            'status': 'aktif',
        },
        {
            'nama_usaha': 'Toko Kelontong Pak Budi',
            'pemilik': 'Budi Santoso',
            'nik_pemilik': '1234567890123457',
            'alamat_usaha': 'Jl. Pasar Desa No. 8',
            'alamat_pemilik': 'Jl. Pasar Desa No. 8',
            'jenis_usaha': 'Perdagangan',
            'skala_usaha': 'mikro',
            'modal_awal': 10000000,
            'omzet_bulanan': 5000000,
            'jumlah_karyawan': 2,
            'tanggal_mulai': date(2015, 3, 10),
            'telepon': '081234567891',
            'produk_utama': 'Sembako, kebutuhan sehari-hari',
            'target_pasar': 'Masyarakat desa',
            'status': 'aktif',
        },
        {
            'nama_usaha': 'Bengkel Motor Jaya',
            'pemilik': 'Jaya Kusuma',
            'nik_pemilik': '1234567890123458',
            'alamat_usaha': 'Jl. Raya Desa No. 25',
            'alamat_pemilik': 'Jl. Raya Desa No. 25',
            'jenis_usaha': 'Jasa',
            'skala_usaha': 'kecil',
            'modal_awal': 15000000,
            'omzet_bulanan': 8000000,
            'jumlah_karyawan': 4,
            'tanggal_mulai': date(2020, 6, 1),
            'telepon': '081234567892',
            'produk_utama': 'Service motor, spare part',
            'target_pasar': 'Pemilik kendaraan bermotor',
            'status': 'aktif',
        },
    ]
    
    for data in ukm_data:
        ukm, created = UKM.objects.get_or_create(
            nama_usaha=data['nama_usaha'],
            defaults=data
        )
        if created:
            print(f"   ✓ Created UKM: {ukm.nama_usaha}")
    
    # Create additional random UKM entries
    for i in range(2):
        ukm, created = UKM.objects.get_or_create(
            nama_usaha=f"UKM {fake.company()}",
            defaults={
                'pemilik': fake.name(),
                'nik_pemilik': fake.numerify('################'),
                'alamat_usaha': fake.address(),
                'alamat_pemilik': fake.address(),
                'jenis_usaha': random.choice(['Kuliner', 'Perdagangan', 'Jasa', 'Kerajinan']),
                'skala_usaha': random.choice(['mikro', 'kecil', 'menengah']),
                'modal_awal': random.randint(1000000, 20000000),
                'omzet_bulanan': random.randint(1000000, 50000000),
                'jumlah_karyawan': random.randint(1, 20),
                'tanggal_mulai': fake.date_between(start_date='-10y', end_date='today'),
                'telepon': fake.phone_number(),
                'produk_utama': fake.text(max_nb_chars=100),
                'target_pasar': fake.text(max_nb_chars=100),
                'status': random.choice(['aktif', 'tidak_aktif']),
            }
        )
        if created:
            print(f"   ✓ Created UKM: {ukm.nama_usaha}")

def create_beneficiaries_dummy_data():
    print("\n=== MEMBUAT DATA DUMMY BENEFICIARIES ===")
    
    # Beneficiary Categories
    print("1. Membuat Beneficiary Categories...")
    categories_data = [
        {'name': 'Bantuan Sosial', 'description': 'Bantuan untuk masyarakat kurang mampu'},
        {'name': 'Bantuan Pendidikan', 'description': 'Bantuan untuk pendidikan anak'},
        {'name': 'Bantuan Kesehatan', 'description': 'Bantuan untuk kesehatan masyarakat'},
        {'name': 'Bantuan Usaha', 'description': 'Bantuan untuk pengembangan usaha'},
    ]
    
    for cat_data in categories_data:
        category, created = BeneficiaryCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"   ✓ Created: {category.name}")

def create_documents_dummy_data():
    print("\n=== MEMBUAT DATA DUMMY DOCUMENTS ===")
    
    # Document Types
    print("1. Membuat Document Types...")
    doc_types_data = [
        {'name': 'Surat Keterangan Domisili', 'description': 'Surat keterangan tempat tinggal', 'processing_time_days': 3, 'fee': 5000},
        {'name': 'Surat Keterangan Usaha', 'description': 'Surat keterangan untuk usaha', 'processing_time_days': 5, 'fee': 10000},
        {'name': 'Surat Keterangan Tidak Mampu', 'description': 'Surat keterangan ekonomi tidak mampu', 'processing_time_days': 2, 'fee': 0},
        {'name': 'Surat Pengantar Nikah', 'description': 'Surat pengantar untuk menikah', 'processing_time_days': 7, 'fee': 15000},
    ]
    
    for doc_data in doc_types_data:
        doc_type, created = DocumentType.objects.get_or_create(
            name=doc_data['name'],
            defaults={
                'description': doc_data['description'],
                'processing_time_days': doc_data['processing_time_days'],
                'fee': doc_data['fee']
            }
        )
        if created:
            print(f"   ✓ Created: {doc_type.name}")

def create_events_dummy_data():
    print("\n=== MEMBUAT DATA DUMMY EVENTS ===")
    
    # Event Categories
    print("1. Membuat Event Categories...")
    event_categories_data = [
        {'name': 'Kegiatan Sosial', 'description': 'Kegiatan sosial masyarakat', 'icon': 'fas fa-hands-helping', 'color': 'blue'},
        {'name': 'Kegiatan Budaya', 'description': 'Kegiatan budaya dan tradisi', 'icon': 'fas fa-theater-masks', 'color': 'purple'},
        {'name': 'Kegiatan Olahraga', 'description': 'Kegiatan olahraga dan kesehatan', 'icon': 'fas fa-running', 'color': 'green'},
        {'name': 'Kegiatan Pendidikan', 'description': 'Kegiatan pendidikan dan pelatihan', 'icon': 'fas fa-graduation-cap', 'color': 'orange'},
    ]
    
    for cat_data in event_categories_data:
        category, created = EventCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'icon': cat_data['icon'],
                'color': cat_data['color']
            }
        )
        if created:
            print(f"   ✓ Created: {category.name}")
    
    # Events
    print("2. Membuat Events...")
    categories = list(EventCategory.objects.all())
    for i in range(5):
        event_date = fake.date_between(start_date='+1d', end_date='+30d')
        event, created = Event.objects.get_or_create(
            title=f"Event {fake.catch_phrase()}",
            defaults={
                'category': random.choice(categories) if categories else None,
                'description': fake.text(max_nb_chars=300),
                'start_date': event_date,
                'end_date': event_date + timedelta(days=random.randint(1, 3)),
                'start_time': fake.time(),
                'end_time': fake.time(),
                'location': fake.address(),
                'max_participants': random.randint(50, 200),
                'cost': random.choice([0, 25000, 50000, 100000]),
                'status': 'published',
            }
        )
        if created:
            print(f"   ✓ Created Event: {event.title}")

def create_news_dummy_data():
    print("\n=== MEMBUAT DATA DUMMY NEWS ===")
    
    # News Categories
    print("1. Membuat News Categories...")
    news_categories_data = [
        {'name': 'Berita Desa', 'description': 'Berita seputar desa'},
        {'name': 'Pengumuman', 'description': 'Pengumuman resmi desa'},
        {'name': 'Kegiatan', 'description': 'Berita kegiatan desa'},
        {'name': 'Pembangunan', 'description': 'Berita pembangunan desa'},
    ]
    
    for cat_data in news_categories_data:
        category, created = NewsCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"   ✓ Created: {category.name}")

def create_tourism_dummy_data():
    print("\n=== MEMBUAT DATA DUMMY TOURISM ===")
    
    # Tourism Categories
    print("1. Membuat Tourism Categories...")
    tourism_categories_data = [
        {'name': 'Wisata Alam', 'description': 'Tempat wisata alam'},
        {'name': 'Wisata Budaya', 'description': 'Tempat wisata budaya'},
        {'name': 'Wisata Kuliner', 'description': 'Tempat wisata kuliner'},
        {'name': 'Wisata Religi', 'description': 'Tempat wisata religi'},
    ]
    
    categories = []
    for cat_data in tourism_categories_data:
        category, created = TourismCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories.append(category)
        if created:
            print(f"   ✓ Created: {category.name}")
    
    # Tourism Locations
    print("2. Membuat Tourism Locations...")
    location_types = ['natural', 'cultural', 'historical', 'religious', 'culinary']
    
    for i in range(5):
        location, created = TourismLocation.objects.get_or_create(
            title=f"Wisata {fake.city()}",
            defaults={
                'slug': f"wisata-{fake.slug()}-{i}",
                'category': random.choice(categories),
                'location_type': random.choice(location_types),
                'short_description': fake.text(max_nb_chars=200),
                'full_description': fake.text(max_nb_chars=1000),
                'address': fake.address(),
                'latitude': fake.latitude(),
                'longitude': fake.longitude(),
                'opening_hours': '08:00 - 17:00',
                'entry_fee': random.randint(5000, 50000),
                'contact_phone': fake.phone_number(),
                'status': 'published',
                'is_active': True
            }
        )
        if created:
            print(f"   ✓ Created: {location.title}")

def create_references_dummy_data():
    print("\n=== MEMBUAT DATA DUMMY REFERENCES ===")
    
    # Dusun
    print("1. Membuat Dusun...")
    dusun_data = [
        {'name': 'Dusun Mawar', 'code': 'DM01'},
        {'name': 'Dusun Melati', 'code': 'DM02'},
        {'name': 'Dusun Kenanga', 'code': 'DK01'},
        {'name': 'Dusun Cempaka', 'code': 'DC01'},
    ]
    
    for dusun_info in dusun_data:
        dusun, created = Dusun.objects.get_or_create(
            name=dusun_info['name'],
            defaults={'code': dusun_info['code']}
        )
        if created:
            print(f"   ✓ Created: {dusun.name}")

def main():
    print("🚀 MEMULAI PEMBUATAN DATA DUMMY UNTUK SEMUA MODEL")
    print("=" * 60)
    
    try:
        # Create dummy data for each app
        create_references_dummy_data()
        create_business_dummy_data()
        create_beneficiaries_dummy_data()
        create_documents_dummy_data()
        create_events_dummy_data()
        create_news_dummy_data()
        create_tourism_dummy_data()
        
        print("\n" + "=" * 60)
        print("✅ SEMUA DATA DUMMY BERHASIL DIBUAT!")
        print("\n📊 RINGKASAN:")
        print(f"   • Business Categories: {BusinessCategory.objects.count()}")
        print(f"   • UKM: {UKM.objects.count()}")
        print(f"   • Beneficiary Categories: {BeneficiaryCategory.objects.count()}")
        print(f"   • Document Types: {DocumentType.objects.count()}")
        print(f"   • Event Categories: {EventCategory.objects.count()}")
        print(f"   • Events: {Event.objects.count()}")
        print(f"   • News Categories: {NewsCategory.objects.count()}")
        print(f"   • Tourism Categories: {TourismCategory.objects.count()}")
        print(f"   • Dusun: {Dusun.objects.count()}")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()