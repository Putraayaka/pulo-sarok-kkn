from django import forms
from django.core.exceptions import ValidationError
from .models import (
    OrganizationType, Organization, OrganizationMember, OrganizationEvent, 
    OrganizationDocument, Jabatan, PeriodeKepengurusan, AnggotaOrganisasi,
    GaleriKegiatan, StrukturOrganisasi
)


class OrganizationTypeForm(forms.ModelForm):
    class Meta:
        model = OrganizationType
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        widgets = {
            'established_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class OrganizationMemberForm(forms.ModelForm):
    class Meta:
        model = OrganizationMember
        fields = '__all__'
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class OrganizationEventForm(forms.ModelForm):
    class Meta:
        model = OrganizationEvent
        fields = '__all__'
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class OrganizationDocumentForm(forms.ModelForm):
    class Meta:
        model = OrganizationDocument
        fields = '__all__'
        widgets = {
            'document_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class JabatanForm(forms.ModelForm):
    """Form untuk input jabatan organisasi"""
    class Meta:
        model = Jabatan
        fields = '__all__'
        widgets = {
            'nama_jabatan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama jabatan'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deskripsi jabatan (opsional)'
            }),
            'level_hierarki': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
            'warna_badge': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean_nama_jabatan(self):
        nama = self.cleaned_data.get('nama_jabatan')
        if nama:
            nama = nama.strip().title()
        return nama


class PeriodeKepengurusan(forms.ModelForm):
    """Form untuk periode kepengurusan"""
    class Meta:
        model = PeriodeKepengurusan
        fields = '__all__'
        widgets = {
            'nama_periode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Periode 2024-2026'
            }),
            'tanggal_mulai': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tanggal_selesai': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deskripsi periode (opsional)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        tanggal_mulai = cleaned_data.get('tanggal_mulai')
        tanggal_selesai = cleaned_data.get('tanggal_selesai')
        
        if tanggal_mulai and tanggal_selesai:
            if tanggal_selesai <= tanggal_mulai:
                raise ValidationError('Tanggal selesai harus setelah tanggal mulai')
        
        return cleaned_data


class AnggotaOrganisasiForm(forms.ModelForm):
    """Form untuk anggota organisasi dengan foto profil"""
    class Meta:
        model = AnggotaOrganisasi
        fields = '__all__'
        widgets = {
            'nomor_anggota': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nomor anggota (opsional)'
            }),
            'tanggal_bergabung': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tanggal_keluar': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Biografi singkat anggota'
            }),
            'kontak_whatsapp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '08xxxxxxxxxx'
            }),
            'email_pribadi': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'alamat_lengkap': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Alamat lengkap'
            }),
            'pendidikan_terakhir': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: S1 Teknik Informatika'
            }),
            'pekerjaan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pekerjaan saat ini'
            }),
            'keahlian': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Keahlian yang dimiliki'
            }),
            'prestasi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Prestasi yang pernah diraih'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'foto_profil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_foto_profil(self):
        foto = self.cleaned_data.get('foto_profil')
        if foto:
            if foto.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('Ukuran foto tidak boleh lebih dari 5MB')
            
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            if not any(foto.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError('Format foto harus JPG, JPEG, PNG, atau GIF')
        
        return foto

    def clean_kontak_whatsapp(self):
        whatsapp = self.cleaned_data.get('kontak_whatsapp')
        if whatsapp:
            # Remove non-numeric characters
            whatsapp = ''.join(filter(str.isdigit, whatsapp))
            if len(whatsapp) < 10 or len(whatsapp) > 15:
                raise ValidationError('Nomor WhatsApp tidak valid')
        return whatsapp


class GaleriKegiatanForm(forms.ModelForm):
    """Form untuk galeri kegiatan organisasi"""
    class Meta:
        model = GaleriKegiatan
        fields = '__all__'
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Judul kegiatan'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deskripsi kegiatan'
            }),
            'tanggal_kegiatan': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'lokasi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lokasi kegiatan'
            }),
            'fotografer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama fotografer (opsional)'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tag1, Tag2, Tag3 (pisahkan dengan koma)'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto:
            if foto.size > 10 * 1024 * 1024:  # 10MB
                raise ValidationError('Ukuran foto tidak boleh lebih dari 10MB')
            
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            if not any(foto.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError('Format foto harus JPG, JPEG, PNG, atau GIF')
        
        return foto


class StrukturOrganisasiForm(forms.ModelForm):
    """Form untuk struktur organisasi"""
    class Meta:
        model = StrukturOrganisasi
        fields = '__all__'
        widgets = {
            'posisi_x': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'posisi_y': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'urutan': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'is_visible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


# Form untuk pencarian dan filter
class OrganizationSearchForm(forms.Form):
    """Form untuk pencarian organisasi"""
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cari organisasi...',
            'id': 'search-input'
        })
    )
    
    organization_type = forms.ModelChoiceField(
        queryset=OrganizationType.objects.filter(is_active=True),
        required=False,
        empty_label='Semua Jenis',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    is_active = forms.ChoiceField(
        choices=[('', 'Semua Status'), ('true', 'Aktif'), ('false', 'Non-Aktif')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class AnggotaSearchForm(forms.Form):
    """Form untuk pencarian anggota"""
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cari nama anggota...',
            'id': 'search-input'
        })
    )
    
    jabatan = forms.ModelChoiceField(
        queryset=Jabatan.objects.filter(is_active=True),
        required=False,
        empty_label='Semua Jabatan',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'Semua Status')] + AnggotaOrganisasi._meta.get_field('status').choices,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )