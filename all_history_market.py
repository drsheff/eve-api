import aiohttp
import asyncio
from select_from_tid_name import select_from_tid_name
from ins_in_market_history import ins_in_market_history


async def fetch(session, url):
    limit = 500
    offset = 0
    err = 0
    emp = 0
    while True:
        k = select_from_tid_name(limit, offset)
        if k == 'The End of table':
            print('Error = ' + str(err), 'Empty list = ' + str(emp))
            return print('Job Done')
        for i in k:
            params = {'type_id': i}
            async with session.get(url, params=params) as response:
                h = response.headers['Etag']
                if response.content_length == 2:
                    print('id ' + str(i) + ' - Return empty list')
                    emp += 1
                else:
                    if response.status not in [200, 204, 404]:
                        print('Errr', response.status)
                        print(response.reason)
                        raise Exception('Something going wrong')
                    elif response.status in [502, 503]:
                        async with session.get(url, params=params) as response:
                            hst = []
                            print(i)
                            for x in (await response.json()):
                                hst.append(x)
                            ins_in_market_history(hst, i)
                    else:
                        hst = []
                        print(i)
                        for x in (await response.json()):
                            hst.append(x)
                        ins_in_market_history(hst, i)
        offset += 500


async def main():
    async with aiohttp.ClientSession() as session:
        await fetch(session, 'https://esi.evetech.net/latest/markets/10000002/history/?datasource=tranquility')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
