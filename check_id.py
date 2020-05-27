import psycopg2
from config import config


def check_id(i):
    check = 'Done'
    """ select multiple ids from the vendors table  """
    sql = """ insert into public.id_done(id, "check") 
                VALUES (%s, %s) ON CONFLICT (id) 
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
        cur.executemany(sql, ((i, check),))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
