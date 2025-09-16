from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import NoteForm
from .models import Note
from .util.summarizer import TextSummarizer


class NoteIndex(LoginRequiredMixin, generic.ListView):
    model = Note


class NoteCreate(LoginRequiredMixin, generic.CreateView):
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy("notes:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        body = form.cleaned_data.get("body", "")
        try:
            summarizer = TextSummarizer(language="japanese")
            summary_text = summarizer.summarize(body, sentence_count=3)
        except Exception:
            # 失敗時は空文字やトリミングでフォールバック
            summary_text = (body or "")[:120]
        # 保存前にインスタンスへセット
        if hasattr(form.instance, "summary"):
            form.instance.summary = summary_text or (
                    body[:160] + ("…" if len(body) > 160 else "")
            )
        return super().form_valid(form)