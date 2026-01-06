from django.db import transaction
from django.db.models.fields.related import ForeignKey

from .utils import iter_csv_rows, field_value_from_string


def get_csv_preview(file_obj, encoding='utf-8'):
    total = 0
    preview = []
    for rownum, row in enumerate(iter_csv_rows(file_obj, encoding=encoding), start=0):
        if total > 10:
            break
        preview.append(row)
        total += 1
    return preview


@transaction.atomic
def import_csv_to_model(model, file_obj, encoding='utf-8'):
    created, errors, total = 0, [], 0
    fields_by_name = {f.name: f for f in model._meta.get_fields() if hasattr(f, 'name')}
    for rownum, row in enumerate(iter_csv_rows(file_obj, encoding=encoding), start=1):
        total += 1
        try:
            obj_kwargs, m2m_values = {}, {}
            for col, raw in row.items():
                col = col.strip()
                if col == '':
                    continue
                if col not in fields_by_name:
                    continue
                field = fields_by_name[col]
                if isinstance(field, ForeignKey):
                    obj_kwargs[col + '_id'] = raw or None
                    continue
                if getattr(field, 'many_to_many', False):
                    m2m_values[col] = [v.strip() for v in raw.split(';') if v.strip()] if raw else []
                    continue
                obj_kwargs[col] = field_value_from_string(field, raw)
            obj = model(**obj_kwargs)
            obj.full_clean()
            obj.save()
            for fieldname, pks in m2m_values.items():
                getattr(obj, fieldname).set(pks)
            created += 1
        except Exception as exc:
            errors.append((rownum, str(exc)))
    return { 'created': created, 'errors': errors, 'total_rows': total }
