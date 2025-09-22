import logging
import re
import langid
import ollama
from typing import Optional, cast, Any, Callable
from django.conf import settings
from django.http import HttpRequest
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.text_rank import TextRankSummarizer
from django.contrib import messages
from django.views.generic import CreateView

logger = logging.getLogger(__name__)
_JP_SENT_SPLIT = re.compile(r'(?<=[。！？])\s+')


class MessageOnSuccessMixin:
    """
    成功リダイレクト時にフラッシュメッセージを出すための Mixin
    """
    request: HttpRequest
    success_message: Optional[str] = None
    success_level: int = messages.SUCCESS

    def get_success_message(self):
        """
        最終的に表示するメッセージ文字列を返す
        """
        return self.success_message

    def get_success_url(self) -> str:
        """
        リダイレクト URL 解決前にメッセージを積む
        """
        msg = self.get_success_message()
        if msg:
            messages.add_message(self.request, self.success_level, msg)
        parent = cast(Any, super())
        return parent.get_success_url()


class TextSummarizer:
    """
    sumy の TextRank を用いた簡易要約

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

    @staticmethod
    def _trim_to_n_sentences_jp(text: str, n: int) -> str:
        """
        日本語テキスト text を文で分割、最大 n 文までを連結して返す
        """
        n = max(1, int(n))
        sents = [s for s in _JP_SENT_SPLIT.split(text.strip()) if s]
        return "".join(sents[:n]) if len(sents) >= n else "".join(sents)

    def _gen_summary_ja_ollama(self, ja_text: str, sentence_count: int) -> str:
        N = max(1, int(sentence_count))
        system = (
            "あなたは意訳重視の要約編集者です。出力は必ず自然な日本語の散文一段落。"
            "箇条書き・番号付け・引用は禁止。原文の語順や文をそのまま使わず必ず言い換える。"
            "原文から連続6文字以上を再利用しない。改行は入れない。"
            "固有名詞・数値・割合・年は保持し、新情報の追加・主観・誇張は禁止。"
            "文末は句点「。」で終える。"
        )
        user = (
            f"次の日本語テキストを{N}文の散文一段落に要約してください。"
            "全体はおおよそ120〜180文字に収め、箇条書きや見出しは出力しないでください。"
            "まず内部で要点を整理し、最終的な散文だけを出力してください。内部メモは表示しないでください。\n\n"
            f"{ja_text}"
        )
        res = ollama.chat(
            model="qwen2.5:7b-instruct",
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
            options={
                "num_predict": 200,
                "temperature": 0.5,
                "top_p": 0.95,
                "top_k": 40,
                "repeat_penalty": 1.15,
                "stop": ["\n- ", "\n1.", "\n•", "\n・"]
            },
        keep_alive="30m",
            stream=False,
        )
        out = res["message"]["content"].strip()
        return self._trim_to_n_sentences_jp(out, N)

    def summarize_text(self, text: str, sentence_count: int = 3) -> str:
        ja_text = text
        try:
            # 生成型
            return self._gen_summary_ja_ollama(ja_text, sentence_count)
        except Exception as e:
            # 生成型が失敗した場合は抽出型
            logger.warning("[ollama warn] %s 抽出型", e)
            parser = PlaintextParser.from_string(ja_text, Tokenizer(self.language))
            sentences = self.summarizer(parser.document, max(1, int(sentence_count)))
            return "".join(str(s) for s in sentences)


class SummaryAndMessageMixin:
    create_success_message: str = "作成しました。"
    update_success_message: str = "更新しました。"
    fallback_message: str = "要約の生成に失敗したため、本文の冒頭を保存しました。"
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
                self.success_message = getattr(self, "create_success_message", "作成しました。")
            else:
                self.success_message = getattr(self, "update_success_message", "更新しました。")
            self.success_level = messages.SUCCESS

        parent = cast(Any, super())
        return parent.form_valid(form)
