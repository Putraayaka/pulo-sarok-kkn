from django import forms
from .models import BusinessCategory, Business, BusinessOwner, BusinessProduct, BusinessFinance


class BusinessCategoryForm(forms.ModelForm):
    class Meta:
        model = BusinessCategory
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = '__all__'
        widgets = {
            'established_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class BusinessOwnerForm(forms.ModelForm):
    class Meta:
        model = BusinessOwner
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class BusinessProductForm(forms.ModelForm):
    class Meta:
        model = BusinessProduct
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class BusinessFinanceForm(forms.ModelForm):
    class Meta:
        model = BusinessFinance
        fields = '__all__'
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }