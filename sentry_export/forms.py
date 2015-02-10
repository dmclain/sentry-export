import logging
from django import forms

log = logging.getLogger(__name__)

DEFAULT_CHOICES = (
    ('event_id', 'Event ID'),
    ('message', 'Message'),
    ('datetime', 'Event Time'),
    ('platform', 'Platform'),
)

USER_CHOICES = (
    ('sentry.interfaces.User:email', 'Email'),
    ('sentry.interfaces.User:id', 'ID'),
    ('sentry.interfaces.User:username', 'Username'),
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


class UserFieldForm(forms.Form):
    field = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=USER_CHOICES,
        label="User Fields",
        )


class RawFieldTemplateForm(forms.Form):
    field = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'span6'}),
        label="Raw Selector Field"
    )


def get_tag_form(tags):
    choices = [('tags:%s' % tag.key, tag.get_label()) for tag in tags]
    class TagFieldForm(forms.Form):
        field = forms.ChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=choices,
        label="Tags",
        initial=('event_id', 'datetime'),
        )
    return TagFieldForm()
