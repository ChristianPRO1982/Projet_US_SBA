from django import forms
from .models import ModelApi


class ModelApiForm(forms.ModelForm):
    class Meta:
        model = ModelApi
        fields = "__all__"
