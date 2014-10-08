import csv
from cStringIO import StringIO
import json

from django.utils.translation import ugettext_lazy as _
from sentry.plugins import Plugin
from django.http import HttpResponse
from sentry.plugins.base import Response

from sentry_export import VERSION
from sentry_export.forms import ExportGroupForm
from sentry_export.extractor import ValueExtractor


class ExportPlugin(Plugin):
    author = "Dave McLain"
    author_url = "https://github.com/dmclain/sentry-export"
    version = VERSION

    slug = "export"
    title = _("Export Event Data")
    conf_title = title
    conf_key = slug

    def actions(self, request, group, action_list, **kwargs):
        action_list.append((self.title, self.get_url(group)))
        return action_list

    def view(self, request, group, **kwargs):
        if request.method == 'GET':
            form = ExportGroupForm()
        else:
            form = ExportGroupForm(request.POST)
            if form.is_valid():
                fields = request.POST.getlist('field')
                return self.render_events(form, fields, group)
        context = {
            'title': self.title,
            'form': form,
            'sample': json.dumps(group.event_set.all()[0].data.keys(), sort_keys=True, indent=2)
        }
        return self.render("sentry_export/export_form.html", context)

    def render_events(self, form, fields, group):
        return CSVResponse(form, fields, group.event_set.all())

    def get_form(self, request, group):
        return ExportGroupForm()


class CSVResponse(Response):
    def __init__(self, form, fields, events):
        self.form = form
        self.fields = fields
        self.events = events

    def respond(self, *args, **kwargs):
        extractor = ValueExtractor(self.fields)
        f = StringIO()
        writer = csv.DictWriter(f, self.fields)
        writer.writeheader()
        writer.writerows(extractor.get_values_dict(evt) for evt in self.events)
        return HttpResponse(f.getvalue(), mimetype="application/csv")
