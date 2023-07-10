from flask import Flask, redirect, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Todo
from sqlalchemy.sql import text

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Sunniva2023'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = False
debug = DebugToolbarExtension(app)


connect_db(app)

@app.route('/')
def index_page():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/api/todos')
def list_todos():
    """Iterates over todo's and returns with JSON"""
    all_todos = [todo.serialize() for todo in Todo.query.all()]
    return jsonify(todos=all_todos)

@app.route('/api/todos/<int:id>')
def get_todo(id):
    """Grab's a single todo with id """
    todo = Todo.query.get_or_404(id)
    return jsonify(todo=todo.serialize())

@app.route('/api/todos', methods=["POST"])
def create_todo():
    """Creates a new todo and adds to Todo JSON"""
    new_todo = Todo(title=request.json['title'])
    if new_todo.title == None:
        return {
        'Error': "Please Enter a title!"
    }
    else:
        db.session.add(new_todo)
        db.session.commit()
        response_json = jsonify(todo=new_todo.serialize())
        return (response_json, 201)

@app.route('/api/todos/<int:id>', methods=["PATCH"])
def update_todo(id):
    """update todo's title or done"""
    todo = Todo.query.get_or_404(id)
    todo.title = request.json.get('title', todo.title)
    todo.done = request.json.get('done', todo.done)
    db.session.commit()
    return jsonify(todo=todo.serialize())

@app.route('/api/todos/<int:id>', methods=["DELETE"])
def delete_todo(id):
    """Delete todos with api request"""
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify(message='DELETED')