import aiohttp
import asyncio
import region_id

ids = region_id.id()
print(type(ids))


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'https://esi.evetech.net/latest/markets/10000002/history/?datasource=tranquility&type_id=i')
        print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
