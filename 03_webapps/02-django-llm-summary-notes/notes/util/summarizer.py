from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

class TextSummarizer:
    def __init__(self, language="japanese", algorithm=None):
        self.language = language
        self.summarizer = algorithm() if algorithm else TextRankSummarizer()

    def summarize(self, text: str, sentence_count: int = 3) -> str:
        if not text or not text.strip():
            return ""
        parser = PlaintextParser.from_string(text, Tokenizer(self.language))
        summary = self.summarizer(parser.document, sentence_count)
        return " ".join(str(s) for s in summary)
