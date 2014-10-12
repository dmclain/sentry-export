import logging
from django import forms

log = logging.getLogger(__name__)


class ExportGroupForm(forms.Form):
    export_all = forms.BooleanField(required=False)
    count = forms.IntegerField(required=False)

    def get_count(self):
        if self.cleaned_data['export_all']:
            return None
        return self.cleaned_data['count']


class FieldTemplateForm(forms.Form):
    field = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'span6'}),
    )
