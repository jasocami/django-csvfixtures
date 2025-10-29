from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .forms import CSVUploadPerModelForm
from .utils import import_csv_to_model


class CSVFixtureModelAdminMixin:
    change_list_template = 'admin/csvfixture_importer/per_model_button_change_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        if request.method == 'POST' and 'csv_file' in request.FILES:
            form = CSVUploadPerModelForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']
                result = import_csv_to_model(self.model, csv_file)
                messages.success(request, _(f"Uploaded successfuly: {result['created']} created objects of {result['total_rows']} rows."))
                if result['errors']:
                    messages.warning(request, _(f"{len(result['errors'])} rows with errors."))
                extra_context['import_summary'] = result
        else:
            form = CSVUploadPerModelForm()
        extra_context['csvfixture_per_model_form'] = form
        return super().changelist_view(request, extra_context=extra_context)