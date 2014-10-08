
def safe_get(k, evt):
    val = getattr(evt, k, None)
    if val:
        return val
    keys = k.split(':')
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


class ValueExtractor(object):
    def __init__(self, fields):
        self.fields = fields

    def get_fields(self):
        return self.fields

    def get_values_dict(self, event):
        return dict((f, safe_get(f, event)) for f in self.get_fields())
