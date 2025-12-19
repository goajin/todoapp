from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# 임시 저장용 리스트
todos = []
next_id = 1

@app.route('/')
def index():
    today = datetime.now().date()
    # D-Day 계산 로직
    for todo in todos:
        if todo['due_date'] and todo['due_date'] != "기한 없음":
            try:
                due = datetime.strptime(todo['due_date'], '%Y-%m-%d').date()
                diff = (due - today).days
                if diff == 0:
                    todo['d_day'] = "D-Day"
                elif diff > 0:
                    todo['d_day'] = f"D-{diff}"
                else:
                    todo['d_day'] = f"D+{-diff} (지남)"
            except:
                todo['d_day'] = None
        else:
            todo['d_day'] = None
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    global next_id
    task = request.form.get('task')
    due_date = request.form.get('due_date')
    if task:
        new_todo = {
            'id': next_id,
            'task': task,
            'done': False,
            'due_date': due_date if due_date else "기한 없음"
        }
        todos.append(new_todo)
        next_id += 1
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['done'] = not todo['done']
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)