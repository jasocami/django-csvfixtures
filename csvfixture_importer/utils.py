import csv
from io import TextIOWrapper

from django.apps import apps


def get_model_from_label(label):
    app_label, model_name = label.split('.')
    return apps.get_model(app_label, model_name)


def iter_csv_rows(file_obj, encoding='utf-8'):
    text = TextIOWrapper(file_obj.file, encoding=encoding, newline='')
    reader = csv.DictReader(text)
    for row in reader:
        yield row


def field_value_from_string(field, raw_value):
    # field: django model field, raw_value: string
    if raw_value in (None, ''):
        return None
    try:
        return field.to_python(raw_value)
    except Exception:
        return raw_value
