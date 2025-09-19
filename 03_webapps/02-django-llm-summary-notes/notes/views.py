from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from .forms import NoteForm
from .models import Note
from .util.summarizer import MessageOnSuccessMixin, SummaryAndMessageMixin


class NoteIndex(LoginRequiredMixin, generic.ListView):
    model = Note
    paginate_by = 20

    def get_queryset(self):
        queryset = Note.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(body__icontains=keyword)
            )
        return queryset


class NoteCreate(LoginRequiredMixin, SummaryAndMessageMixin, MessageOnSuccessMixin, generic.CreateView):
    model = Note
    form_class = NoteForm
    action_label = "新規作成"
    button_label = "登録"
    create_success_message = "メモを登録しました。"
    template_name = "notes/form.html"
    success_url = reverse_lazy("notes:index")


class NoteUpdate(LoginRequiredMixin, SummaryAndMessageMixin, MessageOnSuccessMixin, generic.UpdateView):
    model = Note
    form_class = NoteForm
    action_label = "編集"
    button_label = "更新"
    context_object_name = "note"
    update_success_message = "メモを更新しました。"
    template_name = "notes/form.html"
    success_url = reverse_lazy("notes:index")


class NoteDelete(LoginRequiredMixin, MessageOnSuccessMixin, generic.DeleteView):
    model = Note
    action_label = "削除"
    success_message = "削除しました。"
    success_url = reverse_lazy("notes:index")
