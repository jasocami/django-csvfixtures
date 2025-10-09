from django.apps import AppConfig

class CSVFixtureImporterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'csvfixture_importer'
    verbose_name = 'CSV Fixture Importer'