# Main Flask application entry point
from flask import Flask
from routes import inventory_bp

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable debug mode
    app.config['DEBUG'] = True
    app.config['JSON_SORT_KEYS'] = False
    
    # Register blueprints
    app.register_blueprint(inventory_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
