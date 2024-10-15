from flask import Flask

from config import Config
from .services.youtube_service import YouTubeService
from .services.openai_services import OpenAIService

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Servisleri oluştur
    app.youtube_service = YouTubeService(api_key=app.config['YOUTUBE_API_KEY'])
    app.openai_service = OpenAIService(api_key=app.config['OPENAI_API_KEY'])

    # Blueprint'leri kaydet
    from .routes.index import index_bp
    from .routes.results import results_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(results_bp)

    return app
