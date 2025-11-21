from flask import Flask, render_template, request, redirect, url_for

# Flask 애플리케이션 생성
app = Flask(__name__)

# 임시 할 일 목록 (데이터베이스 역할)
# 서버가 재시작되면 데이터는 초기화됩니다.
todos = [
    {'id': 1, 'task': 'Flask 서버 기본 설정', 'done': True},
    {'id': 2, 'task': 'HTML 템플릿 작성 및 연결', 'done': False},
    {'id': 3, 'task': 'CRUD 기능 구현 확인', 'done': False}
]
next_id = 4 # 새로운 항목에 부여할 다음 ID

# 홈 페이지 - 할 일 목록 표시 (Read)
@app.route('/')
def index():
    # 'index.html' 템플릿을 렌더링하고 todos 리스트를 전달
    return render_template('index.html', todos=todos)

# 새 할 일 추가 (Create)
@app.route('/add', methods=['POST'])
def add_todo():
    global next_id
    # 폼(form)에서 'task' 이름으로 넘어온 데이터를 가져옴
    task = request.form.get('task') 
    if task:
        new_todo = {'id': next_id, 'task': task, 'done': False}
        todos.append(new_todo)
        next_id += 1
    # 처리 후 메인 페이지로 리다이렉트
    return redirect(url_for('index'))

# 할 일 완료 상태 토글 (Update)
@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            # 상태 반전
            todo['done'] = not todo['done']
            break
    return redirect(url_for('index'))

# 할 일 삭제 (Delete)
@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    global todos
    # 리스트 컴프리헨션을 사용하여 해당 ID를 가진 항목을 제외 (삭제)
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return redirect(url_for('index'))

# Flask 애플리케이션 실행
if __name__ == '__main__':
    # 디버그 모드를 켜서 코드 변경 시 자동 재시작
    app.run(debug=True)