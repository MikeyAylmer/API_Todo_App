from models import db, connect_db, Todo
from app import app

app.app_context().push()

db.drop_all()
db.create_all()

todos = [
    Todo(title='Clean the house'),
    Todo(title='Make Breakfast'),
    Todo(title='Play with Sunni', done=True),
    Todo(title='Take A Shower'),
    Todo(title='Let Bella and Bowser Play', done=True),
    Todo(title='Make Dinner')]

db.session.add_all(todos)
db.session.commit()