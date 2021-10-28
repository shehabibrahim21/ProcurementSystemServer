import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class SearchForm(forms.Form):
    name = forms.CharField(label = False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_name','class':'autocomplete_name'})
    )
