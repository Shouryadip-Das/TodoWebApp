from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# In-memory task storage (use a database in production)
tasks = []


@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)


@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        priority = request.form['priority']

        task = {
            'id': len(tasks) + 1,
            'title': title,
            'description': description,
            'status': status,
            'due_date': due_date,
            'priority': priority
        }
        tasks.append(task)
        return redirect(url_for('index'))

    return render_template('create_task.html')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        return "Task not found", 404

    if request.method == 'POST':
        task['title'] = request.form['title']
        task['description'] = request.form['description']
        task['status'] = request.form['status']
        task['due_date'] = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        task['priority'] = request.form['priority']
        return redirect(url_for('index'))

    return render_template('edit_task.html', task=task)


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
