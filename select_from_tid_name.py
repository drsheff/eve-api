import psycopg2
from config import config


def select_from_tid_name(limit, offset):
    """ select multiple ids from the vendors table  """
    sql = """ SELECT type_id FROM public.tid limit %s offset %s """ % (limit, offset)
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
        while cur.rowcount != 0:
            print(limit, offset)
            cur.execute(sql)
            s = cur.fetchall()
            if s.__len__() == 0:
                return ('The End of table')
            # print(s)
            list_id = [c for i in s for c in i]
            # l = list_id.__len__()
            # if l == 0:
            #     return ('The End of list')
            # else:
            #     print(list_id)
            return (list_id)

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
