#!/usr/bin/env python
"""
Script untuk membuat data dummy Dusun dan Lorong
untuk testing dropdown dinamis di form penduduk
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from references.models import Dusun, Lorong

def create_dummy_data():
    """Membuat data dummy dusun dan lorong"""
    
    print("Membuat data dummy Dusun dan Lorong...")
    
    # Data dummy dusun
    dusun_data = [
        {'name': 'Dusun Utara', 'code': 'DU01', 'description': 'Dusun bagian utara desa', 'area_size': 25.5, 'population_count': 150},
        {'name': 'Dusun Selatan', 'code': 'DU02', 'description': 'Dusun bagian selatan desa', 'area_size': 30.2, 'population_count': 200},
        {'name': 'Dusun Timur', 'code': 'DU03', 'description': 'Dusun bagian timur desa', 'area_size': 22.8, 'population_count': 180},
        {'name': 'Dusun Barat', 'code': 'DU04', 'description': 'Dusun bagian barat desa', 'area_size': 28.1, 'population_count': 175},
        {'name': 'Dusun Tengah', 'code': 'DU05', 'description': 'Dusun bagian tengah desa', 'area_size': 35.0, 'population_count': 250},
    ]
    
    # Buat dusun
    created_dusun = []
    for data in dusun_data:
        dusun, created = Dusun.objects.get_or_create(
            code=data['code'],
            defaults={
                'name': data['name'],
                'description': data['description'],
                'area_size': data['area_size'],
                'population_count': data['population_count'],
                'is_active': True
            }
        )
        created_dusun.append(dusun)
        if created:
            print(f"✓ Dusun '{dusun.name}' berhasil dibuat")
        else:
            print(f"- Dusun '{dusun.name}' sudah ada")
    
    # Data dummy lorong untuk setiap dusun
    lorong_data = {
        'DU01': [  # Dusun Utara
            {'name': 'Lorong Mawar', 'code': 'LU01', 'description': 'Lorong dengan bunga mawar', 'length': 150.0, 'house_count': 15},
            {'name': 'Lorong Melati', 'code': 'LU02', 'description': 'Lorong dengan bunga melati', 'length': 120.0, 'house_count': 12},
            {'name': 'Lorong Kenanga', 'code': 'LU03', 'description': 'Lorong dengan bunga kenanga', 'length': 180.0, 'house_count': 18},
        ],
        'DU02': [  # Dusun Selatan
            {'name': 'Lorong Dahlia', 'code': 'LS01', 'description': 'Lorong dengan bunga dahlia', 'length': 200.0, 'house_count': 20},
            {'name': 'Lorong Anggrek', 'code': 'LS02', 'description': 'Lorong dengan bunga anggrek', 'length': 160.0, 'house_count': 16},
            {'name': 'Lorong Tulip', 'code': 'LS03', 'description': 'Lorong dengan bunga tulip', 'length': 140.0, 'house_count': 14},
        ],
        'DU03': [  # Dusun Timur
            {'name': 'Lorong Bambu', 'code': 'LT01', 'description': 'Lorong dengan pohon bambu', 'length': 175.0, 'house_count': 17},
            {'name': 'Lorong Kelapa', 'code': 'LT02', 'description': 'Lorong dengan pohon kelapa', 'length': 190.0, 'house_count': 19},
        ],
        'DU04': [  # Dusun Barat
            {'name': 'Lorong Mangga', 'code': 'LB01', 'description': 'Lorong dengan pohon mangga', 'length': 165.0, 'house_count': 16},
            {'name': 'Lorong Rambutan', 'code': 'LB02', 'description': 'Lorong dengan pohon rambutan', 'length': 155.0, 'house_count': 15},
            {'name': 'Lorong Durian', 'code': 'LB03', 'description': 'Lorong dengan pohon durian', 'length': 170.0, 'house_count': 17},
        ],
        'DU05': [  # Dusun Tengah
            {'name': 'Lorong Utama', 'code': 'LC01', 'description': 'Lorong utama dusun tengah', 'length': 250.0, 'house_count': 25},
            {'name': 'Lorong Pasar', 'code': 'LC02', 'description': 'Lorong dekat pasar', 'length': 200.0, 'house_count': 20},
            {'name': 'Lorong Sekolah', 'code': 'LC03', 'description': 'Lorong dekat sekolah', 'length': 180.0, 'house_count': 18},
            {'name': 'Lorong Masjid', 'code': 'LC04', 'description': 'Lorong dekat masjid', 'length': 160.0, 'house_count': 16},
        ],
    }
    
    # Buat lorong untuk setiap dusun
    total_lorong_created = 0
    for dusun in created_dusun:
        if dusun.code in lorong_data:
            for lorong_info in lorong_data[dusun.code]:
                lorong, created = Lorong.objects.get_or_create(
                    dusun=dusun,
                    code=lorong_info['code'],
                    defaults={
                        'name': lorong_info['name'],
                        'description': lorong_info['description'],
                        'length': lorong_info['length'],
                        'house_count': lorong_info['house_count'],
                        'is_active': True
                    }
                )
                if created:
                    print(f"  ✓ Lorong '{lorong.name}' di {dusun.name} berhasil dibuat")
                    total_lorong_created += 1
                else:
                    print(f"  - Lorong '{lorong.name}' di {dusun.name} sudah ada")
    
    print(f"\n=== RINGKASAN ===")
    print(f"Total Dusun: {Dusun.objects.count()}")
    print(f"Total Lorong: {Lorong.objects.count()}")
    print(f"Lorong baru dibuat: {total_lorong_created}")
    
    # Tampilkan data yang sudah dibuat
    print(f"\n=== DATA DUSUN ===")
    for dusun in Dusun.objects.all().order_by('code'):
        lorong_count = dusun.lorongs.count()
        print(f"- {dusun.name} ({dusun.code}) - {lorong_count} lorong")
        for lorong in dusun.lorongs.all():
            print(f"  • {lorong.name} ({lorong.code})")
    
    print("\n✅ Data dummy berhasil dibuat!")
    print("Sekarang dropdown dusun dan lorong akan terisi secara dinamis.")

if __name__ == '__main__':
    try:
        create_dummy_data()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)