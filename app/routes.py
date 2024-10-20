from app import app


@app.route("/")
@app.route("/index")
def index():
    return "SQL more like sea quail amiright?"
