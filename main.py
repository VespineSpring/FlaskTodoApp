from flask import Flask


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/vespine")
def about_vespine():
    info = """
    Hello, my name is Vespine or in short you can call me Ve.
    I am from India and I am 14 years old.
    I have been coding since 4 years.
    """
    return info


if __name__ == "__main__":
    app.run(debug=True)