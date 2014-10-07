import logging
from django import forms

log = logging.getLogger(__name__)


def safe_get(k, evt):
    val = getattr(evt, k)
    if val:
        return val
    keys = k.split('.')
    val = evt.data
    for k in keys:
        try:
            val = val.get(k, {})
        except AttributeError:
            val = None
    return val


class ExportGroupForm(forms.Form):
    event_id = forms.BooleanField(required=False)
    datetime = forms.BooleanField(required=False)
    message = forms.BooleanField(required=False)

    def get_fields(self):
        fields = []
        for k in ('event_id', 'datetime', 'message'):
            if self.cleaned_data[k]:
                fields.append(k)
        return fields

    def get_values(self, event):
        return dict((f, safe_get(f, event)) for f in self.get_fields())
