from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import  Task
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required #to see this, the user has to be logged in
def home():
    """
    Showing the user the add task page (which is also the home page), if there is a POST request, accept the details and if all good,
    create a new task
    """
 
    if request.method == 'POST':
        title = request.form.get('title')
        descr = request.form.get('descr')
        stat = request.form.get('stat')

        new_task = Task(title=title, descr=descr, stat=stat, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added!", category="success")
    return render_template("home.html", user=current_user)




@views.route('/delete-task', methods=['POST'])
def delete_task():
    """Deleting a task in the database (returns {} because the delete function in index.js already redirects to the kanban page)"""
    task = json.loads(request.data)
    taskId = task['taskId']
    task = Task.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()

    return jsonify({})

@views.route('/kanban', methods=["GET", "POST"])
def kanban():
    """Rendering the kanban board"""
    return render_template("kanban.html", user=current_user)


@views.route('/move-task', methods=['POST'])
def move_task():

    """Moving a task in to a different status (returns {} because the delete function in index.js already redirects to the kanban page)"""

    task = json.loads(request.data)
    taskId = task['taskId']
    newStatus = task['newStatus']
    task = Task.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            task.stat = newStatus
            db.session.commit()
    return jsonify({})
