import logging
import langid
from typing import Optional, cast, Any, Callable
from django.conf import settings
from django.http import HttpRequest
from googletrans import Translator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from django.contrib import messages
from django.views.generic import CreateView

logger = logging.getLogger(__name__)

LANG_MAP = {
    "ja": "japanese",
    "en": "english",
}

class MessageOnSuccessMixin:
    """
    成功リダイレクト時にフラッシュメッセージを出すための Mixin
    """
    request: HttpRequest
    success_message: Optional[str] = None
    success_level: int = messages.SUCCESS

    def get_success_message(self):
        """最終的に表示するメッセージ文字列を返す"""
        return self.success_message

    def get_success_url(self) -> str:
        """リダイレクト URL 解決前にメッセージを積む"""
        msg = self.get_success_message()
        if msg:
            messages.add_message(self.request, self.success_level, msg)
        parent = cast(Any, super())
        return parent.get_success_url()


class TextSummarizer:
    """
    sumy の TextRank を用いた簡易要約（抽出）

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
    def __init__(self, language: str = "japanese",
                 algorithm: Optional[Callable[[], Any]] = None) -> None:
        self.language = language
        self.summarizer = algorithm() if algorithm else TextRankSummarizer()

    def detect_lang(self, text: str, default: str = "ja") -> str:
        """
        text の言語を判定して 'ja' or 'en' を返す。判定できない場合は default
        """
        if not isinstance(text, str):
            text = str(text)
        if not text or not text.strip():
            return default
        code, _ = langid.classify(text)
        return "en" if code == "en" else "ja"

    def summarize_text(self, text: str, sentence_count: int = 3) -> str:
        """
        英語または日本語の text を要約して返す
        """
        if not isinstance(text, str):
            text = str(text)
        if not text or not text.strip():
            return ""

        lang_code = self.detect_lang(text, default="ja")
        ja_text = text
        if lang_code == "en":
            # 英語 → 日本語に翻訳
            ja_text = Translator().translate(text, src="en", dest="ja").text
        # 要約
        parser = PlaintextParser.from_string(ja_text, Tokenizer("japanese"))
        summarizer = TextRankSummarizer()
        sentences = summarizer(parser.document, max(1, sentence_count))
        return " ".join(str(s) for s in sentences)


class SummaryAndMessageMixin:
    create_success_message:str = "作成しました。"
    update_success_message:str = "更新しました。"
    fallback_message:str = "要約の生成に失敗したため、本文の冒頭を保存しました。"
    fallback_level: int = messages.WARNING
    success_message: str
    success_level: int

    @staticmethod
    def make_summary(body: str) -> tuple[str, bool]:
        """
        本文 body から要約を生成する。失敗した場合は本文の冒頭120文字を返す
        """
        try:
            summarizer = TextSummarizer(language="japanese")
            return summarizer.summarize_text(body or "", sentence_count=3), False
        # 予見できる入力/設定ミス
        except (ValueError, KeyError, TypeError) as e:
            logger.warning("Summarizer input/config error: %s", e, exc_info=True)
            return (body or "")[:120], True
        except Exception as e:
            logger.exception(f"Unexpected summarizer failure, {e}")
            if settings.DEBUG:
                raise
            return (body or "")[:120], True

    def form_valid(self, form):
        body = form.cleaned_data.get("body", "")
        summary_text, fallback_used = self.make_summary(body)

        if hasattr(form.instance, "summary"):
            form.instance.summary = summary_text or (
                (body or "")[:160] + ("…" if len(body) > 160 else "")
            )

        if fallback_used:
            self.success_message = getattr(self, "fallback_message",
                                           "要約の生成に失敗したため、本文の冒頭を保存しました。")
            self.success_level = getattr(self, "fallback_level", messages.WARNING)
        else:
            if isinstance(self, CreateView):
                #  CreateView の場合
                self.success_message = getattr(self, "create_success_message", "作成しました。")
            else:
                # UpdateView の場合
                self.success_message = getattr(self, "update_success_message", "更新しました。")
            self.success_level = messages.SUCCESS

        parent = cast(Any, super())
        return parent.form_valid(form)
