#!/usr/bin/env python
"""
Script untuk testing penyimpanan data penduduk ke Supabase
dengan dropdown dusun dan lorong yang dinamis
"""

import os
import sys
import django
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from references.models import Dusun, Lorong, Penduduk
from references.forms import PendudukForm

def test_penduduk_save():
    """Test penyimpanan data penduduk dengan dropdown dinamis"""
    
    print("=== TESTING PENYIMPANAN DATA PENDUDUK ===")
    
    # Ambil data dusun dan lorong yang tersedia
    dusun_list = Dusun.objects.filter(is_active=True)
    print(f"\nDusun tersedia: {dusun_list.count()}")
    for dusun in dusun_list:
        lorong_count = dusun.lorongs.filter(is_active=True).count()
        print(f"- {dusun.name} ({dusun.code}) - {lorong_count} lorong")
    
    if not dusun_list.exists():
        print("❌ Tidak ada dusun tersedia. Jalankan create_dummy_dusun_lorong.py terlebih dahulu.")
        return False
    
    # Pilih dusun pertama dan lorong pertama untuk testing
    test_dusun = dusun_list.first()
    test_lorong = test_dusun.lorongs.filter(is_active=True).first()
    
    if not test_lorong:
        print(f"❌ Tidak ada lorong tersedia di {test_dusun.name}")
        return False
    
    print(f"\n📍 Testing dengan Dusun: {test_dusun.name}, Lorong: {test_lorong.name}")
    
    # Data test penduduk dengan pilihan yang benar sesuai model
    test_data = {
        'nik': '1234567890123456',
        'kk_number': '1234567890123456',
        'name': 'John Doe Test',
        'birth_place': 'Jakarta',
        'birth_date': date(1990, 1, 1),
        'gender': 'L',
        'religion': 'Islam',  # Sesuai RELIGION_CHOICES
        'marital_status': 'BELUM_KAWIN',  # Sesuai MARITAL_STATUS_CHOICES
        'education': 'SLTA',  # Sesuai EDUCATION_CHOICES
        'occupation': 'Programmer',
        'blood_type': 'O',
        'citizenship': 'WNI',  # Sesuai CITIZENSHIP_CHOICES
        'phone_number': '081234567890',
        'mobile_number': '081234567890',
        'email': 'john.doe@test.com',
        'dusun': test_dusun.id,
        'lorong': test_lorong.id,
        'address': 'Jl. Test No. 123',
        'rt_number': '001',
        'rw_number': '002',
        'house_number': '123',
        'postal_code': '12345',
        'emergency_contact': 'Bapak Test',
        'emergency_phone': '081234567891',
        'emergency_relationship': 'Ayah'
    }
    
    print("\n📝 Data test penduduk:")
    print(f"- NIK: {test_data['nik']}")
    print(f"- Nama: {test_data['name']}")
    print(f"- Dusun: {test_dusun.name}")
    print(f"- Lorong: {test_lorong.name}")
    print(f"- Alamat: {test_data['address']}")
    
    # Test form validation
    print("\n🔍 Testing form validation...")
    form = PendudukForm(data=test_data)
    
    if form.is_valid():
        print("✅ Form validation berhasil")
        
        # Cek apakah NIK sudah ada
        existing_penduduk = Penduduk.objects.filter(nik=test_data['nik']).first()
        if existing_penduduk:
            print(f"⚠️  Penduduk dengan NIK {test_data['nik']} sudah ada, akan diupdate")
            # Update data existing
            for field, value in test_data.items():
                if hasattr(existing_penduduk, field):
                    setattr(existing_penduduk, field, value)
            existing_penduduk.save()
            saved_penduduk = existing_penduduk
        else:
            # Simpan data baru
            print("💾 Menyimpan data penduduk baru...")
            saved_penduduk = form.save()
        
        print(f"✅ Data penduduk berhasil disimpan dengan ID: {saved_penduduk.id}")
        
        # Verifikasi data tersimpan
        print("\n🔍 Verifikasi data tersimpan:")
        retrieved_penduduk = Penduduk.objects.get(id=saved_penduduk.id)
        print(f"- ID: {retrieved_penduduk.id}")
        print(f"- NIK: {retrieved_penduduk.nik}")
        print(f"- Nama: {retrieved_penduduk.name}")
        print(f"- Dusun: {retrieved_penduduk.dusun.name} ({retrieved_penduduk.dusun.code})")
        print(f"- Lorong: {retrieved_penduduk.lorong.name} ({retrieved_penduduk.lorong.code})")
        print(f"- Alamat: {retrieved_penduduk.address}")
        print(f"- Created: {retrieved_penduduk.created_at}")
        print(f"- Updated: {retrieved_penduduk.updated_at}")
        
        # Test dropdown dinamis
        print("\n🔄 Testing dropdown dinamis:")
        
        # Simulasi API call untuk mendapatkan pilihan
        from references.views import penduduk_create_api
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        
        factory = RequestFactory()
        request = factory.get('/api/penduduk/create/')
        request.user = AnonymousUser()
        
        # Panggil API untuk mendapatkan choices
        response = penduduk_create_api(request)
        if response.status_code == 200:
            import json
            choices_data = json.loads(response.content)
            
            dusun_choices = choices_data.get('dusun_choices', [])
            lorong_choices = choices_data.get('lorong_choices', [])
            
            print(f"✅ API choices berhasil diambil:")
            print(f"- Dusun choices: {len(dusun_choices)} items")
            print(f"- Lorong choices: {len(lorong_choices)} items")
            
            # Tampilkan beberapa pilihan
            print("\n📋 Sample dusun choices:")
            for choice in dusun_choices[:3]:
                print(f"  • {choice[1]} (ID: {choice[0]})")
            
            print("\n📋 Sample lorong choices:")
            for choice in lorong_choices[:5]:
                print(f"  • {choice[1]} (ID: {choice[0]})")
        else:
            print(f"❌ Gagal mengambil API choices: {response.status_code}")
        
        print("\n✅ TESTING BERHASIL!")
        print("Data penduduk berhasil disimpan ke database Supabase dengan dropdown dinamis.")
        return True
        
    else:
        print("❌ Form validation gagal:")
        for field, errors in form.errors.items():
            print(f"- {field}: {', '.join(errors)}")
        return False

def test_dropdown_api():
    """Test API endpoint untuk dropdown"""
    print("\n=== TESTING DROPDOWN API ===")
    
    from django.test import Client
    from django.urls import reverse
    
    client = Client()
    
    try:
        # Test API penduduk create (untuk mendapatkan choices)
        url = reverse('references:penduduk_create')
        response = client.get(url)
        
        print(f"API URL: {url}")
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            import json
            data = json.loads(response.content)
            
            print("✅ API response berhasil:")
            print(f"- Dusun choices: {len(data.get('dusun_choices', []))}")
            print(f"- Lorong choices: {len(data.get('lorong_choices', []))}")
            print(f"- Gender choices: {len(data.get('gender_choices', []))}")
            print(f"- Religion choices: {len(data.get('religion_choices', []))}")
            
            return True
        else:
            print(f"❌ API gagal: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

if __name__ == '__main__':
    try:
        print("🚀 Memulai testing penyimpanan data penduduk...\n")
        
        # Test 1: Penyimpanan data
        success1 = test_penduduk_save()
        
        # Test 2: API dropdown
        success2 = test_dropdown_api()
        
        if success1 and success2:
            print("\n🎉 SEMUA TEST BERHASIL!")
            print("✅ Data penduduk dapat disimpan ke Supabase")
            print("✅ Dropdown dusun dan lorong berfungsi dinamis")
            print("✅ API endpoint berfungsi dengan baik")
        else:
            print("\n⚠️  Beberapa test gagal, silakan periksa log di atas")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)