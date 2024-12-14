# Copyright (C) 2024 - Scalizer (<https://www.scalizer.fr>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from .record import OdooRecord

class OdooRecordSet(set):
    _odoo = None
    _model = None

    def __init__(self, seq=(), model=None):
        super().__init__(seq)
        if model:
            self._model = model
            self._odoo = self._model._odoo

    def __getattr__(self, name):
        if name == 'ids':
            return self.get_ids()
        else:
            return self.super().__getattr__(name)

    def save(self, batch_size=100, skip_line=0, ignore_fields=[]):
        values_list = [r.get_update_values() for r in self]
        res = self._model.load_batch(values_list, batch_size=batch_size, skip_line=skip_line, ignore_fields=ignore_fields)
        for i, r in enumerate(self):
            r._updated_values = {}
            if not r.id:
                r.id = res.get('ids')[i]
        return True

    def get_ids(self):
        return [r.id for r in self]

    def unlink(self):
        ids = self.ids
        self._model.unlink(ids)
        for key in ids:
            self._model._cache.pop(key, None)
        self.clear()
