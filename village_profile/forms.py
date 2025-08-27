from django import forms
from .models import VillageVision, VillageHistory, VillageMap, VillageGeography


class VillageVisionForm(forms.ModelForm):
    class Meta:
        model = VillageVision
        fields = '__all__'
        widgets = {
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
            'vision_text': forms.Textarea(attrs={'rows': 4}),
            'mission_text': forms.Textarea(attrs={'rows': 4}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class VillageHistoryForm(forms.ModelForm):
    class Meta:
        model = VillageHistory
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }


class VillageMapForm(forms.ModelForm):
    class Meta:
        model = VillageMap
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class VillageGeographyForm(forms.ModelForm):
    class Meta:
        model = VillageGeography
        fields = '__all__'