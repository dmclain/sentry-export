import logging
from django import forms

log = logging.getLogger(__name__)


class ExportGroupForm(forms.Form):
    export_all = forms.BooleanField(required=False, initial=True)
    count = forms.IntegerField(required=False)

    def get_count(self):
        if self.cleaned_data['export_all']:
            return None
        return self.cleaned_data['count']


class FieldTemplateForm(forms.Form):
    field = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'span6'}),
    )

def get_tag_template_form_class(tags):
    choices = [('tags:%s' % tag, tag) for tag in tags]
    class TagTemplateForm(forms.Form):
        field = forms.ChoiceField(choices=choices)
    return TagTemplateForm
