from flask import Blueprint, render_template, request, redirect, url_for, flash

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        channel_username = request.form.get('channel_username')

        if not channel_username:
            flash('Please enter a channel username.')
            return redirect(url_for('index.html'))
        
        return redirect(url_for('results.results', channel_username=channel_username))
    
    return render_template('index.html')
