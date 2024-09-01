from flask import Flask, redirect, url_for, request, render_template
import json
import os


app = Flask(__name__)
task_file = "tasks.json"


if not os.path.exists(task_file):
   with open(task_file, "w") as file:
        json.dump([], file)


@app.route("/", methods=["POST", "GET"])
def index():
   tasks = get_tasks()

   if request.method == "POST":
      task = request.form["task"]

      with open(task_file, "r") as file:
         data = json.load(file)

      data.append(task)

      with open(task_file, "w") as file:
         json.dump(data, file, indent=4)

      return redirect(url_for("index"))
   else:
      return render_template("index.html", tasks=tasks)
   

def get_tasks():
   with open(task_file, "r") as file:
      tasks = json.load(file)

   return tasks


if __name__ == "__main__":
    app.run(debug=True)
