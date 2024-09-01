from flask import Flask, redirect, url_for


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/vespine/")
def about_vespine():
    info = """
    Hello, my name is Vespine or in short you can call me Ve.
    I am from India and I am 14 years old.
    I have been coding since 4 years.
    """
    return info


@app.route("/home")
def home_page():
    return "<h1>This is a home page.</h1>"


@app.route("/guest/<guest>")
def hello_guest(guest):
   return f"Hello {guest} as Guest"


@app.route("/admin")
def hello_admin():
   return 'L Admin'


@app.route("/user/<name>")
def hello_user(name):
   if name =="admin":
      return redirect(url_for("hello_admin"))
   else:
      return redirect(url_for("hello_guest", guest = name))


if __name__ == "__main__":
    app.run(debug=True)
