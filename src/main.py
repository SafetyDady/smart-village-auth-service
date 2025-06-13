import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models.user import db, User, Village, House
from src.routes.auth import auth_bp
from src.routes.user_management import user_bp
from src.routes.admin_homeowner_village import admin_bp, homeowner_bp, village_house_bp

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)

    # Configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-in-production')

    # Database configuration for Vercel
    database_url = os.getenv('DATABASE_URL', 'sqlite:///social_auth.db')
    if database_url.startswith('sqlite:///') and not database_url.startswith('sqlite:////'):
        # For Vercel, use /tmp directory for SQLite
        db_path = '/tmp/social_auth.db'
        database_url = f'sqlite:///{db_path}'

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # CORS configuration for Vercel
    CORS(app, origins=['*'])  # Allow all origins for now

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(homeowner_bp, url_prefix='/api/homeowner')
    app.register_blueprint(village_house_bp, url_prefix='/api/village-house')

    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Smart Village Auth Service',
            'version': '1.0.0'
        })

    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Smart Village Social Auth Service',
            'status': 'running',
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth/*',
                'user': '/api/user/*',
                'admin': '/api/admin/*',
                'homeowner': '/api/homeowner/*',
                'village-house': '/api/village-house/*'
            }
        })

    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create super admin if not exists
        super_admin_email = os.getenv('SUPER_ADMIN_EMAIL')
        if super_admin_email:
            existing_super_admin = User.query.filter_by(email=super_admin_email).first()
            if not existing_super_admin:
                super_admin = User(
                    email=super_admin_email,
                    first_name='Super',
                    last_name='Admin',
                    role='super_admin',
                    status='active'
                )
                db.session.add(super_admin)
                db.session.commit()

    return app

# Create the Flask application instance
app = create_app()

# For Vercel deployment - this is the WSGI application
application = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)

