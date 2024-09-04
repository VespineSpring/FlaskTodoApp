from flask import Flask, redirect, url_for, request, render_template
import json
import uuid
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz


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

    task_dict = {
        "id": str(uuid.uuid4()),
        "task": task,
        "status": "incomplete"
    }
    
    with open(TASK_FILE, "r") as file:
        data = json.load(file)

    data.append(task_dict)

    with open(TASK_FILE, "w") as file:
        json.dump(data, file, indent=4)
   

def get_tasks():
    initialize_task_file()

    with open(TASK_FILE, "r") as file:
        tasks = json.load(file)

    return tasks


@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.get_json()
    task_id = data.get("id")
    new_status = data.get("status")

    tasks = get_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            break

    with open(TASK_FILE, "w") as file:
            json.dump(tasks, file, indent=4)

    return '', 204


def reset_tasks():
    tasks = get_tasks()
    for task in tasks:
        task["status"] = "incomplete"

    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

    print("Tasks reset to incomplete")


if __name__ == "__main__":
    initialize_task_file() 
    
    scheduler = BackgroundScheduler()
    ist = pytz.timezone('Asia/Kolkata')
    trigger = CronTrigger(hour=0, minute=0, timezone=ist)
    scheduler.add_job(reset_tasks, trigger)
    scheduler.start()
    
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
