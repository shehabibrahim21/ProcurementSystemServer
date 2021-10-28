from config import config
import psycopg2
import re
def get_year():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT DISTINCT(year) FROM public."PPMP_ppmp"''')
    

    row = cur.fetchone()
    lst1 = []
    while row is not None:
        lst1.append((str(row[0]).lower(),str(row[0])))
#         return row[0]
        row = cur.fetchone()
    cur.close()
    
    return lst1

