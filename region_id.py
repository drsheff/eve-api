import aiohttp
import asyncio
from ins_id import insert_id


async def fetch(session, url):
    async with session.get(url) as response:
        ids = []
        for i in range(1, int(response.headers['X-Pages']), 1):
            params = {'page': i}
            async with session.get(url, params=params) as resp:
                for x in (await resp.json()):
                    ids.append(x)
            insert_id(ids, i)

async def main():
    async with aiohttp.ClientSession() as session:
        await fetch(session, 'https://esi.evetech.net/latest/markets/10000002/types/?datasource=tranquility')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
