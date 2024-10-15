from googleapiclient.discovery import build
from datetime import datetime, timedelta
from services.comment import Comment

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

    def get_recent_videos(self, channel_id, days=2):
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
