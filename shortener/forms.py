from django import forms
from django.forms.widgets import TextInput


class ShortForm(forms.Form):
    website = forms.URLField(max_length=200, widget=TextInput, required=True)
    slug = forms.SlugField(
        label="Slug", required=False, help_text="Optional (Letters and numbers only)"
    )

    def __init__(self, *args, **kwargs):
        super(ShortForm, self).__init__(*args, **kwargs)
        self.fields["slug"].widget = TextInput(attrs={"id": "slug"})
        self.fields["website"].widget = TextInput(attrs={"id": "website"})
