import logging
from django import forms

log = logging.getLogger(__name__)

DEFAULT_CHOICES = (
    ('event_id', 'Event ID'),
    ('message', 'Message'),
    ('datetime', 'Event Time'),
    ('platform', 'Platform'),
)


class ExportGroupForm(forms.Form):
    export_all = forms.BooleanField(required=False, initial=True)
    count = forms.IntegerField(required=False)

    def get_count(self):
        if self.cleaned_data['export_all']:
            return None
        return self.cleaned_data['count']


class DefaultFieldForm(forms.Form):
    field = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=DEFAULT_CHOICES,
        label="Event Fields",
        initial=('event_id', 'datetime'),
        )


class RawFieldTemplateForm(forms.Form):
    field = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'span6'}),
        label="Raw Selector Field"
    )

def get_tag_template_form(tags):
    choices = [('tags:%s' % tag, tag) for tag in tags]
    class TagTemplateForm(forms.Form):
        field = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=choices,
        label="Tags",
        initial=('event_id', 'datetime'),
        )
    return TagTemplateForm()
