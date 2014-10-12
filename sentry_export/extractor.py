from itertools import izip

def safe_get(field):
    keys = field.split(':')
    def _safe_get(evt):
        if len(keys) == 1:
            val = getattr(evt, field, None)
            if val:
                return val
        val = evt.data
        for k in keys:
            try:
                val = val[k]
            except:
                try:
                    val = val[int(k)]
                except:
                    val = None
        return val
    return _safe_get


def tag_get(field):
    _, key = field.split(':', 1)
    def _tag_get(evt):
        if not hasattr(evt, 'tag_dict'):
            tags = evt.data['tags']
            evt.tag_dict = dict(tags)
        return evt.tag_dict.get(key)
    return _tag_get


class ValueExtractor(object):
    def __init__(self, fields):
        self.fields = fields
        self.extractors = [self.get_extractor(field) for field in fields]

    def get_fields(self):
        return self.fields

    def get_extractor(self, field):
        if field.startswith('tags:'):
            return tag_get(field)
        return safe_get(field)

    def get_values_dict(self, event):
        return dict(izip(self.fields, self.get_values(event)))

    def get_values(self, event):
        return [extractor(event) for extractor in self.extractors]
