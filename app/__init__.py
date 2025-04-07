"""Initialize Flask application."""
import os
import logging
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.utils.init_nltk import init_nltk

csrf = CSRFProtect()

def create_app():
    """Create and configure the Flask application."""
    # Initialize NLTK data before creating the app
    init_nltk()
    
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize CSRF protection
    csrf.init_app(app)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main.bp)
    
    return app 