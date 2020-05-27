import aiohttp
import asyncio
import itertools
from datetime import datetime
from select_from_tid_name import select_from_tid_name
from ins_in_market_history import ins_in_market_history
from max_date_SQL import last_date
from check_id import check_id


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
            last_day_add = last_date(i)
            async with session.get(url, params=params) as response:
                if response.content_length == 2:
                    print('id ' + str(i) + ' - Return empty list')
                    emp += 1
                else:
                    if response.status == 404:
                        print(response.headers, '404', i)
                        print('"error": "Type not found!"')
                    elif response.status in [502, 503]:
                        print(response.headers, '502', i)
                        async with session.get(url, params=params) as response:
                            print(response.headers, '502', i)
                            hst = []
                            print(i)
                            for x in (await response.json()):
                                hst.append(x)
                            ins_in_market_history(hst, i)
                    else:
                        # print(response.headers, 'other', i)
                        if response.headers['Content-type'] == 'text/html':
                            print(response.headers)
                        # print(response.headers, '200', i)
                        hst = []
                        print(i)
                        r = await response.json()
                        # Последняя дата в полученном массиве
                        ld_r = datetime.strptime(r[-1]['date'], '%Y-%m-%d').date()
                        ld_db = last_day_add
                        if ld_db is None:
                            continue
                        le = [i for i, x in enumerate(r) if str(ld_db) in x['date']][0]
                        print(r[le]['date'])
                        if le < r.__len__():
                            print(r[le])
                            hst.append(r[le])
                            le += 1
                        elif le > r.__len__():
                            pass
                        ins_in_market_history(hst, i)

                        # for x in await response.json():
                        #     if datetime.strptime(x[-1]['date'], '%Y-%m-%d').date() < last_day_add:
                        #         hst.append(x)
                        #     ins_in_market_history(hst, i)
            check_id(i)
        offset += 500


async def main():
    async with aiohttp.ClientSession() as session:
        await fetch(session, 'https://esi.evetech.net/latest/markets/10000002/history/?datasource=tranquility')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
