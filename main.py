from datetime import datetime

from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JSON_SORT_KEYS'] = False  # json排序
app.config['JSON_AS_ASCII'] = False  # 顯示中文 而不是ascii


class Todo(db.Model):
    __tablename__ = "todo_list"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    create_datetime = db.Column(db.DateTime, default=datetime.now)
    done = db.Column(db.Boolean, default=False)
    status = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<Todo id={self.id} content={self.content}>'


'''
def __init__(self, content):
    self.content = content
    self.done = False


def __repr__(self):
  return '<content %r>' % self.id
'''

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/create", methods=['GET'])
@app.route("/create/<record_name>", methods=['GET'])
def create(record_name="First_Record"):
    new_record = Todo()
    new_record.content = record_name
    db.session.add(new_record)
    db.session.commit()
    # print(request.method)
    return jsonify({"result": True})


@app.route("/read", methods=['GET'])
def read():
    all_results = Todo.query.order_by(Todo.create_datetime.desc()).all()
    result = []
    for item in all_results:
        result.append({"name": item.content, "create_time": item.create_datetime,
                       "done": item.done, "task_status": item.status})
    return jsonify(result)


@app.route("/read_by_status", methods=['GET'])
def read_by_status():
    all_results = Todo.query.order_by(Todo.status.desc()).all()
    result = []
    for item in all_results:
        result.append({"name": item.content, "create_time": item.create_datetime,
                       "done": item.done, "task_status": item.status})
    return jsonify(result)


@app.route("/search/<search_name>", methods=['GET'])
@app.route("/search", methods=['POST'])
def search(search_name=None):
    all_results = Todo.query.order_by(Todo.create_datetime).all()
    search_results = []
    tasks = Todo.query.order_by(Todo.status.desc()).all()
    if request.method == 'POST':
        task_content = request.form['target']
        search_results = Todo.query.filter(Todo.content.like('%' + task_content + '%')).order_by(Todo.status.desc())
        return render_template("index.html", tasks=tasks, search_results=search_results, current_time=datetime.utcnow())
    else:
        for item in all_results:
            if search_name in item.content:
                search_results.append({"name": item.content, "create_time": item.create_datetime,
                                       "done": item.done, "task_status": item.status})
        if search_results:
            return jsonify(search_results)
        else:
            return jsonify("NOT FOUND")


@app.route("/update/<record_id>", methods=['GET', 'POST'])
def update(record_id):
    record = Todo.query.get_or_404(record_id)
    print(record)
    if request.method == 'POST':
        record.content = request.form['content']
        record.status = request.form['status']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('update.html', task=record)


@app.route("/delete/<record_id>", methods=['GET'])
def delete(record_id):
    record = Todo.query.get_or_404(record_id)
    try:
        if record is not None:
            db.session.delete(record)
            db.session.commit()
            return redirect('/')
    except:
        return 'There was an error while deleting that task'


@app.route("/done/<int:record_id>", methods=['POST', 'GET'])
def done(record_id):
    task = Todo.query.get(record_id)
    if not task:
        return redirect('/')
    if task.done is True:
        task.done = False
    else:
        task.done = True
    db.session.commit()
    return redirect('/')


@app.route("/", methods=['POST', 'GET'])
@app.route("/<user>", methods=['GET'])
def index(user=None, search_results=None):
    if request.method == 'POST':
        task_content = request.form['content']
        task_status = request.form['status']
        new_task = Todo(content=task_content, status=task_status)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding the task'

    else:
        tasks = Todo.query.order_by(Todo.status.desc()).all()
        return render_template("index.html", tasks=tasks, user=user, search=search_results, current_time=datetime.utcnow())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5353, debug=True)
