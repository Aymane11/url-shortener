from django import forms
from django.core.validators import RegexValidator
from django.forms.widgets import TextInput

validate_slug = RegexValidator(
    regex=r"^[a-zA-Z0-9]+$",
    message="Invalid Slug (Letters and numbers only)",
    code="invalid_slug",
)


class ShortForm(forms.Form):
    website = forms.URLField(max_length=200, widget=TextInput, required=True)
    slug = forms.CharField(
        label="Slug",
        required=False,
        help_text="Optional (Letters and numbers only)",
        validators=[validate_slug],
    )

    def __init__(self, *args, **kwargs):
        super(ShortForm, self).__init__(*args, **kwargs)
        self.fields["slug"].widget = TextInput(attrs={"id": "slug"})
        self.fields["website"].widget = TextInput(attrs={"id": "website"})
