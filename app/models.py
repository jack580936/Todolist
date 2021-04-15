from app import db
from datetime import datetime


class Todo(db.Model):
    __tablename__ = "todo_list"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    create_datetime = db.Column(db.DateTime, default=datetime.now)
    done = db.Column(db.Boolean, default=False)
    status = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<Todo id={self.id} content={self.content}>'
