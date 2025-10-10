from django.apps import AppConfig

class CSVFixtureImporterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'csvfixture_importer'
    verbose_name = 'CSV Fixture Importer'

    def ready(self):
        from . import urls
        
        # Use a custom admin index template that includes our link
        if not hasattr(admin.site, 'original_index_template'):
            admin.site.original_index_template = admin.site.index_template

        admin.site.index_template = "admin/csvfixture_importer_index.html"
