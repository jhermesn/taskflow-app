from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task List API")

_tasks: dict[int, dict] = {}
_next_id = 1

_TASK_NOT_FOUND = "Task not found"
_404 = {404: {"description": _TASK_NOT_FOUND}}


class TaskIn(BaseModel):
    title: str
    done: bool = False


class TaskPatch(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return list(_tasks.values())


@app.post("/tasks", status_code=201)
def create_task(body: TaskIn):
    global _next_id
    task = {"id": _next_id, **body.model_dump()}
    _tasks[_next_id] = task
    _next_id += 1
    return task


@app.get("/tasks/{task_id}", responses=_404)
def get_task(task_id: int):
    if task_id not in _tasks:
        raise HTTPException(404, _TASK_NOT_FOUND)
    return _tasks[task_id]


@app.patch("/tasks/{task_id}", responses=_404)
def update_task(task_id: int, body: TaskPatch):
    if task_id not in _tasks:
        raise HTTPException(404, _TASK_NOT_FOUND)
    _tasks[task_id].update(body.model_dump(exclude_unset=True))
    return _tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=204, responses=_404)
def delete_task(task_id: int):
    if task_id not in _tasks:
        raise HTTPException(404, _TASK_NOT_FOUND)
    del _tasks[task_id]
