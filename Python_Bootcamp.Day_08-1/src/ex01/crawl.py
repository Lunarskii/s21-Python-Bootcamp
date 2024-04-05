import sys
import asyncio
import service


async def main(urls):
    result = await service.post('http://localhost:8888/api/v1/tasks/', True, json=urls)
    print(result)
    while True:
        new_result = await service.get(f'http://localhost:8888/api/v1/tasks/{result["id"]}', True)
        if new_result.get('status', 0) == 'ready':
            [print(f'{url}: {new_result["results"][i]}') for i, url in enumerate(urls)]
            break
        await asyncio.sleep(1)


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        asyncio.run(main(args[1:]))
