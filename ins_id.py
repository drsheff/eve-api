import psycopg2
from config import config


def insert_id(ids, i):
    """ insert multiple vendors into the vendors table  """
    sql = """ INSERT INTO public.tid (type_id) VALUES (%s) ON CONFLICT (type_id) DO NOTHING """
    """ truncate table with reset ai"""
    check = 'False'
    sql1 = """ INSERT INTO public.id_done (id, "check") VALUES (%s, %s) ON CONFLICT (id) DO NOTHING """
    trun_typeid = """ TRUNCATE TABLE public.tid RESTART IDENTITY CASCADE; """
    trun_nameid = """ TRUNCATE TABLE public.name_id RESTART IDENTITY CASCADE; """
    trun_iddone = """ TRUNCATE TABLE public.id_done RESTART IDENTITY CASCADE; """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        if i == 1:
            cur.execute(trun_typeid)
            cur.execute(trun_nameid)
            cur.execute(trun_iddone)
            conn.commit()
            cur.executemany(sql, [[row] for row in ids])
            for c in ids:
                cur.executemany(sql1, ((c, check),))
        else:
            cur.executemany(sql, [[row] for row in ids])
            for c in ids:
                cur.executemany(sql1, ((c, check),))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return
