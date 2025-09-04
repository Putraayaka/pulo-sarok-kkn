#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from business.models import Aset

print('=== CHECKING ASET DATA ===')
print(f'Total aset: {Aset.objects.count()}')
print('\nData aset:')

if Aset.objects.count() == 0:
    print('Tidak ada data aset di database!')
    print('\nMembuat data contoh...')
    
    # Create sample data
    sample_assets = [
        {
            'nama_aset': 'Komputer Desktop',
            'kategori': 'elektronik',
            'kode_aset': 'KOMP001',
            'deskripsi': 'Komputer untuk administrasi',
            'lokasi': 'Kantor Desa',
            'kondisi': 'baik',
            'nilai_perolehan': 5000000,
            'masa_manfaat': 5,
            'penanggung_jawab': 'Admin Desa'
        },
        {
            'nama_aset': 'Meja Kerja',
            'kategori': 'furniture',
            'kode_aset': 'MEJA001',
            'deskripsi': 'Meja kerja kayu',
            'lokasi': 'Kantor Desa',
            'kondisi': 'baik',
            'nilai_perolehan': 1500000,
            'masa_manfaat': 10,
            'penanggung_jawab': 'Admin Desa'
        },
        {
            'nama_aset': 'Kursi Kantor',
            'kategori': 'furniture',
            'kode_aset': 'KURSI001',
            'deskripsi': 'Kursi kantor ergonomis',
            'lokasi': 'Kantor Desa',
            'kondisi': 'rusak_ringan',
            'nilai_perolehan': 800000,
            'masa_manfaat': 8,
            'penanggung_jawab': 'Admin Desa'
        }
    ]
    
    for asset_data in sample_assets:
        aset = Aset.objects.create(**asset_data)
        print(f'Created: {aset.nama_aset}')
    
    print(f'\nTotal aset setelah membuat data: {Aset.objects.count()}')
else:
    for aset in Aset.objects.all()[:10]:
        print(f'- {aset.nama_aset} ({aset.kategori}) - {aset.kondisi}')

print('\n=== CHECKING STATISTICS ===')
total_aset = Aset.objects.count()
baik = Aset.objects.filter(kondisi='baik').count()
perlu_perbaikan = Aset.objects.filter(kondisi__in=['rusak_ringan', 'rusak_berat', 'tidak_dapat_digunakan']).count()

print(f'Total Aset: {total_aset}')
print(f'Kondisi Baik: {baik}')
print(f'Perlu Perbaikan: {perlu_perbaikan}')

# Check nilai_perolehan sum
try:
    total_nilai = Aset.objects.aggregate(total=django.db.models.Sum('nilai_perolehan'))['total']
    print(f'Total Nilai: Rp {total_nilai or 0:,.0f}')
except Exception as e:
    print(f'Error calculating total nilai: {e}')

print('\n=== DONE ===')