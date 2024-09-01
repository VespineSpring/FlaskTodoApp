from flask import Flask, redirect, url_for, request, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user/<username>")
def user_page(username):
   return render_template("user.html", name=username)


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name


@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success', name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success', name = user))
   

@app.route("/score/<int:score>")
def score(score):
   return render_template("score.html", marks=score)


@app.route("/result")
def result():
   report_card = {"Maths": 80, "Physics": 77, "Chemistry": 78, "Computer Science": 80, "English": 70}
   return render_template("result.html", result=report_card)


if __name__ == "__main__":
    app.run(debug=True)
