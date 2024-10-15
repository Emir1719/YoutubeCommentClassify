from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from services.openai_services import OpenAIService
from services.youtube_service import YouTubeService

app = Flask(__name__)
app.config.from_object(Config)

youtube_service = YouTubeService(api_key=app.config['YOUTUBE_API_KEY'])
openai_service = OpenAIService(api_key=app.config['OPENAI_API_KEY'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        channel_username = request.form.get('channel_username')

        if not channel_username:
            flash('Please enter a channel username.')
            return redirect(url_for('index'))
        
        return redirect(url_for('results', channel_username=channel_username))
    return render_template('index.html')


@app.route('/results/<channel_username>')
def results(channel_username):
    try:
        channel_id = youtube_service.get_channel_id(channel_username)
        video_ids = youtube_service.get_recent_videos(channel_id)
        comments = []

        for video_id in video_ids:
            video_comments = youtube_service.get_comments_from_video(video_id)
            for comment in video_comments:
                comment.clean()
                comment.classify(openai_service)
                comments.append(comment)

    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))
    
    # Sort comments by published_at in descending order
    comments.sort(key=lambda x: x.published_at, reverse=True)
    return render_template('results.html', comments=comments)
    

if __name__ == '__main__':
    app.run(debug=True)
