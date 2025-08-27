# 🏖️ Aplikasi Tourism - Wisata Desa Pulosarok

Aplikasi Django untuk mengelola dan mempromosikan destinasi wisata Desa Pulosarok dengan fitur lengkap dan responsif mobile.

## ✨ Fitur Utama

### 🗺️ Manajemen Lokasi Wisata
- **CRUD Lokasi Wisata**: Tambah, edit, hapus, dan lihat detail lokasi wisata
- **Kategori Wisata**: Pengelompokan wisata berdasarkan jenis dan tema
- **Galeri Media**: Upload foto, video, dan foto 360° untuk setiap lokasi
- **Informasi Detail**: Alamat, jam buka, biaya masuk, kontak, dan koordinat GPS
- **Status Publikasi**: Draft, Published, dan Archived

### 📸 Galeri & Media
- **Multi-format Media**: Gambar, video, dan foto 360°
- **Upload File**: Support berbagai format gambar dan video
- **URL Video**: Integrasi dengan YouTube, Vimeo, dan platform video lainnya
- **Caption & Alt Text**: SEO-friendly dan aksesibilitas

### 💬 Review & Rating System
- **User Reviews**: Pengguna dapat memberikan review dan rating
- **Rating Categories**: Kebersihan, aksesibilitas, fasilitas, pelayanan, dan nilai
- **Moderation**: Admin dapat menyetujui atau menolak review
- **Visit Information**: Tanggal kunjungan dan jenis kunjungan

### 📅 Event Wisata
- **Event Management**: Kelola event wisata dengan detail lengkap
- **Event Types**: Festival, pameran, workshop, kompetisi, upacara
- **Registration**: Sistem pendaftaran event dengan URL kustom
- **Calendar View**: Tampilan kalender untuk event mendatang

### 🎒 Paket Wisata
- **Package Types**: Perjalanan sehari, weekend, seminggu, dan kustom
- **Pricing**: Harga dalam berbagai mata uang
- **Itinerary**: Detail perjalanan dan aktivitas
- **Booking Info**: Maksimal peserta dan deadline booking

### ❓ FAQ System
- **Question Categories**: Pengelompokan pertanyaan berdasarkan tema
- **Ordering**: Urutan tampilan yang dapat dikustomisasi
- **Search**: Pencarian cepat pertanyaan dan jawaban

### 🔍 Advanced Search & Filter
- **Text Search**: Pencarian berdasarkan nama, deskripsi, dan alamat
- **Category Filter**: Filter berdasarkan kategori wisata
- **Type Filter**: Filter berdasarkan jenis wisata
- **Rating Filter**: Filter berdasarkan rating
- **Location Filter**: Filter berdasarkan lokasi geografis

### 📱 Responsive Design
- **Mobile First**: Desain yang dioptimalkan untuk perangkat mobile
- **Tailwind CSS**: Framework CSS modern untuk styling yang konsisten
- **Interactive Elements**: Modal, dropdown, dan komponen interaktif
- **Touch Friendly**: Interface yang mudah digunakan di perangkat touch

## 🏗️ Arsitektur Sistem

### Models
- `TourismCategory`: Kategori wisata
- `TourismLocation`: Lokasi wisata utama
- `TourismGallery`: Galeri media untuk setiap lokasi
- `TourismReview`: Review dan komentar pengguna
- `TourismRating`: Rating detail untuk berbagai aspek
- `TourismEvent`: Event wisata
- `TourismPackage`: Paket wisata
- `TourismFAQ`: Pertanyaan yang sering diajukan

### Views
- **Public Views**: Dashboard, list wisata, detail wisata, search
- **Admin Views**: CRUD operations, dashboard admin, moderation
- **API Views**: REST API endpoints untuk integrasi mobile app

### Forms
- **TourismLocationForm**: Form lengkap untuk lokasi wisata
- **TourismGalleryForm**: Form untuk upload media
- **TourismReviewForm**: Form untuk review dan rating
- **TourismEventForm**: Form untuk event wisata
- **TourismPackageForm**: Form untuk paket wisata

## 🚀 Instalasi & Setup

### 1. Requirements
```bash
Django >= 4.0
Pillow >= 9.0  # Untuk image processing
```

### 2. Tambahkan ke INSTALLED_APPS
```python
INSTALLED_APPS = [
    # ... other apps
    'tourism',
]
```

### 3. Tambahkan URLs
```python
urlpatterns = [
    # ... other urls
    path('pulosarok/tourism/', include('tourism.urls')),
]
```

### 4. Migrations
```bash
python manage.py makemigrations tourism
python manage.py migrate
```

### 5. Static Files
```bash
python manage.py collectstatic
```

## 📁 Struktur Direktori

```
tourism/
├── admin.py              # Admin interface
├── apps.py               # App configuration
├── forms.py              # Form definitions
├── models.py             # Database models
├── urls.py               # URL patterns
├── views.py              # View functions
├── templates/
│   └── tourism/
│       ├── dashboard.html           # Dashboard utama
│       ├── location_list.html       # List lokasi wisata
│       ├── location_detail.html     # Detail lokasi wisata
│       └── admin/
│           ├── dashboard.html       # Dashboard admin
│           ├── location_list.html   # Admin list
│           ├── location_form.html   # Form create/edit
│           └── location_confirm_delete.html  # Konfirmasi delete
└── README.md             # Dokumentasi ini
```

## 🎯 Penggunaan

### Untuk Admin
1. **Dashboard**: Akses `/pulosarok/tourism/admin/` untuk dashboard admin
2. **Tambah Wisata**: Gunakan form lengkap untuk input data wisata
3. **Kelola Media**: Upload dan atur galeri foto/video
4. **Moderasi Review**: Setujui atau tolak review pengguna
5. **Event Management**: Kelola event wisata

### Untuk Pengguna
1. **Browse Wisata**: Lihat daftar semua lokasi wisata
2. **Search & Filter**: Cari wisata berdasarkan preferensi
3. **Detail Wisata**: Lihat informasi lengkap dan galeri
4. **Review & Rating**: Berikan feedback dan rating
5. **Event Info**: Lihat event wisata yang akan datang

## 🔧 Konfigurasi

### Settings Tambahan
```python
# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

### Environment Variables
```bash
# Optional: Google Maps API Key
GOOGLE_MAPS_API_KEY=your_api_key_here

# Optional: YouTube API Key
YOUTUBE_API_KEY=your_api_key_here
```

## 📱 Mobile Optimization

### Responsive Breakpoints
- **Mobile**: < 768px (default)
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Touch Interactions
- **Swipe**: Navigasi galeri foto
- **Tap**: Buka modal dan detail
- **Pinch**: Zoom gambar (jika diimplementasikan)

### Performance
- **Lazy Loading**: Gambar dimuat saat diperlukan
- **Image Optimization**: Compress dan resize gambar otomatis
- **Caching**: Cache untuk data yang sering diakses

## 🔒 Security Features

### User Authentication
- **Login Required**: Admin views memerlukan login
- **Permission System**: Role-based access control
- **CSRF Protection**: Cross-site request forgery protection

### Data Validation
- **Form Validation**: Validasi input di sisi server
- **File Upload Security**: Validasi tipe dan ukuran file
- **SQL Injection Protection**: Django ORM protection

### Content Moderation
- **Review Approval**: Review harus disetujui admin
- **Spam Protection**: Filter konten spam
- **User Reporting**: Sistem pelaporan konten tidak pantas

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure database production
- [ ] Set up static/media file serving
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Configure security headers

### Performance Optimization
- **Database Indexing**: Index untuk field yang sering dicari
- **Caching**: Redis/Memcached untuk data caching
- **CDN**: Content Delivery Network untuk media files
- **Compression**: Gzip compression untuk response

## 🧪 Testing

### Unit Tests
```bash
python manage.py test tourism
```

### Test Coverage
```bash
coverage run --source='.' manage.py test tourism
coverage report
```

## 📊 Monitoring & Analytics

### Built-in Analytics
- **User Engagement**: View count, review count
- **Popular Content**: Wisata paling banyak dilihat
- **User Behavior**: Rating patterns, review sentiment

### Integration Options
- **Google Analytics**: Track user behavior
- **Facebook Pixel**: Social media tracking
- **Custom Analytics**: Custom tracking implementation

## 🔄 API Endpoints

### Public API
- `GET /api/locations/` - List semua lokasi wisata
- `GET /api/location/{id}/` - Detail lokasi wisata
- `POST /api/review/` - Submit review (require auth)

### Admin API
- `POST /api/admin/location/` - Create lokasi wisata
- `PUT /api/admin/location/{id}/` - Update lokasi wisata
- `DELETE /api/admin/location/{id}/` - Delete lokasi wisata

## 🤝 Contributing

### Development Setup
1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

### Code Style
- **Python**: PEP 8 compliance
- **HTML**: Semantic HTML5
- **CSS**: Tailwind CSS classes
- **JavaScript**: ES6+ with modern syntax

## 📝 Changelog

### Version 1.0.0
- Initial release
- Basic CRUD operations
- Gallery system
- Review & rating system
- Event management
- Package management
- FAQ system
- Search & filter
- Responsive design

## 📞 Support

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

### Issues
- Report bugs via GitHub Issues
- Feature requests welcome
- Pull requests appreciated

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Dibuat dengan ❤️ untuk Desa Pulosarok**
