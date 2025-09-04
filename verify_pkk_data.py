import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from organization.models import PenggerakPKK
from references.models import Penduduk

print('=== VERIFYING PKK DATA ===')

# Check PKK record with ID 17
try:
    pkk = PenggerakPKK.objects.get(id=17)
    print(f'Found PKK record: {pkk}')
    print(f'ID: {pkk.id}')
    print(f'Nama: {pkk.penduduk.name}')
    print(f'NIK: {pkk.penduduk.nik}')
    print(f'Jabatan: {pkk.get_jabatan_display()}')
    print(f'Nomor anggota: "{pkk.nomor_anggota}"')
    print(f'Tanggal bergabung: {pkk.tanggal_bergabung}')
    print(f'Status: {pkk.get_status_display()}')
    print(f'Keahlian: "{pkk.keahlian}"')
    print(f'Pengalaman organisasi: "{pkk.pengalaman_organisasi}"')
    print(f'Deskripsi tugas: "{pkk.deskripsi_tugas}"')
    print(f'SK pengangkatan: "{pkk.sk_pengangkatan}"')
    print(f'Kontak WhatsApp: "{pkk.kontak_whatsapp}"')
    print(f'Email: "{pkk.email}"')
    print(f'Alamat lengkap: "{pkk.alamat_lengkap}"')
    print(f'Prestasi: "{pkk.prestasi}"')
    
    # Check if fields are empty or None
    empty_fields = []
    if not pkk.nomor_anggota:
        empty_fields.append('nomor_anggota')
    if not pkk.keahlian:
        empty_fields.append('keahlian')
    if not pkk.pengalaman_organisasi:
        empty_fields.append('pengalaman_organisasi')
    if not pkk.deskripsi_tugas:
        empty_fields.append('deskripsi_tugas')
    if not pkk.alamat_lengkap:
        empty_fields.append('alamat_lengkap')
    if not pkk.kontak_whatsapp:
        empty_fields.append('kontak_whatsapp')
    if not pkk.prestasi:
        empty_fields.append('prestasi')
    
    if empty_fields:
        print(f'\nEmpty fields found: {empty_fields}')
    else:
        print('\nAll fields have data!')
        
except PenggerakPKK.DoesNotExist:
    print('PKK record with ID 17 not found!')
except Exception as e:
    print(f'Error: {e}')

print('\n=== VERIFICATION COMPLETE ===')