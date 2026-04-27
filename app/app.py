from flask import Flask, jsonify, request

app = Flask(__name__)
todos = []

@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    todo = {"id": len(todos) + 1, "task": data["task"], "done": False}
    todos.append(todo)
    return jsonify(todo), 201

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)