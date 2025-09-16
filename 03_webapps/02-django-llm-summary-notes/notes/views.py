from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Note


class NoteIndex(LoginRequiredMixin, generic.ListView):
    model = Note
