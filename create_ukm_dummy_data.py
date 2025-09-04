#!/usr/bin/env python
"""
Script untuk membuat data dummy UKM saja
"""

import os
import sys
import django
from datetime import date
from faker import Faker
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

# Import models
from business.models import UKM

fake = Faker('id_ID')  # Indonesian locale

def create_ukm_dummy_data():
    print("Creating UKM dummy data...")
    
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
        else:
            print(f"   - UKM already exists: {ukm.nama_usaha}")
    
    print(f"\nTotal UKM: {UKM.objects.count()}")

if __name__ == '__main__':
    create_ukm_dummy_data()