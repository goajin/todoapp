from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 템플릿, static 연결
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 임시 데이터 저장
todo_list = []


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todo_list})


@app.post("/add")
async def add_todo(task: str = Form(...)):
    todo_list.append(task)
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{item_id}")
async def delete_todo(item_id: int):
    if 0 <= item_id < len(todo_list):
        del todo_list[item_id]
    return RedirectResponse("/", status_code=303)
