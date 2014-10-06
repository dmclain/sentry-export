from django.utils.translation import ugettext_lazy as _
from sentry.plugins import Plugin

from sentry_export import VERSION


class ExportPlugin(Plugin):
    author = "Dave McLain"
    author_url = "https://github.com/dmclain/sentry-export"
    version = VERSION

    slug = "export"
    title = _("Export")
    conf_title = title
    conf_key = slug

    def actions(self, request, group, action_list, **kwargs):
        action_list.append((self.title, self.get_url(group)))
        return action_list

    def view(self, request, group, **kwargs):
        return self.render("sentry_export/export_form.html", {})
