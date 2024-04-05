from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
import magic


def validate_audio_file(value):
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(value.read(1024))
    if not mime_type.startswith('audio/'):
        raise ValidationError(
            gettext_lazy('The uploaded file is not an audio file.'),
            code='invalid'
        )
