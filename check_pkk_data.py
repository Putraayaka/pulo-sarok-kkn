import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from organization.models import PenggerakPKK
from references.models import Penduduk

print('=== UPDATING PKK DATA WITH SAMPLE VALUES ===')

# Get the first PKK record
if PenggerakPKK.objects.exists():
    pkk = PenggerakPKK.objects.first()
    print(f'Updating PKK record: {pkk}')
    
    # Update empty fields with sample data
    if not pkk.nomor_anggota:
        pkk.nomor_anggota = 'PKK001'
    
    if not pkk.keahlian:
        pkk.keahlian = 'Kepemimpinan, Koordinasi Tim, Pemberdayaan Masyarakat'
    
    if not pkk.pengalaman_organisasi:
        pkk.pengalaman_organisasi = 'Aktif dalam organisasi PKK selama 5 tahun, pernah menjadi koordinator berbagai kegiatan pemberdayaan perempuan dan keluarga.'
    
    if not pkk.deskripsi_tugas:
        pkk.deskripsi_tugas = 'Bertanggung jawab dalam mengkoordinasikan kegiatan PKK di tingkat desa, melaksanakan program pemberdayaan perempuan, dan memfasilitasi kegiatan sosial kemasyarakatan.'
    
    if not pkk.alamat_lengkap:
        pkk.alamat_lengkap = 'Jl. Merdeka No. 15, RT 02/RW 01, Desa Pulo Sarok'
    
    if not pkk.kontak_whatsapp:
        pkk.kontak_whatsapp = '081234567890'
    
    if not pkk.prestasi:
        pkk.prestasi = 'Juara 1 Lomba PKK Tingkat Kecamatan 2023, Penghargaan Tokoh Perempuan Inspiratif 2022'
    
    # Save the updated record
    pkk.save()
    
    print('\n=== UPDATED PKK DATA ===')
    print(f'PKK ID: {pkk.id}')
    print(f'Nama: {pkk.penduduk.name}')
    print(f'Jabatan: {pkk.get_jabatan_display()}')
    print(f'Nomor anggota: {pkk.nomor_anggota}')
    print(f'Tanggal bergabung: {pkk.tanggal_bergabung}')
    print(f'Status: {pkk.get_status_display()}')
    print(f'Keahlian: {pkk.keahlian}')
    print(f'Pengalaman organisasi: {pkk.pengalaman_organisasi[:100]}...')
    print(f'Deskripsi tugas: {pkk.deskripsi_tugas[:100]}...')
    print(f'SK pengangkatan: {pkk.sk_pengangkatan}')
    print(f'Kontak WhatsApp: {pkk.kontak_whatsapp}')
    print(f'Email: {pkk.email}')
    print(f'Alamat lengkap: {pkk.alamat_lengkap}')
    print(f'Prestasi: {pkk.prestasi}')
    
    print(f'\nPKK record updated successfully! You can now view it at:')
    print(f'http://127.0.0.1:8000/pulosarok/organization/penggerak-pkk/{pkk.id}/')
else:
    print('No PKK records found!')