# 📊 Dashboard & Data Dummy - Aplikasi References

Dokumentasi lengkap untuk fitur Dashboard dan Data Dummy pada modul References (Data Referensi) website Pulosarok.

## 🎯 Fitur yang Tersedia

### ✨ Dashboard Lengkap
- **Statistik Real-time**: Total penduduk, dusun, lorong, dan data disabilitas
- **Demografi Visual**: Distribusi gender dan kelompok usia dengan chart progress bar
- **Geografis**: Populasi per dusun dan rata-rata rumah per lorong
- **Disabilitas**: Statistik lengkap penyandang disabilitas dan tingkat bantuan
- **Distribusi Data**: Chart untuk agama, pendidikan, dan status perkawinan
- **Aktivitas Terbaru**: Tracking data baru dalam 30 hari terakhir
- **Aksi Cepat**: Link langsung ke halaman management data

### 🗃️ Data Dummy Komprehensif
- **10 Dusun** dengan nama-nama Aceh (Krueng Raya, Ujong Blang, dll)
- **8-12 Lorong per Dusun** dengan variasi nama realistis
- **10 Penduduk per Dusun** (total ~100 penduduk) dengan data lengkap
- **10 Jenis Disabilitas** sesuai standar Indonesia
- **~10% Penduduk** memiliki data disabilitas (realistis)
- **6 Agama** resmi Indonesia
- **Data Relasional** yang konsisten antar model

## 🚀 Cara Menggunakan

### Metode 1: Script Otomatis (Recommended)
```bash
# Jalankan script generator
python generate_dummy_data.py
```

### Metode 2: Management Command Django
```bash
# Buat data dummy baru (tanpa hapus existing)
python manage.py create_dummy_references

# Hapus data lama dan buat baru
python manage.py create_dummy_references --clear
```

### Metode 3: Melalui Dashboard (Coming Soon)
- Buka Dashboard References: `/admin/references/`
- Klik tombol "Generate Data Dummy"
- Ikuti petunjuk di layar

## 📱 Akses Dashboard

### URL Dashboard
```
http://localhost:8000/admin/references/
```

### Halaman Individual
- **Input Data Dusun**: `/admin/references/admin/dusun/`
- **Input Data Lorong**: `/admin/references/admin/lorong/`
- **Input Data Penduduk**: `/admin/references/admin/penduduk/`
- **Input Data Disabilitas**: `/admin/references/admin/disabilitas/`

## 📊 Detail Data Dummy

### 🏘️ Data Dusun (10 entries)
```
- Krueng Raya (DS01)      - Alue Naga (DS04)       - Leupung (DS07)
- Ujong Blang (DS02)      - Lampuuk (DS05)         - Aceh Besar (DS08)
- Paya Bakong (DS03)      - Lhoknga (DS06)         - Banda Raya (DS09)
                                                   - Syiah Kuala (DS10)
```

### 🛣️ Data Lorong (8-12 per Dusun)
```
- Lorong Mesjid           - Lorong Pemuda          - Lorong Bahagia
- Lorong Sekolah          - Lorong Merdeka         - Lorong Harmoni
- Lorong Pasar            - Lorong Damai           - Lorong Bersatu
- Lorong Kesehatan        - Lorong Makmur          - dll.
```

### 👥 Data Penduduk (10 per Dusun = ~100 total)
**Informasi Personal:**
- Nama: Mix nama Aceh/Indonesia (Muhammad Rizki, Cut Nyak Meutia, dll)
- NIK: 16 digit random
- Gender: L/P (seimbang)
- Usia: 1-80 tahun (distribusi realistis)
- Agama: Mayoritas Islam, minority lainnya

**Informasi Demografis:**
- Tempat Lahir: Banda Aceh, Aceh Besar, Pidie, dll
- Pendidikan: SD, SMP, SMA, SMK, D3, S1, S2, S3
- Pekerjaan: Petani, Nelayan, PNS, Guru, Wiraswasta, dll
- Status: Sesuai dengan usia (realistis)

### ♿ Data Disabilitas (10 jenis + ~10% populasi)
**Jenis Disabilitas:**
- Disabilitas Fisik (FIS)
- Disabilitas Netra (NET)
- Disabilitas Rungu (RUN)
- Disabilitas Wicara (WIC)
- Disabilitas Mental (MEN)
- Disabilitas Psikososial (PSI)
- Disabilitas Grahita (GRA)
- Disabilitas Ganda (GAN)
- Disabilitas Daksa (DAK)
- Autis (AUT)

**Data Disabilitas:**
- Tingkat: Ringan, Sedang, Berat
- Status Bantuan: Random
- Tanggal Diagnosis: Historis

## 🎨 Fitur Dashboard

### 📈 Kartu Statistik
- **Total Penduduk**: Dengan growth rate bulanan
- **Total Dusun**: Dengan rata-rata populasi
- **Total Lorong**: Dengan rata-rata rumah
- **Data Disabilitas**: Dengan persentase populasi

### 📊 Visualisasi Data
- **Bar Charts**: Populasi per dusun
- **Progress Bars**: Kelompok usia (Anak, Dewasa, Lansia)
- **Percentage Indicators**: Gender distribution
- **Color-coded Charts**: Jenis disabilitas, agama, pendidikan

### ⚡ Aksi Cepat
- Direct link ke form tambah penduduk
- Management pages untuk setiap data type
- Generator data dummy
- Export/Import functionality

## 🔧 Konfigurasi & Kustomisasi

### Mengubah Jumlah Data
Edit file `references/management/commands/create_dummy_references.py`:

```python
# Ubah jumlah penduduk per dusun (default: 10)
for i in range(20):  # Ganti 10 menjadi 20

# Ubah jumlah lorong per dusun (default: 8-12)
num_lorongs = random.randint(5, 15)  # Ganti range
```

### Mengubah Data Template
Customize arrays di dalam command:
- `male_names` / `female_names`: Daftar nama
- `birth_places`: Tempat lahir
- `educations`: Tingkat pendidikan
- `occupations`: Jenis pekerjaan

### API Endpoints
```
GET /admin/references/stats/           # Statistik dashboard
GET /admin/references/dashboard-summary/  # Summary enhanced
```

## 🚨 Troubleshooting

### Error: Module not found
```bash
# Pastikan dalam virtual environment
pip install -r requirements.txt
```

### Error: Database locked
```bash
# Stop development server dulu
python manage.py migrate
```

### Data tidak muncul di dashboard
```bash
# Refresh browser atau clear cache
# Check network tab untuk API errors
```

### Permission denied
```bash
# Pastikan login sebagai admin/staff
# Check user permissions
```

## 📝 Catatan Pengembangan

### Dependencies Baru
```txt
pandas==2.0.3  # Untuk export/import Excel
```

### File Baru yang Ditambahkan
```
references/management/commands/create_dummy_references.py
generate_dummy_data.py
REFERENCES_README.md
```

### API Endpoints Baru
```python
# views.py
references_stats_api()      # Dashboard statistics
dashboard_summary_api()     # Enhanced summary
```

### Template Updates
```html
templates/admin/modules/references/index.html  # Dashboard baru
```

## 🎉 Hasil Akhir

Setelah menjalankan data dummy, Anda akan memiliki:

- ✅ **Dashboard interaktif** dengan 15+ chart dan statistik
- ✅ **100+ data penduduk** realistis dengan relasi lengkap
- ✅ **10 dusun dan 80+ lorong** tersebar geografis
- ✅ **10+ data disabilitas** dengan distribusi yang masuk akal
- ✅ **Visualisasi real-time** yang responsif mobile
- ✅ **Export/Import functionality** untuk semua data
- ✅ **CRUD interface** yang user-friendly

## 📞 Support

Jika mengalami masalah:
1. Check console browser untuk JavaScript errors
2. Check Django logs untuk backend errors
3. Pastikan semua migrations sudah dijalankan
4. Verify database permissions

---

**Happy Coding! 🚀**

*Dashboard ini dibuat dengan ❤️ menggunakan Django + Tailwind CSS + Vanilla JavaScript*
