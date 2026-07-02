"""A small sample Flask application.

Uses the application-factory pattern so tests can create isolated app
instances. Run with `flask --app app run` or `python app.py`.
"""
from __future__ import annotations

from datetime import datetime, timezone

from flask import Flask, jsonify, request


def create_app(config: dict | None = None) -> Flask:
    """Build and configure a Flask application instance."""
    app = Flask(__name__)
    app.config.update(config or {})

    # A tiny in-memory store so we have something to CRUD against.
    todos: list[dict] = []
    next_id = {"value": 1}

    @app.route("/")
    def hello():
        return "Hello, World!"

    @app.get("/health")
    def health():
        return jsonify(
            status="ok",
            time=datetime.now(timezone.utc).isoformat(),
        )

    @app.get("/greet/<name>")
    def greet(name: str):
        return jsonify(message=f"Hello, {name}!")

    @app.get("/todos")
    def list_todos():
        return jsonify(todos=todos)

    @app.post("/todos")
    def create_todo():
        data = request.get_json(silent=True) or {}
        title = data.get("title")
        if not title:
            return jsonify(error="'title' is required"), 400

        todo = {"id": next_id["value"], "title": title, "done": False}
        next_id["value"] += 1
        todos.append(todo)
        return jsonify(todo=todo), 201

    return app


# Module-level app for `flask --app app run`.
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
