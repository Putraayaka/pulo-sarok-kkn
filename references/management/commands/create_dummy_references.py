from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import date, timedelta
import random
from references.models import (
    Dusun, Lorong, Penduduk, DisabilitasType, DisabilitasData, ReligionReference
)


class Command(BaseCommand):
    help = 'Create dummy data for references app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            DisabilitasData.objects.all().delete()
            Penduduk.objects.all().delete()
            Lorong.objects.all().delete()
            Dusun.objects.all().delete()
            DisabilitasType.objects.all().delete()
            ReligionReference.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        try:
            with transaction.atomic():
                # Create religion references
                self.create_religion_references()
                
                # Create disability types
                self.create_disability_types()
                
                # Create dusun data
                dusuns = self.create_dusun_data()
                
                # Create lorong data
                lorongs = self.create_lorong_data(dusuns)
                
                # Create penduduk data
                penduduks = self.create_penduduk_data(dusuns, lorongs)
                
                # Create disability data
                self.create_disability_data(penduduks)
                
                self.stdout.write(self.style.SUCCESS('Successfully created dummy data for references app'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating dummy data: {str(e)}'))

    def create_religion_references(self):
        """Create religion reference data"""
        religions = [
            {'name': 'Islam', 'code': 'ISL'},
            {'name': 'Kristen Protestan', 'code': 'PRO'},
            {'name': 'Kristen Katolik', 'code': 'KAT'},
            {'name': 'Hindu', 'code': 'HIN'},
            {'name': 'Buddha', 'code': 'BUD'},
            {'name': 'Konghucu', 'code': 'KON'},
        ]
        
        for religion_data in religions:
            ReligionReference.objects.get_or_create(
                code=religion_data['code'],
                defaults=religion_data
            )
        
        self.stdout.write('Created religion references')

    def create_disability_types(self):
        """Create disability type data"""
        disability_types = [
            {'name': 'Disabilitas Fisik', 'code': 'FIS', 'description': 'Gangguan pada fungsi gerak tubuh'},
            {'name': 'Disabilitas Netra', 'code': 'NET', 'description': 'Gangguan penglihatan atau kebutaan'},
            {'name': 'Disabilitas Rungu', 'code': 'RUN', 'description': 'Gangguan pendengaran atau ketulian'},
            {'name': 'Disabilitas Wicara', 'code': 'WIC', 'description': 'Gangguan bicara atau komunikasi'},
            {'name': 'Disabilitas Mental', 'code': 'MEN', 'description': 'Gangguan fungsi pikir karena tingkat kecerdasan di bawah rata-rata'},
            {'name': 'Disabilitas Psikososial', 'code': 'PSI', 'description': 'Gangguan fungsi pikir, emosi, perilaku'},
            {'name': 'Disabilitas Grahita', 'code': 'GRA', 'description': 'Retardasi mental atau disabilitas intelektual'},
            {'name': 'Disabilitas Ganda', 'code': 'GAN', 'description': 'Kombinasi dua atau lebih jenis disabilitas'},
            {'name': 'Disabilitas Daksa', 'code': 'DAK', 'description': 'Kelainan atau cacat pada tulang, otot, dan sendi'},
            {'name': 'Autis', 'code': 'AUT', 'description': 'Gangguan perkembangan yang mempengaruhi komunikasi dan interaksi sosial'},
        ]
        
        for disability_data in disability_types:
            DisabilitasType.objects.get_or_create(
                code=disability_data['code'],
                defaults=disability_data
            )
        
        self.stdout.write('Created disability types')

    def create_dusun_data(self):
        """Create 10 dusun data"""
        dusun_names = [
            'Krueng Raya', 'Ujong Blang', 'Paya Bakong', 'Alue Naga',
            'Lampuuk', 'Lhoknga', 'Leupung', 'Aceh Besar',
            'Banda Raya', 'Syiah Kuala'
        ]
        
        dusuns = []
        for i, name in enumerate(dusun_names, 1):
            dusun = Dusun.objects.create(
                name=name,
                code=f'DS{i:02d}',
                description=f'Deskripsi untuk dusun {name}',
                area_size=round(random.uniform(5.0, 25.0), 2),
                population_count=random.randint(150, 500),
                is_active=True
            )
            dusuns.append(dusun)
        
        self.stdout.write(f'Created {len(dusuns)} dusun records')
        return dusuns

    def create_lorong_data(self, dusuns):
        """Create lorong data for each dusun"""
        lorong_names = [
            'Lorong Mesjid', 'Lorong Sekolah', 'Lorong Pasar', 'Lorong Kesehatan',
            'Lorong Pemuda', 'Lorong Merdeka', 'Lorong Damai', 'Lorong Makmur',
            'Lorong Sejahtera', 'Lorong Bahagia', 'Lorong Harmoni', 'Lorong Bersatu'
        ]
        
        lorongs = []
        for dusun in dusuns:
            # Create 8-12 lorongs per dusun
            num_lorongs = random.randint(8, 12)
            selected_names = random.sample(lorong_names, min(num_lorongs, len(lorong_names)))
            
            for i, name in enumerate(selected_names, 1):
                lorong = Lorong.objects.create(
                    dusun=dusun,
                    name=name,
                    code=f'{dusun.code}L{i:02d}',
                    description=f'Deskripsi untuk {name} di {dusun.name}',
                    length=round(random.uniform(100.0, 800.0), 2),
                    house_count=random.randint(10, 40),
                    is_active=True
                )
                lorongs.append(lorong)
        
        self.stdout.write(f'Created {len(lorongs)} lorong records')
        return lorongs

    def create_penduduk_data(self, dusuns, lorongs):
        """Create penduduk data"""
        # Common Indonesian names
        male_names = [
            'Muhammad Rizki', 'Ahmad Fadli', 'Zulkifli Hassan', 'Teuku Rahman',
            'Cut Nyak Dien', 'Iskandar Muda', 'Sultan Hasanuddin', 'Hamzah Fansuri',
            'Abdullah Said', 'Ibrahim Hasan', 'Yusuf Ali', 'Omar Dhani',
            'Hafiz Anwar', 'Ridwan Kamil', 'Fajar Nugroho', 'Andi Wijaya'
        ]
        
        female_names = [
            'Siti Aisyah', 'Cut Nyak Meutia', 'Kartini Sari', 'Dewi Sartika',
            'Ratu Kalinyamat', 'Putri Lindungan', 'Tjoet Nja Dhien', 'Halimah Said',
            'Fatimah Zahra', 'Khadijah Nur', 'Mariam Sari', 'Aminah Hasan',
            'Aisyah Putri', 'Rahmawati', 'Nurul Hidayah', 'Sari Dewi'
        ]
        
        birth_places = [
            'Banda Aceh', 'Aceh Besar', 'Pidie', 'Lhokseumawe', 'Langsa',
            'Sabang', 'Subulussalam', 'Medan', 'Jakarta', 'Padang'
        ]
        
        educations = [
            'SD', 'SMP', 'SMA', 'SMK', 'D3', 'S1', 'S2', 'S3', 'Tidak Sekolah'
        ]
        
        occupations = [
            'Petani', 'Nelayan', 'Pedagang', 'PNS', 'TNI/POLRI', 'Guru',
            'Dokter', 'Perawat', 'Tukang', 'Sopir', 'Buruh', 'Wiraswasta',
            'Ibu Rumah Tangga', 'Mahasiswa', 'Pensiunan'
        ]
        
        religions = ['Islam', 'Kristen Protestan', 'Kristen Katolik', 'Hindu', 'Buddha']
        
        penduduks = []
        
        # Create 15 penduduk per dusun (150 total for 10 dusuns)
        for dusun in dusuns:
            dusun_lorongs = [l for l in lorongs if l.dusun == dusun]
            
            for i in range(15):
                # Generate random birth date (age between 1-80 years)
                age = random.randint(1, 80)
                birth_date = date.today() - timedelta(days=age*365 + random.randint(0, 365))
                
                # Choose gender and corresponding name
                gender = random.choice(['L', 'P'])
                if gender == 'L':
                    name = random.choice(male_names)
                else:
                    name = random.choice(female_names)
                
                # Generate NIK (16 digits)
                nik = f"{random.randint(1100000000000000, 1199999999999999)}"
                
                # Select random lorong from this dusun
                lorong = random.choice(dusun_lorongs) if dusun_lorongs else None
                
                # Determine marital status based on age
                if age < 17:
                    marital_status = 'BELUM_KAWIN'
                else:
                    marital_status = random.choice(['BELUM_KAWIN', 'KAWIN', 'CERAI_HIDUP', 'CERAI_MATI'])
                
                penduduk = Penduduk.objects.create(
                    nik=nik,
                    name=name,
                    gender=gender,
                    birth_place=random.choice(birth_places),
                    birth_date=birth_date,
                    religion=random.choice(religions),
                    education=random.choice(educations),
                    occupation=random.choice(occupations),
                    marital_status=marital_status,
                    dusun=dusun,
                    lorong=lorong,
                    address=f'Jalan {random.choice(["Merdeka", "Sudirman", "Diponegoro", "Gajah Mada"])} No. {random.randint(1, 100)}, {dusun.name}',
                    is_active=True
                )
                penduduks.append(penduduk)
        
        self.stdout.write(f'Created {len(penduduks)} penduduk records')
        return penduduks

    def create_disability_data(self, penduduks):
        """Create disability data for some residents"""
        disability_types = list(DisabilitasType.objects.all())
        
        # Create disability data for about 25% of population (minimum 30 records)
        disabled_count = max(30, int(len(penduduks) * 0.25))
        disabled_residents = random.sample(penduduks, min(disabled_count, len(penduduks)))
        
        disability_data_list = []
        
        for penduduk in disabled_residents:
            # Each disabled resident can have 1-2 disability types
            num_disabilities = random.randint(1, 2)
            selected_disabilities = random.sample(disability_types, min(num_disabilities, len(disability_types)))
            
            for disability_type in selected_disabilities:
                # Generate diagnosis date (some time in the past)
                diagnosis_date = penduduk.birth_date + timedelta(days=random.randint(365, (date.today() - penduduk.birth_date).days))
                
                disability_data = DisabilitasData.objects.create(
                    penduduk=penduduk,
                    disability_type=disability_type,
                    severity=random.choice(['RINGAN', 'SEDANG', 'BERAT']),
                    description=f'Diagnosis {disability_type.name} untuk {penduduk.name}',
                    diagnosis_date=diagnosis_date,
                    needs_assistance=random.choice([True, False]),
                    is_active=True
                )
                disability_data_list.append(disability_data)
        
        self.stdout.write(f'Created {len(disability_data_list)} disability data records')
        return disability_data_list
