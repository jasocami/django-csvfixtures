MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:


# django_csvfixtures

Django 5 library to import CSV files as fixtures from the `/admin` panel or directly from each model list page.
Designed to be **plug-and-play**, **installable via pip**, and ready for publication on **GitHub / PyPI**.


## ✅ Summary

This app (`csvfixture_importer`) provides:

* Automatic detection of all models in the project (`django.apps.apps.get_models()`).
* Central admin panel at `/admin/csv-fixtures/` with a model selector and CSV upload input.
* `CSVFixtureModelAdminMixin` to add an **“Upload fixture”** button in each model changelist view.
* CSV importer that creates objects (header = model field name).
* Support for basic field types (`CharField`, `IntegerField`, `BooleanField`, `DateField`, `DecimalField`, etc.) and `ForeignKey` (by PK).
* Upload summary with created objects, error count, and total rows.


## 🔧 Installation (via pip / PyPI)

Once published to PyPI or installed from GitHub:

```bash
pip install django-csvfixtures
```

Add it to your `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.admin',
    'csvfixture_importer',
]
```

Then open `/admin/csv-fixtures/` or use the “Upload fixture” button from any model.

---

## 📝 Example CSV Upload

Here is an example of how to create 2 objects for two models: `Zone` and `Section`.

### CSV for `Zone`:

```csv
id,name,number
1,North Zone,101
2,South Zone,102
```

### CSV for `Section`:

```csv
id,name,number,zone_id
1,Section A,1,1
2,Section B,2,2
```

**Notes:**

* Upload `Zone.csv` first, then `Section.csv` (so the foreign key exists).
* The `zone_id` field in `Section` corresponds to the `id` of the `Zone` objects.
* Fields in the CSV must exactly match the model field names.

This example can be used directly in the admin panel or via the **Upload fixture** button in each model’s changelist.

---

This keeps the library fully **plug-and-play**, **admin-integrated**, and **ready for production use** without requiring the user to manually include any URLs or modify their Django configuration.
