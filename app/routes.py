from flask import render_template, redirect, request, flash, url_for
from app import app, db
from app.models import MyTask

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        current_task = request.form["content"]
        if not current_task.strip():
            flash("Task content cannot be empty!", "error")
            return redirect(url_for("index"))
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "error")
        return redirect(url_for("index"))
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)

# Route to handle task deletion
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id: int):
    delete_task = db.session.get(MyTask, id)
    if delete_task is None:
        flash("Task not found!", "error")
        return redirect(url_for("index"))
    try:
        db.session.delete(delete_task)
        db.session.commit()
        flash("Task deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("index"))

# Route to handle task updates
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id: int):
    task_to_update = db.session.get(MyTask, id)
    if task_to_update is None:
        flash("Task not found!", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        new_content = request.form["content"]
        if not new_content.strip():
            flash("Task content cannot be empty!", "error")
            return redirect(url_for("update", id=id))
        task_to_update.content = new_content
        try:
            db.session.commit()
            flash("Task updated successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "error")
        return redirect(url_for("index"))
    else:
        return render_template("update.html", task=task_to_update)

# Route to toggle task completion status
@app.route("/toggle/<int:id>", methods=["POST"])
def toggle(id: int):
    task_to_toggle = db.session.get(MyTask, id)
    if task_to_toggle is None:
        flash("Task not found!", "error")
        return redirect(url_for("index"))
    task_to_toggle.complete = not task_to_toggle.complete
    try:
        db.session.commit()
        flash("Task status updated!", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for("index"))

# Route to filter tasks by completion status
@app.route("/filter/<status>")
def filter_tasks(status):
    if status == "complete":
        tasks = MyTask.query.filter_by(complete=True).order_by(MyTask.created).all()
    elif status == "incomplete":
        tasks = MyTask.query.filter_by(complete=False).order_by(MyTask.created).all()
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
    return render_template("index.html", tasks=tasks)