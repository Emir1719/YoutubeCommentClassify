from googleapiclient.discovery import build
from datetime import datetime, timedelta
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


class YouTubeService:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def get_channel_id(self, channel_username):
        request = self.youtube.search().list(
            part="snippet",
            q=channel_username,
            type="channel"
        )
        response = request.execute()
        items = response.get('items')
        if not items:
            raise Exception("Channel not found.")
        channel_id = items[0]['snippet']['channelId']
        return channel_id

    def get_recent_videos(self, channel_id, days=8):
        videos = []
        request = self.youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=100,
            order='date',
            publishedAfter=(datetime.utcnow() - timedelta(days=days)).isoformat("T") + "Z"
        )
        while request:
            response = request.execute()
            for item in response['items']:
                if item['id']['kind'] == 'youtube#video':
                    videos.append(item['id']['videoId'])
            request = self.youtube.search().list_next(request, response)
        return videos

    def get_comments_from_video(self, video_id):
        comments = []
        request = self.youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,
            textFormat='plainText'
        )
        while request:
            response = request.execute()
            for item in response['items']:
                snippet = item['snippet']['topLevelComment']['snippet']
                comment_text = snippet['textOriginal']
                comment_id = item['snippet']['topLevelComment']['id']
                comment_link = f"https://www.youtube.com/watch?v={video_id}&lc={comment_id}"
                published_at = datetime.strptime(snippet['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")

                comment = Comment(
                    video_id=video_id,
                    text=comment_text,
                    link=comment_link,
                    published_at=published_at
                )
                comments.append(comment)
            request = self.youtube.commentThreads().list_next(request, response)
        return comments
