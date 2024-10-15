import re
import string
import emoji

class TextCleaner:
    @staticmethod
    def clean(text: str) -> str:
        """
        Verilen metni temizler: Sayıları, noktalama işaretlerini ve emojileri kaldırır.
        """
        # Sayıları kaldır
        text = re.sub(r'\d+', '', text)
        # Noktalama işaretlerini kaldır
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Emojileri kaldır
        text = emoji.replace_emoji(text, replace='')
        # Baş ve sondaki boşlukları temizle
        return text.strip()