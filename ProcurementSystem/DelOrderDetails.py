from config import config
import psycopg2
import re

def delete_oder_details(id_):
    
    conn = None
    rows_deleted = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
   
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute('DELETE FROM public."PPMP_orderdetails" WHERE public."PPMP_orderdetails".id = %s', (id_,))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#     return rows_deleted

