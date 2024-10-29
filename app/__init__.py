import os
from flask import Flask, render_template

def create_app():
    app = Flask(__name__, template_folder='templates')

    #we need secret key in order to use url_for function
    app.config['SECRET_KEY'] = os.urandom(24).hex() #making it a random hex = more secure
    from app.routes import allstarfull_routes, home_bp

    # Register blueprints/routes
    app.register_blueprint(home_bp, url_prefix='/home')
    app.register_blueprint(allstarfull_routes, url_prefix="/allstarfull")

    #defined this here because we want this to display as the first page u see, always
    @app.route('/')
    def home():
        return render_template('home.html', title="SEA QUAIL BABY", message="SQL more like sea quail amiright?")

    return app

if __name__ == "__main__":
    app = create_app()
    #app.run(debug=True)  # Ensure you're running in debug mode