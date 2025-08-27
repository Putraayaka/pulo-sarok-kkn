from django import forms
from .models import Dusun, Lorong, Penduduk, DisabilitasType, DisabilitasData, ReligionReference


class DusunForm(forms.ModelForm):
    class Meta:
        model = Dusun
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'area_size': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'name': 'Nama Dusun',
            'code': 'Kode Dusun',
            'description': 'Deskripsi',
            'area_size': 'Luas Area (Hektar)',
            'population_count': 'Jumlah Penduduk',
            'is_active': 'Aktif',
        }


class LorongForm(forms.ModelForm):
    class Meta:
        model = Lorong
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'length': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'name': 'Nama Lorong',
            'code': 'Kode Lorong',
            'description': 'Deskripsi',
            'dusun': 'Dusun',
            'length': 'Panjang (Meter)',
            'house_count': 'Jumlah Rumah',
            'is_active': 'Aktif',
        }


class PendudukForm(forms.ModelForm):
    class Meta:
        model = Penduduk
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'nik': 'NIK',
            'name': 'Nama',
            'gender': 'Jenis Kelamin',
            'birth_place': 'Tempat Lahir',
            'birth_date': 'Tanggal Lahir',
            'religion': 'Agama',
            'education': 'Pendidikan',
            'occupation': 'Pekerjaan',
            'marital_status': 'Status Perkawinan',
            'dusun': 'Dusun',
            'lorong': 'Lorong',
            'address': 'Alamat',
            'is_active': 'Aktif',
        }


class DisabilitasTypeForm(forms.ModelForm):
    class Meta:
        model = DisabilitasType
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Nama Jenis',
            'code': 'Kode',
            'description': 'Deskripsi',
            'is_active': 'Aktif',
        }


class DisabilitasDataForm(forms.ModelForm):
    class Meta:
        model = DisabilitasData
        fields = '__all__'
        widgets = {
            'diagnosis_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'penduduk': 'Penduduk',
            'disability_type': 'Jenis Disabilitas',
            'severity': 'Tingkat Keparahan',
            'description': 'Deskripsi',
            'diagnosis_date': 'Tanggal Diagnosis',
            'needs_assistance': 'Memerlukan Bantuan',
            'is_active': 'Aktif',
        }


class ReligionReferenceForm(forms.ModelForm):
    class Meta:
        model = ReligionReference
        fields = '__all__'
        labels = {
            'name': 'Nama Agama',
            'code': 'Kode',
            'is_active': 'Aktif',
        }