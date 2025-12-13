from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .forms import CSVUploadForm
from .importer import import_csv_to_model
from .utils import get_model_from_label


@staff_member_required
def admin_panel_view(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            model_label = form.cleaned_data['model']
            csv_file = form.cleaned_data['csv_file']
            model = get_model_from_label(model_label)
            result = import_csv_to_model(model, csv_file)
            messages.success(
                request,
                _(f"Uploaded successfully: {result['created']} created objects of {result['total_rows']} rows.")
            )
            if result['errors']:
                messages.warning(request, _(f"{len(result['errors'])} rows with errors."))
            return render(
                request,
                'admin/csvfixture_importer/panel.html',
                {
                    'form': CSVUploadForm(),
                    'summary': result,
                }
            )
    else:
        model = None
        if m := request.GET.get('model', None):
            model = m
        form = CSVUploadForm(specific_model=model)
    return render(
        request,
        'admin/csvfixture_importer/panel.html',
        {
            'form': form,
        }
    )
