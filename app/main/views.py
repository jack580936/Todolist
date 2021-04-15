from datetime import datetime

from flask import jsonify, request, render_template, redirect
from .. import db
from . import main
from app.models import Todo


@main.route("/create", methods=['GET'])
@main.route("/create/<record_name>", methods=['GET'])
def create(record_name="First_Record"):
    new_record = Todo()
    new_record.content = record_name
    db.session.add(new_record)
    db.session.commit()
    # print(request.method)
    return jsonify({"result": True})


@main.route("/read", methods=['GET'])
def read():
    all_results = Todo.query.order_by(Todo.create_datetime.desc()).all()
    result = []
    for item in all_results:
        result.append({"name": item.content, "create_time": item.create_datetime,
                       "done": item.done, "task_status": item.status})
    return jsonify(result)


@main.route("/read_by_status", methods=['GET'])
def read_by_status():
    all_results = Todo.query.order_by(Todo.status.desc()).all()
    result = []
    for item in all_results:
        result.append({"name": item.content, "create_time": item.create_datetime,
                       "done": item.done, "task_status": item.status})
    return jsonify(result)


@main.route("/search/<search_name>", methods=['GET'])
@main.route("/search", methods=['POST'])
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


@main.route("/update/<record_id>", methods=['GET', 'POST'])
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


@main.route("/delete/<record_id>", methods=['GET'])
def delete(record_id):
    record = Todo.query.get_or_404(record_id)
    try:
        if record is not None:
            db.session.delete(record)
            db.session.commit()
            return redirect('/')
    except:
        return 'There was an error while deleting that task'


@main.route("/done/<int:record_id>", methods=['POST', 'GET'])
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


@main.route("/", methods=['POST', 'GET'])
@main.route("/<user>", methods=['GET'])
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
        return render_template("index.html", tasks=tasks, user=user, search=search_results,
                               current_time=datetime.utcnow())
