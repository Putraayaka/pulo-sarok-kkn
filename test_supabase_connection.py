#!/usr/bin/env python
"""
Script untuk test koneksi ke Supabase database
"""

import os
import sys
from urllib.parse import urlparse
from decouple import config

def test_supabase_connection():
    print("=== Test Koneksi Supabase ===")
    
    # Load DATABASE_URL dari .env
    try:
        database_url = config("DATABASE_URL")
        print(f"✓ DATABASE_URL ditemukan: {database_url[:50]}...")
    except Exception as e:
        print(f"✗ Error loading DATABASE_URL: {e}")
        return False
    
    # Parse URL
    try:
        parsed = urlparse(database_url)
        print(f"✓ Host: {parsed.hostname}")
        print(f"✓ Port: {parsed.port}")
        print(f"✓ Database: {parsed.path[1:]}")
        print(f"✓ Username: {parsed.username}")
    except Exception as e:
        print(f"✗ Error parsing URL: {e}")
        return False
    
    # Test DNS resolution
    print("\n=== Test DNS Resolution ===")
    import socket
    try:
        ip = socket.gethostbyname(parsed.hostname)
        print(f"✓ DNS Resolution berhasil: {parsed.hostname} -> {ip}")
    except socket.gaierror as e:
        print(f"✗ DNS Resolution gagal: {e}")
        print("Kemungkinan penyebab:")
        print("  - Hostname salah dalam connection string")
        print("  - Masalah koneksi internet")
        print("  - DNS server bermasalah")
        return False
    
    # Test database connection
    print("\n=== Test Database Connection ===")
    try:
        import psycopg2
        conn = psycopg2.connect(database_url)
        print("✓ Koneksi database berhasil!")
        
        # Test simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✓ PostgreSQL Version: {version[:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print("✗ psycopg2 tidak terinstall")
        print("Install dengan: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"✗ Koneksi database gagal: {e}")
        print("Kemungkinan penyebab:")
        print("  - Password salah")
        print("  - Database tidak aktif")
        print("  - Firewall memblokir port 5432")
        print("  - SSL configuration bermasalah")
        return False

def main():
    print("Supabase Connection Tester")
    print("=" * 40)
    
    success = test_supabase_connection()
    
    if success:
        print("\n🎉 Semua test berhasil! Database siap digunakan.")
        print("Jalankan: python manage.py migrate")
    else:
        print("\n❌ Ada masalah dengan koneksi database.")
        print("Periksa connection string di file .env")
        print("Atau gunakan SQLite untuk development dengan menghapus DATABASE_URL dari .env")

if __name__ == "__main__":
    main()