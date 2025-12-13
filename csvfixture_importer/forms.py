from django import forms
from django.apps import apps


class CSVUploadForm(forms.Form):
    model = forms.ChoiceField(label='Model', choices=(), required=True)
    csv_file = forms.FileField(label='CSV file', required=True)

    def __init__(self, *args, **kwargs):
        model_name = kwargs.pop('specific_model', None)
        super().__init__(*args, **kwargs)
        models = []
        if model_name:
            models.append((model_name, model_name))
        else:
            for model in [m for m in apps.get_models() if not m._meta.abstract]:
                label = f"{model._meta.app_label}.{model._meta.object_name}"
                models.append((label, label))
            models.sort(key=lambda x: x[1])
        self.fields['model'].choices = models
