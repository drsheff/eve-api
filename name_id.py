import aiohttp
import asyncio
from ins_in_name_id import ins_in_name_id
from select_from_tid_name import select_from_tid_name


async def fetch(session, url):
    limit = 1000
    offset = 0

    while True:
        k = select_from_tid_name(limit, offset)
        if k == 'The End of table':
            return print(k)
        else:
            async with session.post(url, data=str(k)) as resp:
                while resp.status not in [200, 204]:
                    print('Errr', resp.status)
                    raise Exception('Something going wrong')
                else:
                    offset += 1000
                js = (await resp.json())
                ins_in_name_id(js)


async def main():
    async with aiohttp.ClientSession() as session:
        await fetch(session, 'https://esi.evetech.net/latest/universe/names/?datasource=tranquility')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
