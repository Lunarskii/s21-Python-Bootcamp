from fastapi import FastAPI, BackgroundTasks, HTTPException
from urllib.parse import urlparse
from models import Task
import uuid
import uvicorn
import service
import asyncio
import aioredis
import argparse
import logging


app = FastAPI()
redis = aioredis.from_url("redis://localhost:6379")
args = argparse.Namespace()
logging.basicConfig(level=logging.INFO, format='%(levelname)s: \t  %(message)s')
tasks = {}


async def clear_cache(timeout: int):
    await asyncio.sleep(timeout)
    logging.info('Starting to delete the cache')
    keys = await redis.hkeys('cache')
    if keys:
        await redis.hdel('cache', *keys)
        logging.info('The cache has been cleared')
    else:
        logging.info('The cache was not found. Nothing was cleared :)')


async def collect_url_codes(task: Task, urls: list[str]):
    task.status = 'ready'
    task.results = []
    for url in urls:
        domain = urlparse(url).netloc
        cache = await redis.hget('cache', url)
        if cache:
            status_code = int(cache)
            logging.info(f'URL \'{url}\' is cached. {status_code=}')
        else:
            status_code = (await service.get(url)).status
            await redis.hset('cache', url, status_code)
            logging.info(f'URL \'{url}\' is not cached. We cache it... {status_code=}')
        counter = await redis.incr(domain)
        logging.info(f'{domain}: {counter}')
        task.results.append(status_code)
        await asyncio.sleep(1)
    tasks[task.id] = task


@app.post('/api/v1/tasks/', response_model=Task, status_code=201)
async def handle_urls(urls: list[str], background_tasks: BackgroundTasks):
    response = Task(id=uuid.uuid4(), status='running')
    background_tasks.add_task(collect_url_codes, response, urls)
    background_tasks.add_task(clear_cache, args.timeout)
    return response


@app.get('/api/v1/tasks/{task_id}', status_code=200)
async def get_task_results(task_id: str):
    task_uuid = uuid.UUID(task_id)
    if task_uuid in tasks:
        return tasks.pop(task_uuid)
    else:
        raise HTTPException(status_code=404, detail="Task not found")


async def clear_redis():
    logging.info('Redis storage has been cleared')
    await redis.flushdb()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('-c', type=bool, default=False)
    args = parser.parse_args()
    if args.c:
        asyncio.run(clear_redis())
    else:
        uvicorn.run(app=app, host="localhost", port=8888)
