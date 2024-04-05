from django.shortcuts import render, redirect
from django.http import Http404
from .models import Audio
from .forms import AudioForm
from os.path import splitext


def index(request):
    audio_list = Audio.objects.order_by('-publication_date')
    return render(request, 'app/index.html', {'audio_list': audio_list})


def add_audio(request):
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES or None)
        if form.is_valid():
            audio = form.save(commit=False)
            audio.name = splitext(audio.file.name)[0]
            audio.save()
            return redirect('app:audio_list')
    else:
        form = AudioForm()
    return render(request, 'app/add.html', {'form': form})
