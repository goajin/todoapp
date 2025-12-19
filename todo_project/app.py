from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 기존 리스트를 비우거나 아래처럼 형식을 맞춰주세요.
todos = [
    # 기존 데이터에도 due_date가 있어야 화면에 보입니다.
    {'id': 1, 'task': '새로운 기능 테스트', 'done': False, 'due_date': '2025-12-25'}
]
next_id = 2

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    global next_id
    task = request.form.get('task')
    # HTML의 name="due_date"에서 보낸 값을 가져옵니다.
    due_date = request.form.get('due_date') 
    
    if task:
        if not due_date:
            due_date = "기한 없음"
            
        new_todo = {
            'id': next_id, 
            'task': task, 
            'done': False, 
            'due_date': due_date  # 이 부분이 리스트에 저장되어야 HTML에서 보임
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
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)