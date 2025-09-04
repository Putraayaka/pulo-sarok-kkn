from django import forms
from .models import Dusun, Lorong, Penduduk, DisabilitasType, DisabilitasData, ReligionReference, Family


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
            'area_size': 'Luas Area (Hektar)',
            'population_count': 'Jumlah Penduduk',
            'description': 'Deskripsi',
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
            'dusun': 'Dusun',
            'length': 'Panjang (Meter)',
            'house_count': 'Jumlah Rumah',
            'description': 'Deskripsi',
            'is_active': 'Aktif',
        }


class PendudukForm(forms.ModelForm):
    class Meta:
        model = Penduduk
        fields = '__all__'
        exclude = ['created_by', 'updated_by']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'death_date': forms.DateInput(attrs={'type': 'date'}),
            'passport_expiry': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'height': forms.NumberInput(attrs={'min': '0', 'max': '300'}),
            'weight': forms.NumberInput(attrs={'min': '0', 'max': '500'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '08123456789'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': '08123456789'}),
            'rt_number': forms.TextInput(attrs={'maxlength': '3'}),
            'rw_number': forms.TextInput(attrs={'maxlength': '3'}),
            'postal_code': forms.TextInput(attrs={'maxlength': '5'}),
        }
        labels = {
            'nik': 'NIK',
            'name': 'Nama Lengkap',
            'gender': 'Jenis Kelamin',
            'birth_place': 'Tempat Lahir',
            'birth_date': 'Tanggal Lahir',
            'religion': 'Agama',
            'education': 'Pendidikan',
            'occupation': 'Pekerjaan',
            'marital_status': 'Status Perkawinan',
            'kk_number': 'Nomor Kartu Keluarga',
            'family_head': 'Kepala Keluarga',
            'relationship_to_head': 'Hubungan dengan Kepala Keluarga',
            'blood_type': 'Golongan Darah',
            'height': 'Tinggi Badan (cm)',
            'weight': 'Berat Badan (kg)',
            'phone_number': 'Nomor Telepon',
            'mobile_number': 'Nomor HP',
            'email': 'Email',
            'dusun': 'Dusun',
            'lorong': 'Lorong',
            'rt_number': 'Nomor RT',
            'rw_number': 'Nomor RW',
            'house_number': 'Nomor Rumah',
            'address': 'Alamat Lengkap',
            'postal_code': 'Kode Pos',
            'citizenship': 'Kewarganegaraan',
            'passport_number': 'Nomor Paspor',
            'passport_expiry': 'Berlaku Hingga',
            'emergency_contact': 'Kontak Darurat',
            'emergency_phone': 'Telepon Darurat',
            'emergency_relationship': 'Hubungan dengan Kontak Darurat',
            'is_active': 'Aktif',
            'is_alive': 'Masih Hidup',
            'death_date': 'Tanggal Meninggal',
            'death_place': 'Tempat Meninggal',
        }
        error_messages = {
            'nik': {
                'required': 'NIK wajib diisi.',
                'unique': 'NIK sudah terdaftar dalam sistem.',
                'max_length': 'NIK tidak boleh lebih dari 16 karakter.',
                'min_length': 'NIK harus 16 karakter.',
            },
            'name': {
                'required': 'Nama lengkap wajib diisi.',
                'max_length': 'Nama tidak boleh lebih dari 100 karakter.',
            },
            'gender': {
                'required': 'Jenis kelamin wajib dipilih.',
                'invalid_choice': 'Pilihan jenis kelamin tidak valid.',
            },
            'birth_place': {
                'required': 'Tempat lahir wajib diisi.',
                'max_length': 'Tempat lahir tidak boleh lebih dari 100 karakter.',
            },
            'birth_date': {
                'required': 'Tanggal lahir wajib diisi.',
                'invalid': 'Format tanggal tidak valid. Gunakan format YYYY-MM-DD.',
            },
            'religion': {
                'invalid_choice': 'Pilihan agama tidak valid.',
            },
            'marital_status': {
                'invalid_choice': 'Pilihan status perkawinan tidak valid.',
            },
            'education': {
                'invalid_choice': 'Pilihan pendidikan tidak valid.',
            },
            'blood_type': {
                'invalid_choice': 'Pilihan golongan darah tidak valid.',
            },
            'citizenship': {
                'invalid_choice': 'Pilihan kewarganegaraan tidak valid.',
            },
            'email': {
                'invalid': 'Format email tidak valid.',
            },
            'phone_number': {
                'max_length': 'Nomor telepon tidak boleh lebih dari 15 karakter.',
            },
            'mobile_number': {
                'max_length': 'Nomor HP tidak boleh lebih dari 15 karakter.',
            },
            'height': {
                'invalid': 'Tinggi badan harus berupa angka.',
                'min_value': 'Tinggi badan tidak boleh kurang dari 0.',
                'max_value': 'Tinggi badan tidak boleh lebih dari 300 cm.',
            },
            'weight': {
                'invalid': 'Berat badan harus berupa angka.',
                'min_value': 'Berat badan tidak boleh kurang dari 0.',
                'max_value': 'Berat badan tidak boleh lebih dari 500 kg.',
            },
        }
    
    def clean_nik(self):
        nik = self.cleaned_data.get('nik')
        if nik:
            # Validate NIK format (should be 16 digits)
            if not nik.isdigit():
                raise forms.ValidationError('NIK harus berupa angka.')
            if len(nik) != 16:
                raise forms.ValidationError('NIK harus terdiri dari 16 digit.')
            
            # Check for duplicate NIK
            queryset = Penduduk.objects.filter(nik=nik)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError('NIK sudah terdaftar dalam sistem.')
        return nik
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            from datetime import date
            today = date.today()
            if birth_date > today:
                raise forms.ValidationError('Tanggal lahir tidak boleh di masa depan.')
            # Check if age is reasonable (not more than 150 years)
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age > 150:
                raise forms.ValidationError('Umur tidak boleh lebih dari 150 tahun.')
        return birth_date
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove any non-digit characters for validation
            digits_only = ''.join(filter(str.isdigit, phone))
            if len(digits_only) < 10:
                raise forms.ValidationError('Nomor telepon minimal 10 digit.')
            if len(digits_only) > 15:
                raise forms.ValidationError('Nomor telepon maksimal 15 digit.')
        return phone
    
    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if mobile:
            # Remove any non-digit characters for validation
            digits_only = ''.join(filter(str.isdigit, mobile))
            if len(digits_only) < 10:
                raise forms.ValidationError('Nomor HP minimal 10 digit.')
            if len(digits_only) > 15:
                raise forms.ValidationError('Nomor HP maksimal 15 digit.')
        return mobile
    
    def clean_kk_number(self):
        kk_number = self.cleaned_data.get('kk_number')
        if kk_number:
            # Validate KK number format (should be 16 digits)
            if not kk_number.isdigit():
                raise forms.ValidationError('Nomor KK harus berupa angka.')
            if len(kk_number) != 16:
                raise forms.ValidationError('Nomor KK harus terdiri dari 16 digit.')
            
            # Check for duplicate KK number
            queryset = Penduduk.objects.filter(kk_number=kk_number)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError('Nomor KK sudah terdaftar dalam sistem.')
        return kk_number
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            from django.core.validators import validate_email
            from django.core.exceptions import ValidationError as DjangoValidationError
            try:
                validate_email(email)
            except DjangoValidationError:
                raise forms.ValidationError('Format email tidak valid.')
        return email
    
    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height is not None:
            if height < 50 or height > 250:
                raise forms.ValidationError('Tinggi badan harus antara 50-250 cm.')
        return height
    
    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None:
            if weight < 1 or weight > 300:
                raise forms.ValidationError('Berat badan harus antara 1-300 kg.')
        return weight
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Auto-grouping: if KK number is provided, handle family creation/linking
        if instance.kk_number:
            try:
                # Find existing family with same KK number
                family = Family.objects.get(kk_number=instance.kk_number)
                if family.head and not instance.family_head:
                    # If family has a head and this person doesn't have family_head set
                    instance.family_head = family.head
                elif not family.head and not instance.family_head:
                    # If family doesn't have a head, make this person the head
                    family.head = instance
                    if commit:
                        family.save()
            except Family.DoesNotExist:
                # Create new family if it doesn't exist
                if commit:
                    instance.save()  # Save instance first to get ID
                    family = Family.objects.create(
                        kk_number=instance.kk_number,
                        head=instance,
                        dusun=instance.dusun,
                        lorong=instance.lorong,
                        address=instance.address,
                        rt_number=instance.rt_number,
                        rw_number=instance.rw_number,
                        house_number=instance.house_number,
                        postal_code=instance.postal_code,
                    )
                    return instance
        
        if commit:
            instance.save()
        return instance
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make family_head choices more user-friendly
        if 'family_head' in self.fields:
            self.fields['family_head'].queryset = Penduduk.objects.filter(is_active=True).order_by('name')
            self.fields['family_head'].empty_label = "Pilih Kepala Keluarga (kosongkan jika kepala keluarga)"
        
        # Make dusun and lorong choices more user-friendly
        if 'dusun' in self.fields:
            self.fields['dusun'].queryset = Dusun.objects.filter(is_active=True).order_by('name')
        
        if 'lorong' in self.fields:
            self.fields['lorong'].queryset = Lorong.objects.filter(is_active=True).order_by('name')
            self.fields['lorong'].empty_label = "Pilih Lorong (opsional)"


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'total_income': forms.NumberInput(attrs={'step': '1000', 'min': '0'}),
            'rt_number': forms.TextInput(attrs={'maxlength': '3'}),
            'rw_number': forms.TextInput(attrs={'maxlength': '3'}),
            'postal_code': forms.TextInput(attrs={'maxlength': '5'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '08123456789'}),
        }
        labels = {
            'kk_number': 'Nomor Kartu Keluarga',
            'head': 'Kepala Keluarga',
            'family_status': 'Status Keluarga',
            'total_members': 'Jumlah Anggota',
            'total_income': 'Total Pendapatan per Bulan (Rp)',
            'address': 'Alamat Keluarga',
            'dusun': 'Dusun',
            'lorong': 'Lorong',
            'rt_number': 'Nomor RT',
            'rw_number': 'Nomor RW',
            'house_number': 'Nomor Rumah',
            'postal_code': 'Kode Pos',
            'phone_number': 'Nomor Telepon',
            'is_active': 'Aktif',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make head choices more user-friendly
        if 'head' in self.fields:
            self.fields['head'].queryset = Penduduk.objects.filter(is_active=True).order_by('name')
        
        # Make dusun and lorong choices more user-friendly
        if 'dusun' in self.fields:
            self.fields['dusun'].queryset = Dusun.objects.filter(is_active=True).order_by('name')
        
        if 'lorong' in self.fields:
            self.fields['lorong'].queryset = Lorong.objects.filter(is_active=True).order_by('name')
            self.fields['lorong'].empty_label = "Pilih Lorong (opsional)"


class DisabilitasTypeForm(forms.ModelForm):
    class Meta:
        model = DisabilitasType
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Nama Jenis Disabilitas',
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make choices more user-friendly
        if 'penduduk' in self.fields:
            self.fields['penduduk'].queryset = Penduduk.objects.filter(is_active=True).order_by('name')
        
        if 'disability_type' in self.fields:
            self.fields['disability_type'].queryset = DisabilitasType.objects.filter(is_active=True).order_by('name')


class ReligionReferenceForm(forms.ModelForm):
    class Meta:
        model = ReligionReference
        fields = '__all__'
        labels = {
            'name': 'Nama Agama',
            'code': 'Kode',
            'is_active': 'Aktif',
        }