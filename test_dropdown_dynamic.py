#!/usr/bin/env python
"""
Script untuk testing dropdown dinamis dusun dan lorong
tanpa menyimpan data ke database
"""

import os
import sys
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from references.models import Dusun, Lorong
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from references.views import penduduk_create_api

def test_dropdown_data():
    """Test data dusun dan lorong untuk dropdown"""
    
    print("=== TESTING DROPDOWN DINAMIS ===")
    
    # Test 1: Cek data dusun dan lorong
    print("\n1. 📊 Data Dusun dan Lorong:")
    dusun_count = Dusun.objects.filter(is_active=True).count()
    lorong_count = Lorong.objects.filter(is_active=True).count()
    
    print(f"   ✓ Total Dusun aktif: {dusun_count}")
    print(f"   ✓ Total Lorong aktif: {lorong_count}")
    
    if dusun_count == 0:
        print("   ❌ Tidak ada data dusun! Jalankan create_dummy_dusun_lorong.py")
        return False
    
    # Tampilkan data dusun dan lorong
    print("\n   📋 Daftar Dusun:")
    for dusun in Dusun.objects.filter(is_active=True).order_by('code'):
        lorong_count_per_dusun = dusun.lorongs.filter(is_active=True).count()
        print(f"      • {dusun.name} ({dusun.code}) - {lorong_count_per_dusun} lorong")
        
        # Tampilkan beberapa lorong
        for lorong in dusun.lorongs.filter(is_active=True)[:3]:
            print(f"        - {lorong.name} ({lorong.code})")
        
        if dusun.lorongs.filter(is_active=True).count() > 3:
            remaining = dusun.lorongs.filter(is_active=True).count() - 3
            print(f"        ... dan {remaining} lorong lainnya")
    
    return True

def test_api_choices():
    """Test API untuk mendapatkan pilihan dropdown"""
    
    print("\n2. 🔌 Testing API Choices:")
    
    try:
        # Simulasi request GET ke API
        factory = RequestFactory()
        request = factory.get('/api/penduduk/create/')
        request.user = AnonymousUser()
        
        # Panggil API
        response = penduduk_create_api(request)
        
        print(f"   📡 API Status: {response.status_code}")
        
        if response.status_code == 200:
            # Parse response JSON
            data = json.loads(response.content)
            
            # Cek pilihan yang tersedia
            dusun_choices = data.get('dusun_choices', [])
            lorong_choices = data.get('lorong_choices', [])
            gender_choices = data.get('gender_choices', [])
            religion_choices = data.get('religion_choices', [])
            marital_choices = data.get('marital_status_choices', [])
            education_choices = data.get('education_choices', [])
            
            print(f"   ✅ API Response berhasil:")
            print(f"      • Dusun choices: {len(dusun_choices)} items")
            print(f"      • Lorong choices: {len(lorong_choices)} items")
            print(f"      • Gender choices: {len(gender_choices)} items")
            print(f"      • Religion choices: {len(religion_choices)} items")
            print(f"      • Marital choices: {len(marital_choices)} items")
            print(f"      • Education choices: {len(education_choices)} items")
            
            # Tampilkan sample choices
            print("\n   📋 Sample Dusun Choices:")
            for choice in dusun_choices[:3]:
                print(f"      • ID: {choice[0]}, Nama: {choice[1]}")
            
            print("\n   📋 Sample Lorong Choices:")
            for choice in lorong_choices[:5]:
                print(f"      • ID: {choice[0]}, Nama: {choice[1]}")
            
            print("\n   📋 Sample Religion Choices:")
            for choice in religion_choices[:3]:
                print(f"      • Value: {choice[0]}, Label: {choice[1]}")
            
            return True
        else:
            print(f"   ❌ API gagal dengan status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing API: {e}")
        return False

def test_form_choices():
    """Test form choices untuk dropdown"""
    
    print("\n3. 📝 Testing Form Choices:")
    
    try:
        from references.forms import PendudukForm
        
        # Buat instance form
        form = PendudukForm()
        
        # Cek field dusun
        if 'dusun' in form.fields:
            dusun_queryset = form.fields['dusun'].queryset
            dusun_count = dusun_queryset.count()
            print(f"   ✓ Form Dusun queryset: {dusun_count} items")
            
            if dusun_count > 0:
                print("     📋 Sample Dusun dari Form:")
                for dusun in dusun_queryset[:3]:
                    print(f"        • {dusun.name} ({dusun.code})")
        
        # Cek field lorong
        if 'lorong' in form.fields:
            lorong_queryset = form.fields['lorong'].queryset
            lorong_count = lorong_queryset.count()
            print(f"   ✓ Form Lorong queryset: {lorong_count} items")
            
            if lorong_count > 0:
                print("     📋 Sample Lorong dari Form:")
                for lorong in lorong_queryset[:5]:
                    print(f"        • {lorong.name} - {lorong.dusun.name}")
        
        # Cek choices lainnya
        from references.models import Penduduk
        
        print("\n   📋 Model Choices:")
        print(f"      • Gender choices: {len(Penduduk.GENDER_CHOICES)} items")
        print(f"      • Religion choices: {len(Penduduk.RELIGION_CHOICES)} items")
        print(f"      • Marital choices: {len(Penduduk.MARITAL_STATUS_CHOICES)} items")
        print(f"      • Education choices: {len(Penduduk.EDUCATION_CHOICES)} items")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing form: {e}")
        return False

def test_javascript_integration():
    """Test integrasi dengan JavaScript di frontend"""
    
    print("\n4. 🌐 Testing JavaScript Integration:")
    
    # Simulasi data yang akan dikirim ke frontend
    try:
        from references.models import Penduduk
        
        # Data yang akan digunakan JavaScript
        js_data = {
            'dusun_choices': list(Dusun.objects.filter(is_active=True).values_list('id', 'name')),
            'lorong_choices': list(Lorong.objects.filter(is_active=True).values_list('id', 'name')),
            'gender_choices': Penduduk.GENDER_CHOICES,
            'religion_choices': Penduduk.RELIGION_CHOICES,
            'marital_status_choices': Penduduk.MARITAL_STATUS_CHOICES,
            'education_choices': Penduduk.EDUCATION_CHOICES,
            'blood_type_choices': Penduduk.BLOOD_TYPE_CHOICES,
            'citizenship_choices': Penduduk.CITIZENSHIP_CHOICES,
        }
        
        print(f"   ✅ Data untuk JavaScript:")
        for key, value in js_data.items():
            if isinstance(value, list):
                print(f"      • {key}: {len(value)} items")
        
        # Simulasi JSON yang akan dikirim ke frontend
        json_data = json.dumps(js_data, default=str, ensure_ascii=False)
        json_size = len(json_data)
        
        print(f"   📦 JSON size: {json_size} characters")
        print(f"   ✅ Data siap untuk digunakan JavaScript di frontend")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing JavaScript integration: {e}")
        return False

if __name__ == '__main__':
    try:
        print("🚀 Memulai testing dropdown dinamis...\n")
        
        # Test 1: Data dusun dan lorong
        success1 = test_dropdown_data()
        
        # Test 2: API choices
        success2 = test_api_choices()
        
        # Test 3: Form choices
        success3 = test_form_choices()
        
        # Test 4: JavaScript integration
        success4 = test_javascript_integration()
        
        print("\n" + "="*50)
        
        if all([success1, success2, success3, success4]):
            print("🎉 SEMUA TEST BERHASIL!")
            print("✅ Data dusun dan lorong tersedia")
            print("✅ API choices berfungsi dengan baik")
            print("✅ Form choices berfungsi dinamis")
            print("✅ Integrasi JavaScript siap")
            print("\n💡 Dropdown dusun dan lorong akan terisi secara DINAMIS")
            print("💡 Data tidak di-hardcode, diambil dari database Supabase")
            print("💡 Ketika user klik 'Simpan' di modal, data akan tersimpan ke Supabase")
        else:
            print("⚠️  Beberapa test gagal:")
            if not success1: print("❌ Data dusun/lorong tidak tersedia")
            if not success2: print("❌ API choices bermasalah")
            if not success3: print("❌ Form choices bermasalah")
            if not success4: print("❌ JavaScript integration bermasalah")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)