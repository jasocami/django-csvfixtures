from django.urls import path
from django.contrib import admin
from .admin import admin_panel_view


def register_admin_urls():
    csv_fixture_url = path(
        'csv-fixtures/',
        admin.site.admin_view(admin_panel_view),
        name='csv-fixtures'
    )

    original_get_urls = admin.site.get_urls

    def get_urls():
        return [csv_fixture_url] + original_get_urls()

    admin.site.get_urls = get_urls


register_admin_urls()