#!/usr/bin/env python
import os
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from django.db import connection
from business.models import Aset

print('=== CREATING SAMPLE ASET DATA ===')

# First, let's check if the table exists and its structure
with connection.cursor() as cursor:
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='business_aset';")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print('Table business_aset exists')
            cursor.execute("PRAGMA table_info(business_aset);")
            columns = cursor.fetchall()
            print('Table columns:')
            for col in columns:
                print(f'  - {col[1]} ({col[2]})')
        else:
            print('Table business_aset does not exist!')
            exit(1)
            
    except Exception as e:
        print(f'Error checking table: {e}')
        exit(1)

# Try to create sample data using raw SQL
sample_data = [
    {
        'nama': 'Komputer Desktop',
        'kategori': 'peralatan',
        'kode_aset': 'KOMP001',
        'deskripsi': 'Komputer untuk administrasi desa',
        'lokasi': 'Kantor Desa',
        'nilai': 5000000.00,
        'tanggal_perolehan': '2024-01-15',
        'kondisi': 'baik',
        'masa_manfaat': 5,
        'penyusutan_per_tahun': 1000000.00,
        'nilai_buku': 4000000.00,
        'penanggung_jawab': 'Admin Desa',
        'nomor_sertifikat': '',
        'keterangan': 'Komputer untuk keperluan administrasi'
    },
    {
        'nama': 'Meja Kerja Kayu',
        'kategori': 'inventaris',
        'kode_aset': 'MEJA001',
        'deskripsi': 'Meja kerja dari kayu jati',
        'lokasi': 'Ruang Kepala Desa',
        'nilai': 1500000.00,
        'tanggal_perolehan': '2023-06-10',
        'kondisi': 'baik',
        'masa_manfaat': 10,
        'penyusutan_per_tahun': 150000.00,
        'nilai_buku': 1275000.00,
        'penanggung_jawab': 'Kepala Desa',
        'nomor_sertifikat': '',
        'keterangan': 'Meja kerja untuk kepala desa'
    },
    {
        'nama': 'Kursi Kantor',
        'kategori': 'inventaris',
        'kode_aset': 'KURSI001',
        'deskripsi': 'Kursi kantor ergonomis',
        'lokasi': 'Ruang Staff',
        'nilai': 800000.00,
        'tanggal_perolehan': '2023-08-20',
        'kondisi': 'rusak_ringan',
        'masa_manfaat': 8,
        'penyusutan_per_tahun': 100000.00,
        'nilai_buku': 675000.00,
        'penanggung_jawab': 'Staff Admin',
        'nomor_sertifikat': '',
        'keterangan': 'Kursi dengan roda yang perlu diperbaiki'
    },
    {
        'nama': 'Printer Laser',
        'kategori': 'peralatan',
        'kode_aset': 'PRINT001',
        'deskripsi': 'Printer laser untuk dokumen',
        'lokasi': 'Ruang Admin',
        'nilai': 2500000.00,
        'tanggal_perolehan': '2024-03-01',
        'kondisi': 'baik',
        'masa_manfaat': 6,
        'penyusutan_per_tahun': 416666.67,
        'nilai_buku': 2083333.33,
        'penanggung_jawab': 'Admin Desa',
        'nomor_sertifikat': '',
        'keterangan': 'Printer untuk keperluan cetak dokumen'
    },
    {
        'nama': 'Motor Dinas',
        'kategori': 'kendaraan',
        'kode_aset': 'MOTOR001',
        'deskripsi': 'Motor untuk keperluan dinas',
        'lokasi': 'Parkir Kantor Desa',
        'nilai': 18000000.00,
        'tanggal_perolehan': '2022-12-15',
        'kondisi': 'baik',
        'masa_manfaat': 8,
        'penyusutan_per_tahun': 2250000.00,
        'nilai_buku': 13500000.00,
        'penanggung_jawab': 'Kepala Desa',
        'nomor_sertifikat': 'BPKB123456',
        'keterangan': 'Motor untuk keperluan dinas luar'
    }
]

with connection.cursor() as cursor:
    try:
        # Clear existing data
        cursor.execute("DELETE FROM business_aset;")
        print('Cleared existing data')
        
        # Insert sample data
        for i, data in enumerate(sample_data, 1):
            sql = """
            INSERT INTO business_aset (
                nama, kategori, kode_aset, deskripsi, lokasi, 
                nilai, tanggal_perolehan, kondisi, masa_manfaat,
                penyusutan_per_tahun, nilai_buku, penanggung_jawab, 
                nomor_sertifikat, keterangan, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, datetime('now'), datetime('now')
            )
            """
            
            cursor.execute(sql, (
                data['nama'], data['kategori'], data['kode_aset'],
                data['deskripsi'], data['lokasi'], data['nilai'],
                data['tanggal_perolehan'], data['kondisi'], data['masa_manfaat'],
                data['penyusutan_per_tahun'], data['nilai_buku'], 
                data['penanggung_jawab'], data['nomor_sertifikat'], data['keterangan']
            ))
            print(f'Created: {data["nama"]}')
        
        # Commit the transaction
        connection.commit()
        print(f'\nSuccessfully created {len(sample_data)} sample assets!')
        
        # Verify the data
        cursor.execute("SELECT COUNT(*) FROM business_aset;")
        count = cursor.fetchone()[0]
        print(f'Total assets in database: {count}')
        
        cursor.execute("SELECT nama, kategori, kondisi FROM business_aset LIMIT 5;")
        assets = cursor.fetchall()
        print('\nSample data:')
        for asset in assets:
            print(f'  - {asset[0]} ({asset[1]}) - {asset[2]}')
            
    except Exception as e:
        print(f'Error creating sample data: {e}')
        connection.rollback()

print('\n=== DONE ===')