from flask import Flask, render_template # type: ignore

def create_app():
    """Create the Flask app instance"""
    app = Flask(__name__)


    @app.route("/")
    def index_page():
        return render_template("landing.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run()