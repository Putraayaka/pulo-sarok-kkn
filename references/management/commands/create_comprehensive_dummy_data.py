from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
import random
from references.models import Dusun, Lorong, Penduduk, Family, DisabilitasType, ReligionReference

User = get_user_model()


class Command(BaseCommand):
    help = 'Create comprehensive dummy data for references app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of penduduk to create (default: 50)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        self.stdout.write('Creating comprehensive dummy data...')
        
        # Create admin user if not exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Created admin user')
        
        # Create Dusun
        dusun_names = ['Dusun Krajan', 'Dusun Ngemplak', 'Dusun Karanganyar', 'Dusun Sidomulyo', 'Dusun Wonosari']
        dusuns = []
        for i, name in enumerate(dusun_names):
            dusun, created = Dusun.objects.get_or_create(
                name=name,
                defaults={
                    'code': f'D{i+1:02d}',
                    'description': f'Deskripsi {name}',
                    'area_size': random.uniform(50.0, 200.0),
                    'population_count': random.randint(100, 500)
                }
            )
            dusuns.append(dusun)
            if created:
                self.stdout.write(f'Created dusun: {name}')
        
        # Create Lorong for each Dusun
        lorongs = []
        for dusun in dusuns:
            for j in range(random.randint(3, 6)):
                lorong_name = f'Lorong {chr(65+j)}'
                lorong, created = Lorong.objects.get_or_create(
                    name=lorong_name,
                    dusun=dusun,
                    defaults={
                        'code': f'{dusun.code}L{j+1:02d}',
                        'description': f'Deskripsi {lorong_name} di {dusun.name}',
                        'length': random.uniform(100.0, 500.0),
                        'house_count': random.randint(20, 80)
                    }
                )
                lorongs.append(lorong)
                if created:
                    self.stdout.write(f'Created lorong: {lorong_name} in {dusun.name}')
        
        # Create Religion References
        religions = ['Islam', 'Kristen Protestan', 'Kristen Katolik', 'Hindu', 'Buddha', 'Konghucu']
        for religion in religions:
            ReligionReference.objects.get_or_create(
                name=religion,
                defaults={'code': religion[:3].upper()}
            )
        
        # Create Disabilitas Types with unique codes
        disabilitas_types = [
            ('Tunanetra', 'TUN'),
            ('Tunarungu', 'TUR'),
            ('Tunawicara', 'TUW'),
            ('Tunadaksa', 'TUD'),
            ('Tunagrahita', 'TUG'),
            ('Tunalaras', 'TUL')
        ]
        for disabilitas, code in disabilitas_types:
            DisabilitasType.objects.get_or_create(
                name=disabilitas,
                defaults={'code': code}
            )
        
        # Create Penduduk
        first_names = ['Ahmad', 'Siti', 'Budi', 'Dewi', 'Joko', 'Sri', 'Rudi', 'Nina', 'Agus', 'Maya']
        last_names = ['Santoso', 'Rahayu', 'Wijaya', 'Kusuma', 'Purnama', 'Hidayat', 'Nugraha', 'Putri']
        
        penduduks = []
        for i in range(count):
            # Generate random data
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"
            
            # Generate NIK (16 digits)
            nik = f"35{random.randint(10, 99)}{random.randint(1, 12):02d}{random.randint(1, 28):02d}{random.randint(1000, 9999)}"
            
            # Generate birth date (18-80 years old)
            years_ago = random.randint(18, 80)
            birth_date = date.today() - timedelta(days=years_ago * 365 + random.randint(0, 365))
            
            # Generate KK number (16 digits)
            kk_number = f"35{random.randint(10, 99)}{random.randint(1, 12):02d}{random.randint(1, 28):02d}{random.randint(10000, 99999)}"
            
            # Random choices
            gender = random.choice(['L', 'P'])
            religion = random.choice(religions)
            education = random.choice(['TIDAK_BELUM_SEKOLAH', 'BELUM_TAMAT_SD', 'TAMAT_SD', 'SLTP', 'SLTA', 'D1', 'D2', 'D3', 'D4_S1', 'S2', 'S3'])
            marital_status = random.choice(['BELUM_KAWIN', 'KAWIN', 'CERAI_HIDUP', 'CERAI_MATI'])
            blood_type = random.choice(['A', 'B', 'AB', 'O'])
            citizenship = random.choice(['WNI', 'WNA'])
            
            # Random physical data
            height = random.randint(150, 190) if random.random() > 0.3 else None
            weight = random.randint(40, 100) if random.random() > 0.3 else None
            
            # Random contact data
            phone_number = f"08{random.randint(100000000, 999999999)}" if random.random() > 0.4 else None
            mobile_number = f"08{random.randint(100000000, 999999999)}" if random.random() > 0.3 else None
            email = f"{first_name.lower()}.{last_name.lower()}@example.com" if random.random() > 0.5 else None
            
            # Random address data
            dusun = random.choice(dusuns)
            lorong = random.choice(lorongs) if random.random() > 0.3 else None
            rt_number = f"{random.randint(1, 20):02d}" if random.random() > 0.2 else None
            rw_number = f"{random.randint(1, 10):02d}" if random.random() > 0.2 else None
            house_number = f"{random.randint(1, 999)}" if random.random() > 0.2 else None
            postal_code = f"{random.randint(10000, 99999)}" if random.random() > 0.3 else None
            
            # Create Penduduk
            penduduk = Penduduk.objects.create(
                nik=nik,
                name=full_name,
                gender=gender,
                birth_place=f"Kota {random.choice(['Surabaya', 'Malang', 'Sidoarjo', 'Gresik', 'Mojokerto'])}",
                birth_date=birth_date,
                kk_number=kk_number,
                religion=religion,
                education=education,
                occupation=random.choice(['Petani', 'Pedagang', 'PNS', 'Swasta', 'Wiraswasta', 'Pelajar/Mahasiswa', 'Ibu Rumah Tangga']),
                marital_status=marital_status,
                blood_type=blood_type,
                height=height,
                weight=weight,
                phone_number=phone_number,
                mobile_number=mobile_number,
                email=email,
                dusun=dusun,
                lorong=lorong,
                rt_number=rt_number,
                rw_number=rw_number,
                house_number=house_number,
                address=f"Jl. {random.choice(['Mawar', 'Melati', 'Anggrek', 'Tulip', 'Matahari'])} No. {random.randint(1, 100)}",
                postal_code=postal_code,
                citizenship=citizenship,
                emergency_contact=f"Kontak {random.choice(['Suami', 'Istri', 'Anak', 'Orang Tua', 'Saudara'])}",
                emergency_phone=f"08{random.randint(100000000, 999999999)}" if random.random() > 0.4 else None,
                emergency_relationship=random.choice(['Suami', 'Istri', 'Anak', 'Orang Tua', 'Saudara']),
                is_active=True,
                is_alive=True,
                created_by=admin_user,
                updated_by=admin_user
            )
            
            penduduks.append(penduduk)
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'Created {i + 1} penduduk...')
        
        # Create Families
        family_count = count // 4  # Create families for about 1/4 of penduduk
        for i in range(family_count):
            if i < len(penduduks):
                head = penduduks[i]
                
                # Update penduduk to be family head
                head.family_head = None
                head.relationship_to_head = 'Kepala Keluarga'
                head.save()
                
                # Create family
                family = Family.objects.create(
                    kk_number=head.kk_number,
                    head=head,
                    family_status=random.choice(['NORMAL', 'MISKIN', 'PRASEJAHTERA', 'SEJAHTERA', 'SEJAHTERA_1', 'SEJAHTERA_2', 'SEJAHTERA_3']),
                    total_members=random.randint(1, 6),
                    total_income=random.randint(1000000, 10000000) if random.random() > 0.3 else None,
                    address=head.address,
                    dusun=head.dusun,
                    lorong=head.lorong,
                    rt_number=head.rt_number,
                    rw_number=head.rw_number,
                    house_number=head.house_number,
                    postal_code=head.postal_code,
                    phone_number=head.phone_number or head.mobile_number
                )
                
                # Add some family members
                member_count = min(family.total_members - 1, len(penduduks) - i - 1)
                for j in range(member_count):
                    if i + j + 1 < len(penduduks):
                        member = penduduks[i + j + 1]
                        member.family_head = head
                        member.relationship_to_head = random.choice(['Suami', 'Istri', 'Anak', 'Orang Tua', 'Saudara'])
                        member.save()
                
                if (i + 1) % 5 == 0:
                    self.stdout.write(f'Created {i + 1} families...')
        
        # Update population counts
        for dusun in dusuns:
            dusun.population_count = dusun.residents.count()
            dusun.save()
        
        # Update house counts
        for lorong in lorongs:
            lorong.house_count = lorong.residents.count()
            lorong.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created comprehensive dummy data:\n'
                f'- {len(dusuns)} Dusun\n'
                f'- {len(lorongs)} Lorong\n'
                f'- {len(penduduks)} Penduduk\n'
                f'- {family_count} Families\n'
                f'- Religion references\n'
                f'- Disabilitas types'
            )
        )
