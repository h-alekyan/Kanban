from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Task
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
 
    if request.method == 'POST':
        title = request.form.get('title')
        descr = request.form.get('descr')
        stat = request.form.get('stat')

        new_task = Task(title=title, descr=descr, stat=stat, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added!", category="success")
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/kanban', methods=["GET", "POST"])
def kanban():
    return render_template("kanban.html", user=current_user)
