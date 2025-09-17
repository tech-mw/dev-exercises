from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .forms import NoteForm
from .models import Note
from .util.summarizer import MessageOnSuccessMixin, SummaryAndMessageMixin


class NoteIndex(LoginRequiredMixin, generic.ListView):
    model = Note
    paginate_by = 10


class NoteCreate(LoginRequiredMixin, SummaryAndMessageMixin, MessageOnSuccessMixin, generic.CreateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/form.html"
    action_label = "新規作成"
    button_label = "登録"
    success_url = reverse_lazy("notes:index")


class NoteUpdate(LoginRequiredMixin, SummaryAndMessageMixin, MessageOnSuccessMixin, generic.UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/form.html"
    action_label = "編集"
    button_label = "更新"
    success_message = "更新しました。"
    success_url = reverse_lazy("notes:index")


class NoteDelete(LoginRequiredMixin, MessageOnSuccessMixin, generic.DeleteView):
    model = Note
    action_label = "削除"
    success_message = "削除しました。"
    success_url = reverse_lazy("notes:index")
