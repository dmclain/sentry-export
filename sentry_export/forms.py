import logging
from django import forms

log = logging.getLogger(__name__)


class ExportGroupForm(forms.Form):
    field = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'span6'}),
    )

