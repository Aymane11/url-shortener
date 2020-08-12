from django import forms
from .models import ShortURL
from django.forms.widgets import TextInput
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class ShortForm(forms.Form):
    website = forms.URLField(max_length=200, widget=TextInput, required=True)
    slug = forms.SlugField(label='Slug', required=False, help_text="Optional")

    def __init__(self, *args, **kwargs):
        super(ShortForm, self).__init__(*args, **kwargs)
        self.fields['slug'].widget = TextInput(attrs={'id': 'slug'})
        self.fields['website'].widget = TextInput(attrs={'id': 'website'})