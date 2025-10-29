from django.apps import apps
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .forms import CSVUploadForm
from .utils import import_csv_to_model


def _get_model_from_label(label):
    app_label, model_name = label.split('.')
    return apps.get_model(app_label, model_name)


@staff_member_required
def admin_panel_view(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if form.data.get('pending_confirm', None) == 'pending':
                ...
            model_label = form.cleaned_data['model']
            csv_file = form.cleaned_data['csv_file']
            model = _get_model_from_label(model_label)
            result = import_csv_to_model(model, csv_file)
            messages.success(request, _(f"Uploaded successfuly: {result['created']} created objects of {result['total_rows']} rows."))
            if result['errors']:
                messages.warning(request, _(f"{len(result['errors'])} filas con errores."))
            return render(
                request,
                'admin/csvfixture_importer/panel.html',
                {
                    'form': CSVUploadForm(),
                    'summary': result,
                }
            )
    else:
        form = CSVUploadForm()
    return render(
        request,
        'admin/csvfixture_importer/panel.html',
        {
            'form': form,
            'pending_confirm': True,
        }
    )
