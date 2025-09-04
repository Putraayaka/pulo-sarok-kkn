import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from organization.models import PenggerakPKK
from references.models import Penduduk

print('=== FIXING PKK DATA ===')

# Get PKK record with ID 17
try:
    pkk = PenggerakPKK.objects.get(id=17)
    print(f'Found PKK record: {pkk}')
    
    # Force update all fields
    pkk.nomor_anggota = 'PKK001'
    pkk.keahlian = 'Kepemimpinan, Koordinasi Tim, Pemberdayaan Masyarakat'
    pkk.pengalaman_organisasi = 'Aktif dalam organisasi PKK selama 5 tahun, pernah menjadi koordinator berbagai kegiatan pemberdayaan perempuan dan keluarga.'
    pkk.deskripsi_tugas = 'Bertanggung jawab dalam mengkoordinasikan kegiatan PKK di tingkat desa, melaksanakan program pemberdayaan perempuan, dan memfasilitasi kegiatan sosial kemasyarakatan.'
    pkk.alamat_lengkap = 'Jl. Merdeka No. 15, RT 02/RW 01, Desa Pulo Sarok'
    pkk.kontak_whatsapp = '081234567890'
    pkk.prestasi = 'Juara 1 Lomba PKK Tingkat Kecamatan 2023, Penghargaan Tokoh Perempuan Inspiratif 2022'
    
    # Save with force update
    pkk.save(update_fields=[
        'nomor_anggota', 'keahlian', 'pengalaman_organisasi', 
        'deskripsi_tugas', 'alamat_lengkap', 'kontak_whatsapp', 'prestasi'
    ])
    
    print('Data updated successfully!')
    
    # Verify the update
    pkk.refresh_from_db()
    print('\n=== VERIFICATION AFTER UPDATE ===')
    print(f'Nomor anggota: "{pkk.nomor_anggota}"')
    print(f'Keahlian: "{pkk.keahlian}"')
    print(f'Pengalaman organisasi: "{pkk.pengalaman_organisasi[:50]}..."')
    print(f'Deskripsi tugas: "{pkk.deskripsi_tugas[:50]}..."')
    print(f'Alamat lengkap: "{pkk.alamat_lengkap}"')
    print(f'Kontak WhatsApp: "{pkk.kontak_whatsapp}"')
    print(f'Prestasi: "{pkk.prestasi[:50]}..."')
    
except PenggerakPKK.DoesNotExist:
    print('PKK record with ID 17 not found!')
except Exception as e:
    print(f'Error: {e}')

print('\n=== COMPLETE ===')