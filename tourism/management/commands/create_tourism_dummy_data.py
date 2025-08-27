from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from tourism.models import (
    TourismCategory, TourismLocation, TourismGallery, 
    TourismReview, TourismRating, TourismEvent, 
    TourismPackage, TourismFAQ
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Create dummy data for tourism models'

    def handle(self, *args, **options):
        self.stdout.write('Creating tourism dummy data...')
        
        # Get or create a user for creating the data
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('Created admin user')
        
        # Create categories
        categories_data = [
            {
                'name': 'Wisata Alam',
                'description': 'Destinasi wisata yang menampilkan keindahan alam seperti gunung, pantai, dan hutan.',
                'icon': '🌲',
                'color': '#10B981'
            },
            {
                'name': 'Wisata Budaya',
                'description': 'Destinasi wisata yang menampilkan kekayaan budaya dan tradisi lokal.',
                'icon': '🏛️',
                'color': '#8B5CF6'
            },
            {
                'name': 'Wisata Sejarah',
                'description': 'Destinasi wisata yang memiliki nilai sejarah dan arkeologi.',
                'icon': '🏺',
                'color': '#F59E0B'
            },
            {
                'name': 'Wisata Petualangan',
                'description': 'Destinasi wisata yang menawarkan aktivitas petualangan dan olahraga ekstrem.',
                'icon': '🧗',
                'color': '#EF4444'
            },
            {
                'name': 'Wisata Religi',
                'description': 'Destinasi wisata yang memiliki nilai spiritual dan keagamaan.',
                'icon': '🙏',
                'color': '#3B82F6'
            },
            {
                'name': 'Wisata Kuliner',
                'description': 'Destinasi wisata yang menampilkan keunikan kuliner lokal.',
                'icon': '🍽️',
                'color': '#F97316'
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = TourismCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'is_active': True
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create 10 complete tourism locations
        locations_data = [
            {
                'title': 'Gunung Bromo',
                'category': categories[0],  # Wisata Alam
                'location_type': 'natural',
                'short_description': 'Gunung berapi aktif yang terkenal dengan pemandangan sunrise yang menakjubkan.',
                'full_description': 'Gunung Bromo adalah gunung berapi aktif yang terletak di Jawa Timur. Gunung ini terkenal dengan pemandangan sunrise yang menakjubkan dan kawah yang masih aktif. Pengunjung dapat menikmati pemandangan alam yang indah sambil belajar tentang aktivitas vulkanik.',
                'address': 'Tosari, Pasuruan, Jawa Timur',
                'latitude': -7.9425,
                'longitude': 112.9530,
                'opening_hours': '24 Jam',
                'entry_fee': 50000,
                'contact_phone': '0341-123456',
                'contact_email': 'info@bromo.com',
                'facilities': ['Parkir', 'Toilet', 'Warung Makan', 'Pemandu Wisata'],
                'activities': ['Sunrise Viewing', 'Trekking', 'Fotografi', 'Camping'],
                'featured': True
            },
            {
                'title': 'Candi Borobudur',
                'category': categories[2],  # Wisata Sejarah
                'location_type': 'historical',
                'short_description': 'Candi Buddha terbesar di dunia yang dibangun pada abad ke-9.',
                'full_description': 'Candi Borobudur adalah candi Buddha terbesar di dunia yang dibangun pada abad ke-9. Candi ini memiliki arsitektur yang megah dengan relief yang menceritakan kisah Buddha. Pengunjung dapat belajar tentang sejarah dan budaya Buddha sambil menikmati pemandangan yang indah.',
                'address': 'Magelang, Jawa Tengah',
                'latitude': -7.6079,
                'longitude': 110.2038,
                'opening_hours': '06:00 - 17:00',
                'entry_fee': 75000,
                'contact_phone': '0293-123456',
                'contact_email': 'info@borobudur.com',
                'facilities': ['Parkir', 'Toilet', 'Museum', 'Pemandu Wisata', 'Restoran'],
                'activities': ['Wisata Sejarah', 'Fotografi', 'Meditasi', 'Belajar Budaya'],
                'featured': True
            },
            {
                'title': 'Pantai Bali',
                'category': categories[0],  # Wisata Alam
                'location_type': 'natural',
                'short_description': 'Pantai dengan pasir putih dan air jernih yang cocok untuk berenang dan berselancar.',
                'full_description': 'Pantai Bali menawarkan pemandangan yang indah dengan pasir putih dan air jernih. Pantai ini cocok untuk berbagai aktivitas seperti berenang, berselancar, dan berjemur. Pengunjung juga dapat menikmati sunset yang romantis.',
                'address': 'Kuta, Bali',
                'latitude': -8.7266,
                'longitude': 115.1777,
                'opening_hours': '24 Jam',
                'entry_fee': 0,
                'contact_phone': '0361-123456',
                'contact_email': 'info@balibeach.com',
                'facilities': ['Parkir', 'Toilet', 'Warung Makan', 'Penyewaan Perlengkapan'],
                'activities': ['Berenang', 'Berselancar', 'Berjemur', 'Fotografi'],
                'featured': False
            },
            {
                'title': 'Kampung Adat',
                'category': categories[1],  # Wisata Budaya
                'location_type': 'cultural',
                'short_description': 'Kampung tradisional yang masih mempertahankan adat dan budaya lokal.',
                'full_description': 'Kampung Adat adalah kampung tradisional yang masih mempertahankan adat dan budaya lokal. Pengunjung dapat belajar tentang tradisi, melihat rumah adat, dan berinteraksi dengan masyarakat lokal. Kampung ini menawarkan pengalaman budaya yang autentik.',
                'address': 'Desa Pulosarok, Jawa Tengah',
                'latitude': -7.5000,
                'longitude': 110.0000,
                'opening_hours': '08:00 - 17:00',
                'entry_fee': 25000,
                'contact_phone': '0271-123456',
                'contact_email': 'info@kampungadat.com',
                'facilities': ['Parkir', 'Toilet', 'Pemandu Wisata', 'Warung Makan'],
                'activities': ['Wisata Budaya', 'Fotografi', 'Belajar Tradisi', 'Interaksi Lokal'],
                'featured': True
            },
            {
                'title': 'Gunung Rinjani',
                'category': categories[3],  # Wisata Petualangan
                'location_type': 'adventure',
                'short_description': 'Gunung tertinggi kedua di Indonesia yang menawarkan trekking yang menantang.',
                'full_description': 'Gunung Rinjani adalah gunung tertinggi kedua di Indonesia yang menawarkan trekking yang menantang. Gunung ini memiliki pemandangan yang spektakuler dengan danau kawah yang indah. Trekking ke puncak membutuhkan persiapan fisik yang baik.',
                'address': 'Lombok, Nusa Tenggara Barat',
                'latitude': -8.4091,
                'longitude': 116.4575,
                'opening_hours': '24 Jam',
                'entry_fee': 150000,
                'contact_phone': '0370-123456',
                'contact_email': 'info@rinjani.com',
                'facilities': ['Basecamp', 'Toilet', 'Pemandu Wisata', 'Penyewaan Perlengkapan'],
                'activities': ['Trekking', 'Camping', 'Fotografi', 'Pendakian'],
                'featured': False
            },
            {
                'title': 'Masjid Istiqlal',
                'category': categories[4],  # Wisata Religi
                'location_type': 'religious',
                'short_description': 'Masjid terbesar di Asia Tenggara dengan arsitektur yang megah.',
                'full_description': 'Masjid Istiqlal adalah masjid terbesar di Asia Tenggara yang dibangun dengan arsitektur yang megah. Masjid ini memiliki nilai sejarah dan spiritual yang tinggi. Pengunjung dapat belajar tentang arsitektur Islam dan sejarah kemerdekaan Indonesia.',
                'address': 'Jakarta Pusat, DKI Jakarta',
                'latitude': -6.1702,
                'longitude': 106.8314,
                'opening_hours': '04:00 - 22:00',
                'entry_fee': 0,
                'contact_phone': '021-123456',
                'contact_email': 'info@istiqlal.com',
                'facilities': ['Parkir', 'Toilet', 'Musholla', 'Perpustakaan', 'Kantin'],
                'activities': ['Shalat', 'Wisata Religi', 'Fotografi', 'Belajar Sejarah'],
                'featured': True
            },
            {
                'title': 'Kampung Batik',
                'category': categories[1],  # Wisata Budaya
                'location_type': 'cultural',
                'short_description': 'Kampung yang terkenal dengan kerajinan batik tradisional.',
                'full_description': 'Kampung Batik adalah kampung yang terkenal dengan kerajinan batik tradisional. Pengunjung dapat melihat proses pembuatan batik, belajar membatik, dan membeli batik asli. Kampung ini menawarkan pengalaman budaya yang mendalam.',
                'address': 'Solo, Jawa Tengah',
                'latitude': -7.5755,
                'longitude': 110.8243,
                'opening_hours': '08:00 - 17:00',
                'entry_fee': 15000,
                'contact_phone': '0271-123456',
                'contact_email': 'info@kampungbatik.com',
                'facilities': ['Workshop Batik', 'Showroom', 'Toilet', 'Warung Makan'],
                'activities': ['Belajar Membatik', 'Fotografi', 'Belanja Batik', 'Wisata Budaya'],
                'featured': False
            },
            {
                'title': 'Taman Safari',
                'category': categories[5],  # Wisata Edukasi
                'location_type': 'education',
                'short_description': 'Taman safari yang menampilkan berbagai satwa liar dalam habitat alaminya.',
                'full_description': 'Taman Safari adalah taman safari yang menampilkan berbagai satwa liar dalam habitat alaminya. Pengunjung dapat melihat satwa dari dekat, belajar tentang konservasi, dan menikmati pertunjukan satwa. Taman ini cocok untuk keluarga dan anak-anak.',
                'address': 'Cisarua, Bogor, Jawa Barat',
                'latitude': -6.7000,
                'longitude': 106.9500,
                'opening_hours': '09:00 - 17:00',
                'entry_fee': 200000,
                'contact_phone': '0251-123456',
                'contact_email': 'info@tamansafari.com',
                'facilities': ['Parkir', 'Toilet', 'Restoran', 'Toko Souvenir', 'Area Bermain'],
                'activities': ['Safari Satwa', 'Pertunjukan Satwa', 'Fotografi', 'Edukasi'],
                'featured': True
            },
            {
                'title': 'Pulau Komodo',
                'category': categories[0],  # Wisata Alam
                'location_type': 'natural',
                'short_description': 'Pulau yang terkenal dengan hewan komodo dan pemandangan alam yang indah.',
                'full_description': 'Pulau Komodo adalah pulau yang terkenal dengan hewan komodo dan pemandangan alam yang indah. Pengunjung dapat melihat komodo dari dekat, trekking, snorkeling, dan menikmati keindahan alam. Pulau ini adalah bagian dari Taman Nasional Komodo.',
                'address': 'Labuan Bajo, Nusa Tenggara Timur',
                'latitude': -8.5833,
                'longitude': 119.4500,
                'opening_hours': '06:00 - 18:00',
                'entry_fee': 100000,
                'contact_phone': '0385-123456',
                'contact_email': 'info@pulaukomodo.com',
                'facilities': ['Basecamp', 'Toilet', 'Pemandu Wisata', 'Penyewaan Perlengkapan'],
                'activities': ['Lihat Komodo', 'Trekking', 'Snorkeling', 'Fotografi'],
                'featured': True
            },
            {
                'title': 'Kampung Kuliner',
                'category': categories[5],  # Wisata Kuliner
                'location_type': 'culinary',
                'short_description': 'Kampung yang terkenal dengan berbagai kuliner tradisional dan modern.',
                'full_description': 'Kampung Kuliner adalah kampung yang terkenal dengan berbagai kuliner tradisional dan modern. Pengunjung dapat mencoba berbagai makanan lokal, belajar memasak, dan menikmati suasana yang nyaman. Kampung ini adalah surga bagi pecinta kuliner.',
                'address': 'Yogyakarta, DI Yogyakarta',
                'latitude': -7.7971,
                'longitude': 110.3708,
                'opening_hours': '10:00 - 22:00',
                'entry_fee': 0,
                'contact_phone': '0274-123456',
                'contact_email': 'info@kampungkuliner.com',
                'facilities': ['Warung Makan', 'Toilet', 'Area Parkir', 'Tempat Duduk'],
                'activities': ['Makan', 'Fotografi', 'Belajar Memasak', 'Wisata Kuliner'],
                'featured': False
            }
        ]
        
        locations = []
        for loc_data in locations_data:
            location, created = TourismLocation.objects.get_or_create(
                title=loc_data['title'],
                defaults={
                    'slug': loc_data['title'].lower().replace(' ', '-'),
                    'category': loc_data['category'],
                    'location_type': loc_data['location_type'],
                    'short_description': loc_data['short_description'],
                    'full_description': loc_data['full_description'],
                    'address': loc_data['address'],
                    'latitude': loc_data['latitude'],
                    'longitude': loc_data['longitude'],
                    'opening_hours': loc_data['opening_hours'],
                    'entry_fee': loc_data['entry_fee'],
                    'contact_phone': loc_data['contact_phone'],
                    'contact_email': loc_data['contact_email'],
                    'facilities': loc_data['facilities'],
                    'activities': loc_data['activities'],
                    'featured': loc_data['featured'],
                    'status': 'published',
                    'is_active': True,
                    'created_by': user,
                    'meta_title': loc_data['title'],
                    'meta_description': loc_data['short_description'][:160],
                    'meta_keywords': f"{loc_data['title']}, {loc_data['category'].name}, wisata, desa pulosarok"
                }
            )
            locations.append(location)
            if created:
                self.stdout.write(f'Created location: {location.title}')
        
        # Create events for each location
        event_types = ['festival', 'exhibition', 'workshop', 'competition', 'ceremony']
        for i, location in enumerate(locations):
            event_data = {
                'title': f'Event {location.title}',
                'tourism_location': location,
                'event_type': random.choice(event_types),
                'description': f'Event menarik di {location.title} yang menampilkan berbagai aktivitas dan hiburan.',
                'start_date': timezone.now() + timedelta(days=random.randint(10, 60)),
                'end_date': timezone.now() + timedelta(days=random.randint(10, 60) + 1),
                'organizer': f'Tim Event {location.title}',
                'contact_info': f'Hubungi kami di {location.contact_phone} atau {location.contact_email}',
                'registration_required': random.choice([True, False]),
                'registration_url': f'https://event-{location.slug}.com' if random.choice([True, False]) else '',
                'is_active': True,
                'is_featured': random.choice([True, False])
            }
            
            event, created = TourismEvent.objects.get_or_create(
                title=event_data['title'],
                defaults=event_data
            )
            if created:
                self.stdout.write(f'Created event: {event.title}')
        
        # Create packages for each location
        package_types = ['day_trip', 'weekend', 'week_long', 'custom']
        for i, location in enumerate(locations):
            package_data = {
                'title': f'Paket Wisata {location.title}',
                'tourism_location': location,
                'package_type': random.choice(package_types),
                'description': f'Paket wisata lengkap untuk mengeksplorasi {location.title} dengan berbagai aktivitas menarik.',
                'duration': f'{random.randint(1, 7)} hari {random.randint(0, 1)} malam',
                'price': random.randint(100000, 2000000),
                'currency': 'IDR',
                'includes': ['Transportasi', 'Akomodasi', 'Makan', 'Pemandu Wisata', 'Asuransi'],
                'excludes': ['Tiket Masuk', 'Pengeluaran Pribadi', 'Tips'],
                'itinerary': [
                    {'hari': 1, 'aktivitas': f'Kunjungan ke {location.title}'},
                    {'hari': 2, 'aktivitas': 'Aktivitas tambahan'},
                    {'hari': 3, 'aktivitas': 'Pulang'}
                ],
                'max_participants': random.randint(10, 50),
                'min_participants': random.randint(1, 5),
                'booking_deadline': random.randint(3, 14),
                'is_active': True,
                'is_featured': random.choice([True, False])
            }
            
            package, created = TourismPackage.objects.get_or_create(
                title=package_data['title'],
                defaults=package_data
            )
            if created:
                self.stdout.write(f'Created package: {package.title}')
        
        # Create FAQs for each location
        faq_questions = [
            'Apa yang harus dibawa saat berkunjung?',
            'Apakah ada pemandu wisata?',
            'Bagaimana cara memesan paket wisata?',
            'Apakah ada fasilitas akomodasi?',
            'Kapan waktu terbaik untuk berkunjung?'
        ]
        
        faq_answers = [
            'Sebaiknya membawa pakaian yang nyaman, sepatu yang sesuai, air minum, dan perlengkapan fotografi.',
            'Ya, setiap destinasi menyediakan pemandu wisata yang berpengalaman dan berlisensi.',
            'Pemesanan dapat dilakukan melalui website resmi, telepon, atau datang langsung ke kantor wisata.',
            'Ya, tersedia homestay dan guesthouse yang dikelola oleh warga lokal.',
            'Waktu terbaik adalah pada musim kemarau (April-Oktober) untuk wisata alam dan outdoor.'
        ]
        
        for i, location in enumerate(locations):
            for j in range(3):  # Create 3 FAQs per location
                faq_data = {
                    'tourism_location': location,
                    'question': faq_questions[j],
                    'answer': faq_answers[j],
                    'category': 'Umum',
                    'order': j + 1,
                    'is_active': True
                }
                
                faq, created = TourismFAQ.objects.get_or_create(
                    tourism_location=location,
                    question=faq_questions[j],
                    defaults=faq_data
                )
                if created:
                    self.stdout.write(f'Created FAQ for {location.title}')
        
        # Create some reviews and ratings
        review_texts = [
            'Tempat yang sangat indah dan menakjubkan!',
            'Pengalaman yang luar biasa, sangat direkomendasikan.',
            'Pemandu wisata sangat ramah dan informatif.',
            'Fasilitas yang tersedia sudah cukup memadai.',
            'Harga yang sangat terjangkau untuk pengalaman yang didapat.',
            'Akan kembali lagi di lain waktu.',
            'Tempat yang cocok untuk liburan keluarga.',
            'Suasana yang tenang dan nyaman.',
            'Makanan lokal yang sangat lezat.',
            'Transportasi yang mudah diakses.'
        ]
        
        for location in locations:
            # Create 3-5 reviews per location
            for i in range(random.randint(3, 5)):
                # Create a unique user for each review to avoid constraint violation
                review_user, created = User.objects.get_or_create(
                    username=f'reviewer_{location.id}_{i}',
                    defaults={
                        'email': f'reviewer_{location.id}_{i}@example.com',
                        'first_name': f'Reviewer {i+1}',
                        'last_name': f'Location {location.id}',
                        'is_staff': False,
                        'is_superuser': False
                    }
                )
                
                if created:
                    review_user.set_password('password123')
                    review_user.save()
                
                review = TourismReview.objects.create(
                    tourism_location=location,
                    user=review_user,
                    rating=random.randint(4, 5),
                    title=f'Review {location.title}',
                    comment=random.choice(review_texts),
                    visit_date=timezone.now().date() - timedelta(days=random.randint(1, 365)),
                    visit_type=random.choice(['personal', 'family', 'group', 'business']),
                    is_approved=True,
                    is_flagged=False
                )
                
                # Create rating
                TourismRating.objects.create(
                    tourism_location=location,
                    user=review_user,
                    rating=review.rating,
                    cleanliness=random.randint(4, 5),
                    accessibility=random.randint(4, 5),
                    facilities=random.randint(4, 5),
                    service=random.randint(4, 5),
                    value=random.randint(4, 5)
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created tourism dummy data!')
        )
        self.stdout.write(f'Created {len(categories)} categories')
        self.stdout.write(f'Created {len(locations)} locations')
        self.stdout.write(f'Created events for all locations')
        self.stdout.write(f'Created packages for all locations')
        self.stdout.write(f'Created FAQs for all locations')
        self.stdout.write('Created reviews and ratings for all locations')
