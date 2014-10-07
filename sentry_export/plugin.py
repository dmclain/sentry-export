import csv
from cStringIO import StringIO

from django.utils.translation import ugettext_lazy as _
from sentry.plugins import Plugin
from django.http import HttpResponse
from sentry.plugins.base import Response

from sentry_export import VERSION
from sentry_export.forms import ExportGroupForm


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
                return self.render_events(form, group)
        context = {
            'title': self.title,
            'form': form,
        }
        return self.render("sentry_export/export_form.html", context)

    def render_events(self, form, group):
        return CSVResponse(form, group.event_set.all())

    def get_form(self, request, group):
        return ExportGroupForm()


class CSVResponse(Response):
    def __init__(self, form, events):
        self.form = form
        self.events = events

    def respond(self, *args, **kwargs):
        f = StringIO()
        writer = csv.DictWriter(f, self.form.get_fields())
        writer.writeheader()
        writer.writerows(self.form.get_values(evt) for evt in self.events)
        return HttpResponse(f.getvalue(), mimetype="application/csv")
