from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from django.contrib import messages
from django.views.generic import CreateView


class MessageOnSuccessMixin:
    """
    成功リダイレクト時にフラッシュメッセージを出すための Mixin
    """
    success_message = None
    success_level = messages.SUCCESS

    def get_success_message(self):
        """最終的に表示するメッセージ文字列を返す。必要に応じてオーバーライド可。"""
        return self.success_message

    def get_success_url(self):
        """リダイレクト URL 解決前にメッセージを積む"""
        msg = self.get_success_message()
        if msg:
            messages.add_message(self.request, self.success_level, msg)
        return super().get_success_url()


class TextSummarizer:
    """
    sumy の TextRank を用いた簡易要約器。

    Parameters
    ----------
    language : str
        Tokenizer に渡す言語。日本語なら 'japanese'
    algorithm : Optional[Callable]
        既定以外の要約アルゴリズムを使いたい場合に差し替える

    Notes
    -----
    - 入力テキストが空または空白のみの場合は空文字を返す
    - sentence_count は抽出する文数。短文のときはその範囲で返る
    """
    def __init__(self, language="japanese", algorithm=None):
        self.language = language
        self.summarizer = algorithm() if algorithm else TextRankSummarizer()

    def summarize(self, text: str, sentence_count: int = 3) -> str:
        """
        与えられたテキストを要約し、文を空白で連結して返す。

        Parameters
        ----------
        text : str
            入力本文
        sentence_count : int
            抽出する最大文数

        Returns
        -------
        str
            要約テキスト（空文字可）。
        """
        if not text or not text.strip():
            return ""
        parser = PlaintextParser.from_string(text, Tokenizer(self.language))
        summary = self.summarizer(parser.document, sentence_count)
        return " ".join(str(s) for s in summary)


class SummaryAndMessageMixin:
    """
    Create/Update 共通で:
      - form_valid() 内で本文から要約を作る
      - 生成失敗時は fallback 文言/レベル(WARNING)に切り替える
      - 成功時は Create/Update でメッセージを出し分ける
    """

    def make_summary(self, body: str) -> tuple[str, bool]:
        try:
            summarizer = TextSummarizer(language="japanese")
            return summarizer.summarize(body or "", sentence_count=3), False
        except Exception:
            return (body or "")[:120], True

    def form_valid(self, form):
        body = form.cleaned_data.get("body", "")
        summary_text, fallback_used = self.make_summary(body)

        if hasattr(form.instance, "summary"):
            form.instance.summary = summary_text or (
                    (body or "")[:160] + ("…" if len(body) > 160 else "")
            )

        if fallback_used:
            self.success_message = self.fallback_message
            self.success_level = self.fallback_level
        else:
            if isinstance(self, CreateView):
                self.success_message = self.create_success_message
            else:
                self.success_message = self.update_success_message
            self.success_level = messages.SUCCESS

        return super().form_valid(form)
