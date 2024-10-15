import re
import string
from services.openai_services import OpenAIService

class Comment:
    def __init__(self, video_id, text, link, published_at):
        self.video_id = video_id
        self.text = text
        self.link = link
        self.published_at = published_at
        self.category = None  # Will be set after classification

    def clean(self):
        # Remove numbers
        self.text = re.sub(r'\d+', '', self.text)
        # Remove punctuation
        self.text = self.text.translate(str.maketrans('', '', string.punctuation))
        # Remove emojis
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # Emoticons
            u"\U0001F300-\U0001F5FF"  # Symbols & Pictographs
            u"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
            u"\U0001F1E0-\U0001F1FF"  # Flags
            "]+", flags=re.UNICODE)
        self.text = emoji_pattern.sub(r'', self.text)
        self.text = self.text.strip()

    def classify(self, openai_service: OpenAIService):
        # Corrected: only pass self.text as an argument
        self.category = openai_service.classify_comment(self.text)
        
    # Sınıfı bir sözlük yapısına dönüştürme fonksiyonu
    def to_dict(self):
        return {
            "text": self.text,
            "published_at": self.published_at.strftime('%d.%m.%Y %H:%M:%S') if self.published_at else None,
            "category": self.category,
            "link": self.link
        }
        
    @classmethod
    def from_dict(cls, data):
        from datetime import datetime
        return cls(
            text=data['text'],
            published_at=datetime.strptime(data['published_at'], '%d.%m.%Y %H:%M:%S'),
            category=data['category'],
            link=data['link']
        )
