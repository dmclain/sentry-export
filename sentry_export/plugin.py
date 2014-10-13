import csv
from cStringIO import StringIO
import json
from datetime import datetime

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from sentry.plugins import Plugin
from sentry.plugins.base import Response

from sentry_export import VERSION
from sentry_export.forms import (ExportGroupForm, RawFieldTemplateForm,
    get_tag_form, DefaultFieldForm, UserFieldForm)
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
            fields = request.POST.getlist('field')
            if request.POST.get('preview'):
                return self.render_events(fields, group, count=3)
            else:
                form = ExportGroupForm(request.POST)
                if form.is_valid():
                    return self.render_events(fields, group, count=form.get_count())
        tags = group.get_tags()
        sample = group.event_set.all()[0].data
        forms = [
            form,
            DefaultFieldForm(),
        ]
        if tags:
            forms.append(get_tag_form(tags))
        if "sentry.interfaces.User" in sample:
            forms.append(UserFieldForm())
        paths = generate_keys(sample)
        context = {
            'title': self.title,
            'forms': forms,
            'raw_template_form': RawFieldTemplateForm(),
            'sample': json.dumps(paths, sort_keys=True, indent=2)
        }
        return self.render("sentry_export/export_form.html", context)

    def render_events(self, fields, group, count=None):
        events = group.event_set.all()
        if count is not None:
            events = events[:count]
        name = "sentry-%i-%s" % (group.id, datetime.now().replace(microsecond=0).isoformat('-'))
        return CSVResponse(fields, events, name=name)

    def get_form(self, request, group):
        return ExportGroupForm()


class CSVResponse(Response):
    def __init__(self, fields, events, name="sentry"):
        self.name = name
        self.fields = fields
        self.events = events

    def respond(self, *args, **kwargs):
        extractor = ValueExtractor(self.fields)
        f = StringIO()
        writer = csv.DictWriter(f, self.fields)
        writer.writeheader()
        writer.writerows(extractor.get_values_dict(evt) for evt in self.events)
        response = HttpResponse(f.getvalue(), mimetype="text/csv")
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % self.name
        return response


def generate_keys(sample, prefix=""):
    result = []
    for key, value in sample.iteritems():
        if isinstance(value, dict):
            result.extend(generate_keys(value, prefix=prefix + str(key) + ":"))
        else:
            result.append(prefix + str(key) + ' - ' + str(value.__class__))
    return result
