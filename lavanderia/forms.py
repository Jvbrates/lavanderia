from django import forms
from lavanderia.models import Washer


class WasherForm(forms.ModelForm):
    class Meta:
        model = Washer
        fields = ['name']
