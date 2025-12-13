class CSVFixtureModelAdminMixin:
    change_list_template = 'admin/csvfixture_importer/per_model_button_change_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['model'] = f"{self.model._meta.app_label}.{self.model._meta.object_name}"
        return super().changelist_view(request, extra_context=extra_context)
