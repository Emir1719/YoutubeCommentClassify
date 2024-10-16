from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from app.services.comment import Comment
from app.services.youtube_service import YouTubeService

results_bp = Blueprint('results', __name__, url_prefix='/results')

@results_bp.route('/<channel_username>')
def results(channel_username):
    youtube_service: YouTubeService = current_app.youtube_service
    comments = []

    try:
        channel_id = youtube_service.get_channel_id(channel_username)
        video_ids = youtube_service.get_recent_videos(channel_id)

        for video_id in video_ids:
            video_comments: list[Comment] = youtube_service.get_comments_from_video(video_id)
            
            for comment in video_comments:
                comment.clean()
                #comment.classify(current_app.openai_service)
                if comment.text.strip():
                    comments.append(comment)

    except Exception as e:
        flash(str(e))
        return redirect(url_for('index.index'))
    
    comments.sort(key=lambda x: x.published_at, reverse=True)
    
    return render_template(
        'results.html', 
        comments=comments, 
        positive_comments=filter(comments, "Positive"),
        negative_comments=filter(comments, "Negative"),
        question_comments=filter(comments, "Question"),
        donation_comments=filter(comments, "Donation"),
    )


def filter(comments: list[Comment], filter: str):
    return [comment for comment in comments if comment.category == filter]