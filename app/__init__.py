from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates')

    from .routes import allstarfull_routes, home_bp

    # Register blueprints/routes
    app.register_blueprint(home_bp, url_prefix='/home')
    app.register_blueprint(allstarfull_routes, url_prefix="/allstarfull")

    return app

if __name__ == "__main__":
    app = create_app()
    #app.run(debug=True)  # Ensure you're running in debug mode