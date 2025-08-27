import os
import sys
import django
from datetime import date, timedelta
import random
from faker import Faker

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from organization.models import (
    OrganizationType, Organization, OrganizationMember, 
    Jabatan, PeriodeKepengurusan, AnggotaOrganisasi
)
from references.models import Penduduk

fake = Faker('id_ID')

def create_organization_dummy_data():
    print("Membuat data dummy untuk organisasi...")
    
    # 1. Buat OrganizationType (Kategori Organisasi)
    print("1. Membuat kategori organisasi...")
    org_types_data = [
        {'name': 'Badan Permusyawaratan Desa', 'description': 'Lembaga perwakilan masyarakat desa yang bertugas mengawasi dan memberikan masukan kepada pemerintah desa'},
        {'name': 'Pemberdayaan Kesejahteraan Keluarga', 'description': 'Organisasi pemberdayaan perempuan untuk meningkatkan kesejahteraan keluarga'},
        {'name': 'Karang Taruna', 'description': 'Organisasi kepemudaan desa untuk pengembangan generasi muda'},
        {'name': 'Lembaga Pemberdayaan Masyarakat', 'description': 'Lembaga yang bertugas memberdayakan masyarakat desa'},
        {'name': 'Rukun Tetangga', 'description': 'Organisasi masyarakat tingkat RT'},
        {'name': 'Rukun Warga', 'description': 'Organisasi masyarakat tingkat RW'},
        {'name': 'Kelompok Tani', 'description': 'Organisasi petani untuk meningkatkan produktivitas pertanian'},
        {'name': 'Posyandu', 'description': 'Pos pelayanan terpadu kesehatan masyarakat'},
        {'name': 'Majelis Taklim', 'description': 'Organisasi keagamaan untuk pembelajaran agama'},
        {'name': 'Koperasi Desa', 'description': 'Koperasi untuk mengembangkan ekonomi desa'},
        {'name': 'Tim Penggerak PKK', 'description': 'Tim penggerak pemberdayaan kesejahteraan keluarga'},
        {'name': 'Kelompok Usaha Bersama', 'description': 'Kelompok usaha ekonomi masyarakat'}
    ]
    
    org_types = []
    for data in org_types_data:
        org_type, created = OrganizationType.objects.get_or_create(
            name=data['name'],
            defaults={'description': data['description']}
        )
        org_types.append(org_type)
        if created:
            print(f"   - Created: {org_type.name}")
    
    # 2. Buat Jabatan
    print("2. Membuat jabatan...")
    jabatan_data = [
        {'nama_jabatan': 'Ketua', 'level_hierarki': 1, 'deskripsi': 'Pemimpin organisasi'},
        {'nama_jabatan': 'Wakil Ketua', 'level_hierarki': 2, 'deskripsi': 'Wakil pemimpin organisasi'},
        {'nama_jabatan': 'Sekretaris', 'level_hierarki': 3, 'deskripsi': 'Pengelola administrasi dan surat menyurat'},
        {'nama_jabatan': 'Bendahara', 'level_hierarki': 4, 'deskripsi': 'Pengelola keuangan organisasi'},
        {'nama_jabatan': 'Koordinator Bidang', 'level_hierarki': 5, 'deskripsi': 'Koordinator bidang tertentu'},
        {'nama_jabatan': 'Anggota', 'level_hierarki': 6, 'deskripsi': 'Anggota biasa organisasi'},
        {'nama_jabatan': 'Pengurus', 'level_hierarki': 5, 'deskripsi': 'Pengurus organisasi'},
        {'nama_jabatan': 'Humas', 'level_hierarki': 5, 'deskripsi': 'Hubungan masyarakat'},
    ]
    
    jabatan_list = []
    for data in jabatan_data:
        jabatan, created = Jabatan.objects.get_or_create(
            nama_jabatan=data['nama_jabatan'],
            defaults={
                'level_hierarki': data['level_hierarki'],
                'deskripsi': data['deskripsi']
            }
        )
        jabatan_list.append(jabatan)
        if created:
            print(f"   - Created: {jabatan.nama_jabatan}")
    
    # 3. Buat Organization
    print("3. Membuat organisasi...")
    organizations = []
    penduduk_list = list(Penduduk.objects.filter(is_active=True))
    
    if not penduduk_list:
        print("   - Tidak ada data penduduk, membuat data penduduk dummy...")
        create_penduduk_dummy()
        penduduk_list = list(Penduduk.objects.filter(is_active=True))
    
    org_names = [
        'BPD Desa Pulosarok', 'PKK Desa Pulosarok', 'Karang Taruna Muda Karya',
        'LPM Desa Pulosarok', 'RT 001 Dusun Krajan', 'RT 002 Dusun Krajan',
        'RW 001 Desa Pulosarok', 'Kelompok Tani Subur Makmur', 'Kelompok Tani Sejahtera',
        'Posyandu Melati', 'Posyandu Mawar', 'Majelis Taklim Al-Hidayah',
        'Koperasi Maju Bersama', 'Tim Penggerak PKK RT 001', 'KUB Mandiri Sejahtera'
    ]
    
    for i, name in enumerate(org_names):
        org_type = org_types[i % len(org_types)]
        leader = random.choice(penduduk_list) if penduduk_list else None
        
        org, created = Organization.objects.get_or_create(
            name=name,
            defaults={
                'organization_type': org_type,
                'description': f'Organisasi {org_type.name} di Desa Pulosarok',
                'established_date': fake.date_between(start_date='-10y', end_date='-1y'),
                'leader': leader,
                'contact_phone': fake.phone_number(),
                'contact_email': fake.email(),
                'address': fake.address(),
                'is_active': True
            }
        )
        organizations.append(org)
        if created:
            print(f"   - Created: {org.name}")
    
    # 4. Buat PeriodeKepengurusan
    print("4. Membuat periode kepengurusan...")
    periode_list = []
    for org in organizations:
        # Periode lama (sudah selesai)
        periode_lama, created = PeriodeKepengurusan.objects.get_or_create(
            organization=org,
            nama_periode='Periode 2020-2023',
            defaults={
                'tanggal_mulai': date(2020, 1, 1),
                'tanggal_selesai': date(2023, 12, 31),
                'is_active': False
            }
        )
        periode_list.append(periode_lama)
        
        # Periode aktif
        periode_aktif, created = PeriodeKepengurusan.objects.get_or_create(
            organization=org,
            nama_periode='Periode 2024-2027',
            defaults={
                'tanggal_mulai': date(2024, 1, 1),
                'tanggal_selesai': date(2027, 12, 31),
                'is_active': True
            }
        )
        periode_list.append(periode_aktif)
        
        if created:
            print(f"   - Created periode for: {org.name}")
    
    # 5. Buat AnggotaOrganisasi
    print("5. Membuat anggota organisasi...")
    anggota_count = 0
    
    for org in organizations:
        # Ambil periode aktif untuk organisasi ini
        periode_aktif = PeriodeKepengurusan.objects.filter(organization=org, is_active=True).first()
        if not periode_aktif:
            continue
            
        # Tentukan jumlah anggota berdasarkan jenis organisasi
        if 'RT' in org.name or 'RW' in org.name:
            num_members = random.randint(8, 15)
        elif 'Posyandu' in org.name:
            num_members = random.randint(5, 10)
        elif 'BPD' in org.name or 'LPM' in org.name:
            num_members = random.randint(7, 12)
        else:
            num_members = random.randint(10, 20)
        
        # Pilih anggota secara acak dari penduduk
        selected_penduduk = random.sample(penduduk_list, min(num_members, len(penduduk_list)))
        
        for i, penduduk in enumerate(selected_penduduk):
            # Tentukan jabatan berdasarkan urutan
            if i == 0:
                jabatan = jabatan_list[0]  # Ketua
            elif i == 1 and len(selected_penduduk) > 5:
                jabatan = jabatan_list[1]  # Wakil Ketua
            elif i == 2:
                jabatan = jabatan_list[2]  # Sekretaris
            elif i == 3:
                jabatan = jabatan_list[3]  # Bendahara
            elif i < 6:
                jabatan = random.choice(jabatan_list[4:6])  # Koordinator/Pengurus
            else:
                jabatan = jabatan_list[5]  # Anggota
            
            anggota, created = AnggotaOrganisasi.objects.get_or_create(
                organization=org,
                penduduk=penduduk,
                periode=periode_aktif,
                defaults={
                    'jabatan': jabatan,
                    'nomor_anggota': f"{org.id:03d}/{penduduk.id:04d}",
                    'tanggal_bergabung': fake.date_between(
                        start_date=periode_aktif.tanggal_mulai, 
                        end_date='today'
                    ),
                    'status': 'aktif',
                    'bio': f"Anggota {jabatan.nama_jabatan} di {org.name}",
                    'kontak_whatsapp': fake.phone_number(),
                    'email_pribadi': fake.email(),
                    'alamat_lengkap': penduduk.address,
                    'pendidikan_terakhir': penduduk.education or 'SMA',
                    'pekerjaan': penduduk.occupation or 'Wiraswasta',
                    'keahlian': random.choice([
                        'Kepemimpinan', 'Komunikasi', 'Organisasi', 'Administrasi',
                        'Keuangan', 'Teknologi', 'Pertanian', 'Kesehatan'
                    ])
                }
            )
            
            if created:
                anggota_count += 1
    
    print(f"   - Created {anggota_count} anggota organisasi")
    
    print("\nData dummy organisasi berhasil dibuat!")
    print(f"- {len(org_types)} kategori organisasi")
    print(f"- {len(jabatan_list)} jabatan")
    print(f"- {len(organizations)} organisasi")
    print(f"- {len(periode_list)} periode kepengurusan")
    print(f"- {anggota_count} anggota organisasi")

def create_penduduk_dummy():
    """Membuat data penduduk dummy jika belum ada"""
    from references.models import Dusun, Lorong
    
    print("Membuat data penduduk dummy...")
    
    # Buat Dusun jika belum ada
    dusun_names = ['Krajan', 'Tengah', 'Timur', 'Barat']
    dusuns = []
    for name in dusun_names:
        dusun, created = Dusun.objects.get_or_create(
            name=f"Dusun {name}",
            defaults={
                'code': name.upper()[:3],
                'description': f"Dusun {name} Desa Pulosarok"
            }
        )
        dusuns.append(dusun)
    
    # Buat Lorong jika belum ada
    lorongs = []
    for dusun in dusuns:
        for i in range(1, 4):
            lorong, created = Lorong.objects.get_or_create(
                dusun=dusun,
                code=f"L{i:02d}",
                defaults={
                    'name': f"Lorong {i}",
                    'description': f"Lorong {i} {dusun.name}"
                }
            )
            lorongs.append(lorong)
    
    # Buat data penduduk
    for i in range(50):
        nik = fake.unique.numerify('##############')
        name = fake.name()
        gender = random.choice(['L', 'P'])
        birth_date = fake.date_between(start_date='-70y', end_date='-17y')
        
        penduduk, created = Penduduk.objects.get_or_create(
            nik=nik,
            defaults={
                'name': name,
                'gender': gender,
                'birth_place': fake.city(),
                'birth_date': birth_date,
                'religion': random.choice(['Islam', 'Kristen Protestan', 'Kristen Katolik', 'Hindu', 'Buddha']),
                'education': random.choice(['SD', 'SMP', 'SMA', 'D3', 'S1', 'S2']),
                'occupation': random.choice(['Petani', 'Wiraswasta', 'PNS', 'Guru', 'Pedagang', 'Buruh']),
                'marital_status': random.choice(['BELUM_KAWIN', 'KAWIN', 'CERAI_HIDUP', 'CERAI_MATI']),
                'dusun': random.choice(dusuns),
                'lorong': random.choice(lorongs),
                'address': fake.address(),
                'is_active': True
            }
        )
        
        if created:
            print(f"   - Created penduduk: {name}")

if __name__ == '__main__':
    create_organization_dummy_data()