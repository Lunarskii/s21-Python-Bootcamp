import aiohttp


async def post(url: str, decode: bool = False, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, **kwargs) as response:
            if decode:
                return await response.json()
            return response


async def get(url: str, decode: bool = False, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, **kwargs) as response:
            if decode:
                return await response.json()
            return response
