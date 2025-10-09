from io import BytesIO
from django.test import TestCase
from django.apps import apps, AppConfig
from django.db import models, connection
from csvfixture_importer.utils import import_csv_to_model


class CSVFixtureImporterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Dynamically create a temporary test app and models
        class TempAppConfig(AppConfig):
            name = "temp_app"

        apps.app_configs["temp_app"] = TempAppConfig("temp_app", "temp_app")
        apps.clear_cache()

        # Define models
        class Zone(models.Model):
            name = models.CharField(max_length=200, unique=True)
            number = models.IntegerField()

            class Meta:
                app_label = "temp_app"

        class Section(models.Model):
            name = models.CharField(max_length=200)
            number = models.IntegerField()
            zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

            class Meta:
                app_label = "temp_app"

        # Register models
        apps.register_model("temp_app", Zone)
        apps.register_model("temp_app", Section)

        cls.Zone = Zone
        cls.Section = Section

        # Create database tables for the temporary models
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Zone)
            schema_editor.create_model(Section)

    def test_import_zone_csv(self):
        csv_content = b"id,name,number\n1,North Zone,101\n2,South Zone,102\n"
        csv_file = BytesIO(csv_content)
        result = import_csv_to_model(self.Zone, csv_file)
        self.assertEqual(result['created'], 2)
        self.assertEqual(self.Zone.objects.count(), 2)
        self.assertEqual(len(result['errors']), 0)

    def test_import_section_csv_with_foreignkey(self):
        # Create zones first
        zone1 = self.Zone.objects.create(name='North Zone', number=101)
        zone2 = self.Zone.objects.create(name='South Zone', number=102)

        csv_content = f"id,name,number,zone_id\n1,Section A,1,{zone1.id}\n2,Section B,2,{zone2.id}\n".encode()
        csv_file = BytesIO(csv_content)

        result = import_csv_to_model(self.Section, csv_file)
        self.assertEqual(result['created'], 2)
        self.assertEqual(self.Section.objects.count(), 2)
        self.assertEqual(len(result['errors']), 0)

        section_a = self.Section.objects.get(name='Section A')
        self.assertEqual(section_a.zone.id, zone1.id)
