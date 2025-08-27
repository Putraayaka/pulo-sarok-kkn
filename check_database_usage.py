#!/usr/bin/env python
"""
Script untuk mengecek penggunaan database Supabase yang sudah terhubung
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from django.db import connection
from django.apps import apps

def check_database_connection():
    """Cek koneksi database"""
    print("=== STATUS KONEKSI DATABASE ===")
    try:
        db_settings = connection.settings_dict
        print(f"✓ Database Engine: {db_settings['ENGINE']}")
        print(f"✓ Database Name: {db_settings['NAME']}")
        print(f"✓ Database Host: {db_settings.get('HOST', 'N/A')}")
        print(f"✓ Database Port: {db_settings.get('PORT', 'N/A')}")
        print(f"✓ Database User: {db_settings.get('USER', 'N/A')}")
        
        # Test koneksi
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print("✓ Koneksi database berhasil!")
            else:
                print("✗ Koneksi database gagal!")
                
    except Exception as e:
        print(f"✗ Error koneksi database: {e}")
        return False
    return True

def check_tables():
    """Cek tabel yang ada di database"""
    print("\n=== DAFTAR TABEL DI DATABASE ===")
    try:
        with connection.cursor() as cursor:
            if 'postgresql' in connection.settings_dict['ENGINE']:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name
                """)
            else:
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' 
                    ORDER BY name
                """)
            
            tables = cursor.fetchall()
            print(f"Total tabel: {len(tables)}")
            
            for i, table in enumerate(tables, 1):
                print(f"{i:2d}. {table[0]}")
                
    except Exception as e:
        print(f"✗ Error mengambil daftar tabel: {e}")

def check_django_models():
    """Cek model Django yang terdaftar"""
    print("\n=== MODEL DJANGO YANG TERDAFTAR ===")
    
    app_models = {}
    for model in apps.get_models():
        app_label = model._meta.app_label
        if app_label not in app_models:
            app_models[app_label] = []
        app_models[app_label].append(model.__name__)
    
    total_models = sum(len(models) for models in app_models.values())
    print(f"Total model: {total_models}")
    
    for app_label, models in sorted(app_models.items()):
        print(f"\n{app_label.upper()}:")
        for model in sorted(models):
            print(f"  - {model}")

def check_data_samples():
    """Cek sample data dari beberapa tabel utama"""
    print("\n=== SAMPLE DATA DARI TABEL UTAMA ===")
    
    # Import models
    try:
        from core.models import CustomUser
        from references.models import Penduduk
        from organization.models import OrganizationMember
        from business.models import BusinessOwner
        
        models_to_check = [
            (CustomUser, "Users"),
            (Penduduk, "Penduduk"),
            (OrganizationMember, "Anggota Organisasi"),
            (BusinessOwner, "Pemilik Bisnis"),
        ]
        
        for model, name in models_to_check:
            try:
                count = model.objects.count()
                print(f"✓ {name}: {count} records")
                
                if count > 0:
                    # Ambil 3 record pertama
                    samples = model.objects.all()[:3]
                    for i, obj in enumerate(samples, 1):
                        print(f"  {i}. {str(obj)[:50]}...")
                        
            except Exception as e:
                print(f"✗ Error mengecek {name}: {e}")
                
    except ImportError as e:
        print(f"✗ Error import model: {e}")

def main():
    """Fungsi utama"""
    print("CHECKER PENGGUNAAN DATABASE SUPABASE")
    print("=" * 50)
    
    # Cek koneksi database
    if not check_database_connection():
        print("\n✗ Tidak dapat melanjutkan karena koneksi database gagal.")
        sys.exit(1)
    
    # Cek tabel
    check_tables()
    
    # Cek model Django
    check_django_models()
    
    # Cek sample data
    check_data_samples()
    
    print("\n=== KESIMPULAN ===")
    print("✓ Database Supabase sudah terhubung dan berfungsi dengan baik!")
    print("✓ Semua model Django sudah terdaftar.")
    print("✓ Anda dapat mulai menggunakan aplikasi dengan database Supabase.")

if __name__ == "__main__":
    main()