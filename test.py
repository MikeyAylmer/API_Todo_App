from unittest import TestCase

from app import app
from models import db, Todo

# use test database and dont clutter test with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://todo_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML page with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class TodosTestCase(TestCase):
    """Tests for todos"""

    def setUp(self):
        """Make a new todo"""

        Todo.query.delete()
        db.session.commit()

        todo = Todo(title='TestTodo', done=False)
        db.session.add(todo)
        db.session.commit()

        self.todo_id=todo.id
    
    def tearDown(self):
        """clean up"""
        db.session.rollback()

    def test_all_todos(self):
        """tests all todos"""
        with app.test_client() as client:
            resp = client.get('/api/todos')
            self.assertEqual(resp.status_code, 200)

            self.assertEqual(
                resp.json,
                { 'todos':[{
                    'id': self.todo_id,
                    'title': 'TestTodo',
                    'done': False
                }]}
            )
    

    def test_get_single_todo(self):
        """Test a specific todo based off id"""
        with app.test_client() as client:
            resp = client.get(f'/api/todos{self.todo_id}')
            self.assertEqual(resp.status_code, 200)

            self.assertEqual(
                resp.json,
                { 'todos':[{
                    'id': self.todo_id,
                    'title': 'TestTodo',
                    'done': False
                }]}
            )

    def test_create_todo(self):
        """Test creating a new todo"""
        with app.test_client() as client:
            resp = client.post(
               "/api/todos", json={
                   "title": "TestTodo",
                   "done": False
               } 
            )
            self.assertEqual(resp.status_code, 201)

            # Dont know the id, so test then remove
            self.assertIsInstance(resp.json['todo']['id'], int)
            del resp.json['todo']['id']

            self.assertEqual(
                resp.json,
                {'todos': {'title': 'TestTodo', 'done': False}}
            )

            self.assertEqual(Todo.query.count(), 2)
