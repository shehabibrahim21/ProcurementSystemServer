import psycopg2
import re
from config import config

def get_year():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT DISTINCT(year) FROM public."PPMP_ppmp" ORDER BY year''')

    row = cur.fetchone()
    lst1 = []
    while row is not None:
        lst1.append(row[0])
        #         return row[0]
        row = cur.fetchone()
    cur.close()
    lst1.reverse()
    return lst1


def get_ppmp(cc_code, year = get_year()[0]):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # year = get_year()[0]

    cur.execute('''SELECT public."PPMP_ppmp".id,public."PPMP_costcenter".code, public."PPMP_sourceoffund".description,
    public."PPMP_ppmp".year,  public."PPMP_ppmp".type, public."PPMP_sourceoffund".code
    FROM public."PPMP_costcenter" JOIN public."PPMP_ppmp" ON  public."PPMP_costcenter".id =  public."PPMP_ppmp".cc_num_id
    JOIN public."PPMP_sourceoffund" ON public."PPMP_ppmp".sof_num_id = public."PPMP_sourceoffund".id 
    where "PPMP_costcenter".code = %s AND "PPMP_ppmp".year = %s''', (str(cc_code), year))

    row = cur.fetchone()
    lst1 = []
    while row is not None:
        lst1.append(list(row))
#         return row[0]
        row = cur.fetchone()
    cur.close()
    
    return lst1

