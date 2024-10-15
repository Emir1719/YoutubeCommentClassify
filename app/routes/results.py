from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from app.services.comment import Comment

results_bp = Blueprint('results', __name__, url_prefix='/results')

@results_bp.route('/<channel_username>')
def results(channel_username):
    youtube_service = current_app.youtube_service
    comments = []

    try:
        channel_id = youtube_service.get_channel_id(channel_username)
        video_ids = youtube_service.get_recent_videos(channel_id)

        for video_id in video_ids:
            video_comments: list[Comment] = youtube_service.get_comments_from_video(video_id)
            
            for comment in video_comments:
                comment.clean()
                comment.classify(current_app.openai_service)
                if comment.text.strip():
                    comments.append(comment)

    except Exception as e:
        flash(str(e))
        return redirect(url_for('index.index'))
    
    comments.sort(key=lambda x: x.published_at, reverse=True)
    
    positive_comments = [comment for comment in comments if comment.category == 'Positive']
    negative_comments = [comment for comment in comments if comment.category == 'Negative']
    question_comments = [comment for comment in comments if comment.category == 'Question']
    donation_comments = [comment for comment in comments if comment.category == 'Donation']
    
    return render_template(
        'results.html', 
        comments=comments, 
        positive_comments=positive_comments,
        negative_comments=negative_comments,
        question_comments=question_comments,
        donation_comments=donation_comments,
    )
