from flask import Flask, redirect, url_for, request, render_template
import json
import os


app = Flask(__name__)
TASK_FILE = "tasks.json"


def initialize_task_file():
   if not os.path.exists(TASK_FILE) or os.path.getsize(TASK_FILE) == 0:
      with open(TASK_FILE, "w") as file:
         json.dump([], file)


@app.route("/", methods=["POST", "GET"])
def index():
   if request.method == "POST":
      task = request.form["task"]

      save_task(task)

      return redirect(url_for("index"))
   else:
      tasks = get_tasks()
      return render_template("index.html", tasks=tasks)


def save_task(task):
   if not task:
      return
   
   initialize_task_file()
   
   with open(TASK_FILE, "r") as file:
      data = json.load(file)

   data.append(task)

   with open(TASK_FILE, "w") as file:
      json.dump(data, file, indent=4)
   

def get_tasks():
   initialize_task_file()

   with open(TASK_FILE, "r") as file:
      tasks = json.load(file)

   return tasks


if __name__ == "__main__":
   initialize_task_file() 
   app.run(debug=True)
