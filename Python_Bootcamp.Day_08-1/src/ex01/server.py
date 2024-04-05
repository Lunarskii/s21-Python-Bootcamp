from fastapi import FastAPI, BackgroundTasks, HTTPException
from models import Task
import uuid
import uvicorn
import service
import asyncio


app = FastAPI()
tasks = {}


async def collect_url_codes(task: Task, urls: list[str]):
    task.status = 'ready'
    task.results = [(await service.get(url)).status for url in urls]
    await asyncio.sleep(3)
    tasks[task.id] = task


@app.post('/api/v1/tasks/', response_model=Task, status_code=201)
async def handle_urls(urls: list[str], background_tasks: BackgroundTasks):
    response = Task(id=uuid.uuid4(), status='running')
    background_tasks.add_task(collect_url_codes, response, urls)
    return response


@app.get('/api/v1/tasks/{task_id}', status_code=200)
async def get_task_results(task_id: str):
    task_uuid = uuid.UUID(task_id)
    if task_uuid in tasks:
        return tasks.pop(task_uuid)
    else:
        raise HTTPException(status_code=404, detail="Task not found")


if __name__ == '__main__':
    uvicorn.run(app=app, host="localhost", port=8888)
