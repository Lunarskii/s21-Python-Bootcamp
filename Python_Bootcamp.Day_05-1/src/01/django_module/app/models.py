from django.db import models
from django.utils import timezone
from .validators import validate_audio_file


class Audio(models.Model):
    publication_date = models.DateTimeField('date published', default=timezone.now)
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='audio', default='default_audio/default.mp3', validators=[validate_audio_file])

    def __str__(self):
        return self.name
