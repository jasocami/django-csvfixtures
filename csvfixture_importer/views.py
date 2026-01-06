from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .forms import CSVUploadForm
from .importer import import_csv_to_model, get_csv_preview
from .utils import get_model_from_label

# TODO: Check https://docs.djangoproject.com/en/6.0/topics/serialization/#custom-serialization-formats
@staff_member_required
def admin_panel_view(request):
    summary = None
    step = None
    preview = None
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        step = form.get_step_name()
        if step == 'preview':
            step = 'confirm'
            preview = []  # TODO: add preview list of 10 items
            preview = get_csv_preview(form.files.get('csv_file'))
        else:
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
    else:
        model = None
        step = 'preview'
        if m := request.GET.get('model', None):
            model = m
        form = CSVUploadForm(specific_model=model)
    return render(
        request,
        'admin/csvfixture_importer/panel.html',
        {
            'form': form,
            'preview': preview,
            'summary': summary,
            'step': step
        }
    )
