from app.services.openai_services import OpenAIService
from app.services.text_cleaner import TextCleaner

class Comment:
    def __init__(self, video_id, text, link, published_at):
        self.video_id = video_id
        self.text = text
        self.link = link
        self.published_at = published_at
        self.category = None  # Will be set after classification

    def clean(self):
        self.text = TextCleaner.clean(self.text)

    def classify(self, openai_service: OpenAIService):
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
    def from_dict(self, data):
        from datetime import datetime
        return self(
            text=data['text'],
            published_at=datetime.strptime(data['published_at'], '%d.%m.%Y %H:%M:%S'),
            category=data['category'],
            link=data['link']
        )
