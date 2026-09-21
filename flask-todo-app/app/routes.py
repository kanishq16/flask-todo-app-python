"""
Routes for the Todo application.
"""
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort

from app import db
from app.models import Todo

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template("index.html", todos=todos)


@main_bp.route("/todos", methods=["POST"])
def add_todo():
    title = request.form.get("title", "").strip()
    if title:
        todo = Todo(title=title)
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for("main.index"))


@main_bp.route("/todos/<int:todo_id>/toggle", methods=["POST"])
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("main.index"))


@main_bp.route("/todos/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("main.index"))


# --- Simple JSON API, for completeness / future frontend use ---

@main_bp.route("/api/todos", methods=["GET"])
def api_list_todos():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return jsonify([t.to_dict() for t in todos])


@main_bp.route("/api/todos", methods=["POST"])
def api_create_todo():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        abort(400, description="Field 'title' is required.")
    todo = Todo(title=title)
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201


@main_bp.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def api_delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"result": "deleted", "id": todo_id})
