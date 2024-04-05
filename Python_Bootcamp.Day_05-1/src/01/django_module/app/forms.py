from django.forms import ModelForm, FileInput
from .models import Audio


class AudioForm(ModelForm):
    class Meta:
        model = Audio
        fields = ['file']

        # widgets = {
        #     'file': FileInput()
        # }
