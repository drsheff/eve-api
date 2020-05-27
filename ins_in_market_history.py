from datetime import datetime

import psycopg2
from config import config


def ins_in_market_history(hst, i):
    """ select multiple ids from the vendors table  """
    sql = """ insert into public.market_history(average, date, highest, lowest, order_count, volume, nameid) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (average, date, highest, lowest, order_count, volume) 
                DO NOTHING;"""
    conn = None

    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        # cur.execute(sql)
        # print(hst)
        for x in hst:
            c = datetime.strptime(x['date'], '%Y-%m-%d').date()

            cur.executemany(sql, ((x['average'], datetime.strptime(x['date'], '%Y-%m-%d').date(), x['highest'],
                                x['lowest'], x['order_count'], x['volume'], i), ))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
