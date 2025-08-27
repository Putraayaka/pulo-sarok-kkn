from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import VillageVision, VillageHistory, VillageMap, VillageGeography, GoogleMapsEmblem


class VillageVisionForm(forms.ModelForm):
    """Form untuk Visi Misi Desa"""
    
    class Meta:
        model = VillageVision
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Masukkan judul visi misi...'
            }),
            'vision_text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 5,
                'placeholder': 'Tuliskan visi desa...'
            }),
            'mission_text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 8,
                'placeholder': 'Tuliskan misi desa...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Deskripsi tambahan (opsional)...'
            }),
            'effective_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'date'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
            })
        }
        labels = {
            'title': 'Judul Visi Misi',
            'vision_text': 'Visi Desa',
            'mission_text': 'Misi Desa',
            'description': 'Deskripsi Tambahan',
            'effective_date': 'Tanggal Berlaku',
            'is_active': 'Aktif'
        }
    
    def clean_effective_date(self):
        effective_date = self.cleaned_data.get('effective_date')
        if effective_date and effective_date > timezone.now().date():
            raise ValidationError("Tanggal berlaku tidak boleh di masa depan.")
        return effective_date
    
    def clean_vision_text(self):
        vision_text = self.cleaned_data.get('vision_text')
        if len(vision_text) < 20:
            raise ValidationError("Visi desa harus minimal 20 karakter.")
        return vision_text
    
    def clean_mission_text(self):
        mission_text = self.cleaned_data.get('mission_text')
        if len(mission_text) < 50:
            raise ValidationError("Misi desa harus minimal 50 karakter.")
        return mission_text


class VillageHistoryForm(forms.ModelForm):
    """Form untuk Sejarah Desa"""
    
    class Meta:
        model = VillageHistory
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Judul sejarah...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 10,
                'placeholder': 'Ceritakan sejarah desa...'
            }),
            'period_start': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Contoh: 1945, Abad ke-19, dll.'
            }),
            'period_end': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Contoh: 1965, Sekarang, dll.'
            }),
            'historical_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 bg-gray-100 border-gray-300 rounded focus:ring-green-500'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 bg-gray-100 border-gray-300 rounded focus:ring-green-500'
            })
        }
        labels = {
            'title': 'Judul Sejarah',
            'content': 'Isi Sejarah',
            'period_start': 'Periode Awal',
            'period_end': 'Periode Akhir',
            'historical_image': 'Gambar Sejarah',
            'is_featured': 'Sejarah Unggulan',
            'is_active': 'Aktif'
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 100:
            raise ValidationError("Isi sejarah harus minimal 100 karakter.")
        return content
    
    def clean_historical_image(self):
        image = self.cleaned_data.get('historical_image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError("Ukuran gambar tidak boleh lebih dari 5MB.")
            if not image.content_type.startswith('image/'):
                raise ValidationError("File harus berupa gambar.")
        return image


class VillageMapForm(forms.ModelForm):
    """Form untuk Peta Desa"""
    
    class Meta:
        model = VillageMap
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Nama peta...'
            }),
            'map_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'rows': 4,
                'placeholder': 'Deskripsi peta...'
            }),
            'map_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'map_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'accept': '.pdf,.kml,.kmz'
            }),
            'coordinates_center_lat': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'step': 'any',
                'placeholder': 'Contoh: -7.250445'
            }),
            'coordinates_center_lng': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'step': 'any',
                'placeholder': 'Contoh: 112.768845'
            }),
            'zoom_level': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'min': 1,
                'max': 20
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-purple-600 bg-gray-100 border-gray-300 rounded focus:ring-purple-500'
            })
        }
        labels = {
            'title': 'Judul Peta',
            'map_type': 'Jenis Peta',
            'description': 'Deskripsi',
            'map_image': 'Gambar Peta',
            'map_file': 'File Peta (PDF/KML)',
            'coordinates_center_lat': 'Latitude Pusat',
            'coordinates_center_lng': 'Longitude Pusat',
            'zoom_level': 'Level Zoom',
            'is_active': 'Aktif'
        }
    
    def clean_coordinates_center_lat(self):
        lat = self.cleaned_data.get('coordinates_center_lat')
        if lat and (lat < -90 or lat > 90):
            raise ValidationError("Latitude harus antara -90 dan 90.")
        return lat
    
    def clean_coordinates_center_lng(self):
        lng = self.cleaned_data.get('coordinates_center_lng')
        if lng and (lng < -180 or lng > 180):
            raise ValidationError("Longitude harus antara -180 dan 180.")
        return lng
    
    def clean_zoom_level(self):
        zoom = self.cleaned_data.get('zoom_level')
        if zoom and (zoom < 1 or zoom > 20):
            raise ValidationError("Level zoom harus antara 1 dan 20.")
        return zoom


class VillageGeographyForm(forms.ModelForm):
    """Form untuk Geografi Desa"""
    
    class Meta:
        model = VillageGeography
        fields = '__all__'
        widgets = {
            'total_area': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'step': '0.01',
                'placeholder': 'Luas total (hektar)'
            }),
            'agricultural_area': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'step': '0.01',
                'placeholder': 'Luas pertanian (hektar)'
            }),
            'residential_area': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'step': '0.01',
                'placeholder': 'Luas pemukiman (hektar)'
            }),
            'forest_area': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'step': '0.01',
                'placeholder': 'Luas hutan (hektar)'
            }),
            'water_area': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'step': '0.01',
                'placeholder': 'Luas perairan (hektar)'
            }),
            'altitude_min': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'placeholder': 'Ketinggian minimum (mdpl)'
            }),
            'altitude_max': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'placeholder': 'Ketinggian maksimum (mdpl)'
            }),
            'climate_type': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'placeholder': 'Contoh: Tropis, Subtropis'
            }),
            'rainfall_average': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'step': '0.01',
                'placeholder': 'Curah hujan rata-rata (mm/tahun)'
            }),
            'temperature_min': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'step': '0.1',
                'placeholder': 'Suhu minimum (°C)'
            }),
            'temperature_max': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'step': '0.1',
                'placeholder': 'Suhu maksimum (°C)'
            }),
            'boundaries_north': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'placeholder': 'Batas sebelah utara'
            }),
            'boundaries_south': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'placeholder': 'Batas sebelah selatan'
            }),
            'boundaries_east': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'placeholder': 'Batas sebelah timur'
            }),
            'boundaries_west': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent',
                'placeholder': 'Batas sebelah barat'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-yellow-600 bg-gray-100 border-gray-300 rounded focus:ring-yellow-500'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        total_area = cleaned_data.get('total_area')
        agricultural_area = cleaned_data.get('agricultural_area') or 0
        residential_area = cleaned_data.get('residential_area') or 0
        forest_area = cleaned_data.get('forest_area') or 0
        water_area = cleaned_data.get('water_area') or 0
        
        if total_area:
            sum_areas = agricultural_area + residential_area + forest_area + water_area
            if sum_areas > total_area:
                raise ValidationError("Total luas area tidak boleh melebihi luas total desa.")
        
        altitude_min = cleaned_data.get('altitude_min')
        altitude_max = cleaned_data.get('altitude_max')
        if altitude_min and altitude_max and altitude_min >= altitude_max:
            raise ValidationError("Ketinggian minimum harus lebih kecil dari ketinggian maksimum.")
        
        temp_min = cleaned_data.get('temperature_min')
        temp_max = cleaned_data.get('temperature_max')
        if temp_min and temp_max and temp_min >= temp_max:
            raise ValidationError("Suhu minimum harus lebih kecil dari suhu maksimum.")
        
        return cleaned_data


class GoogleMapsEmblemForm(forms.ModelForm):
    """Form untuk Google Maps Emblem"""
    
    class Meta:
        model = GoogleMapsEmblem
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'placeholder': 'Judul emblem...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'rows': 3,
                'placeholder': 'Deskripsi emblem...'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'step': 'any',
                'placeholder': 'Contoh: -7.250445'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'step': 'any',
                'placeholder': 'Contoh: 112.768845'
            }),
            'zoom_level': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent',
                'min': 1,
                'max': 20
            }),
            'emblem_size': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-red-600 bg-gray-100 border-gray-300 rounded focus:ring-red-500'
            }),
            'is_visible': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-red-600 bg-gray-100 border-gray-300 rounded focus:ring-red-500'
            })
        }
        labels = {
            'title': 'Judul Emblem',
            'description': 'Deskripsi',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'zoom_level': 'Level Zoom',
            'emblem_size': 'Ukuran Emblem',
            'is_active': 'Aktif',
            'is_visible': 'Tampilkan di Peta'
        }
    
    def clean_latitude(self):
        lat = self.cleaned_data.get('latitude')
        if lat < -90 or lat > 90:
            raise ValidationError("Latitude harus antara -90 dan 90.")
        return lat
    
    def clean_longitude(self):
        lng = self.cleaned_data.get('longitude')
        if lng < -180 or lng > 180:
            raise ValidationError("Longitude harus antara -180 dan 180.")
        return lng


# Form untuk pencarian dan filter
class VillageProfileSearchForm(forms.Form):
    """Form untuk pencarian data profil desa"""
    
    SEARCH_CHOICES = [
        ('all', 'Semua Data'),
        ('vision', 'Visi Misi'),
        ('history', 'Sejarah'),
        ('maps', 'Peta'),
        ('geography', 'Geografi'),
        ('emblem', 'Emblem')
    ]
    
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Cari data profil desa...'
        })
    )
    
    search_type = forms.ChoiceField(
        choices=SEARCH_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    is_active_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
        }),
        label='Hanya data aktif'
    )