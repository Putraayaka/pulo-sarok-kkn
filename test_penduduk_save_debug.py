#!/usr/bin/env python
import os
import sys
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from references.models import Penduduk, Dusun, Lorong
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

def test_penduduk_save():
    print("=== Test Penyimpanan Data Penduduk ===")
    
    try:
        # Cek apakah ada user untuk created_by
        user = User.objects.first()
        if not user:
            print("❌ Tidak ada user di database. Membuat user test...")
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )
            print("✓ User test berhasil dibuat")
        
        # Cek apakah ada dusun dan lorong
        dusun = Dusun.objects.first()
        lorong = Lorong.objects.first()
        
        if not dusun:
            print("❌ Tidak ada data dusun. Membuat dusun test...")
            dusun = Dusun.objects.create(
                name="Dusun Test",
                created_by=user
            )
            print("✓ Dusun test berhasil dibuat")
            
        if not lorong:
            print("❌ Tidak ada data lorong. Membuat lorong test...")
            lorong = Lorong.objects.create(
                name="Lorong Test",
                dusun=dusun,
                created_by=user
            )
            print("✓ Lorong test berhasil dibuat")
        
        # Test data penduduk
        test_data = {
            'nik': '1234567890123456',
            'name': 'Test Penduduk',
            'gender': 'L',
            'birth_place': 'Jakarta',
            'birth_date': date(1990, 1, 1),
            'religion': 'Islam',
            'marital_status': 'BELUM_KAWIN',
            'dusun': dusun,
            'lorong': lorong,
            'address': 'Alamat Test',
            'created_by': user
        }
        
        print(f"\n=== Mencoba menyimpan data penduduk ===")
        print(f"NIK: {test_data['nik']}")
        print(f"Nama: {test_data['name']}")
        print(f"Dusun: {test_data['dusun'].name}")
        print(f"Lorong: {test_data['lorong'].name}")
        
        # Cek apakah NIK sudah ada
        existing = Penduduk.objects.filter(nik=test_data['nik']).first()
        if existing:
            print(f"⚠️ NIK {test_data['nik']} sudah ada. Menghapus data lama...")
            existing.delete()
        
        # Simpan data baru
        with transaction.atomic():
            penduduk = Penduduk.objects.create(**test_data)
            print(f"✅ Data penduduk berhasil disimpan dengan ID: {penduduk.id}")
            
            # Verifikasi data tersimpan
            saved_penduduk = Penduduk.objects.get(id=penduduk.id)
            print(f"✓ Verifikasi: Data dengan NIK {saved_penduduk.nik} berhasil diambil dari database")
            
            return True
            
    except Exception as e:
        print(f"❌ Error saat menyimpan data: {str(e)}")
        print(f"❌ Type error: {type(e).__name__}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return False

def test_form_validation():
    print("\n=== Test Validasi Form ===")
    
    try:
        from references.forms import PendudukForm
        
        # Test data form
        form_data = {
            'nik': '1234567890123457',
            'name': 'Test Form Penduduk',
            'gender': 'L',
            'birth_place': 'Jakarta',
            'birth_date': '1990-01-01',
            'religion': 'Islam',
            'marital_status': 'BELUM_KAWIN',
            'address': 'Alamat Test Form',
            'citizenship': 'WNI'
        }
        
        # Tambahkan dusun dan lorong jika ada
        dusun = Dusun.objects.first()
        lorong = Lorong.objects.first()
        
        if dusun:
            form_data['dusun'] = dusun.id
        if lorong:
            form_data['lorong'] = lorong.id
            
        print(f"Data form: {form_data}")
        
        form = PendudukForm(data=form_data)
        
        if form.is_valid():
            print("✅ Form valid")
            return True
        else:
            print(f"❌ Form tidak valid: {form.errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error saat validasi form: {str(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        return False

if __name__ == '__main__':
    print("Debugging Penyimpanan Data Penduduk")
    print("====================================")
    
    # Test koneksi database
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Koneksi database berhasil")
    except Exception as e:
        print(f"❌ Koneksi database gagal: {e}")
        sys.exit(1)
    
    # Test penyimpanan data
    save_success = test_penduduk_save()
    
    # Test validasi form
    form_success = test_form_validation()
    
    print("\n=== Ringkasan Test ===")
    print(f"Penyimpanan data: {'✅ Berhasil' if save_success else '❌ Gagal'}")
    print(f"Validasi form: {'✅ Berhasil' if form_success else '❌ Gagal'}")
    
    if save_success and form_success:
        print("\n🎉 Semua test berhasil! Masalah mungkin ada di frontend atau API endpoint.")
    else:
        print("\n⚠️ Ada masalah dengan backend. Periksa error di atas.")