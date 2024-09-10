from flask import Flask, render_template # type: ignore

app = Flask(__name__)

def create_app():
    """Create the Flask app instance"""

    @app.route("/")
    def index():
        return render_template("landing.html")

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/register")
    def register():
        return render_template("register.html")

    return app

app = create_app()

if __name__ == "__main__":
    app.run()