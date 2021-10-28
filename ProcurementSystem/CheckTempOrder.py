

import psycopg2
import re
from config import config

def check_temp_order():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT * FROM public."PPMP_temporderdetails" WHERE public."PPMP_temporderdetails".approved = %s''',
                ('Pending',))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    dct = {}
    while row is not None:
        lst1.append(row)
        row = cur.fetchone()
    cur.close()
    if lst1:
        return True
    else:
        return False




def get_temp_order():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT  public."PPMP_temporderdetails".id,
                public."PPMP_temporderdetails".general_name, public."PPMP_temporderdetails".specifics1,
                public."PPMP_temporderdetails".specifics2,public."PPMP_temporderdetails".specifics3,
                public."PPMP_temporderdetails".specifics4,public."PPMP_temporderdetails".specifics5,
                public."PPMP_temporderdetails".date, public."PPMP_costcenter".name
                FROM public."PPMP_temporderdetails"
                JOIN public."PPMP_ppmp" ON public."PPMP_temporderdetails".ppmp_id_id = public."PPMP_ppmp".id
                JOIN public."PPMP_costcenter" ON public."PPMP_ppmp".cc_num_id = public."PPMP_costcenter".id

                WHERE public."PPMP_temporderdetails".approved = %s''', ('Pending',))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    dct = {}
    while row is not None:
        lst1.append(list(row))
        row = cur.fetchone()
    cur.close()

    [lst.insert(1, re.sub('  +', ' ', ' '.join(lst[1:7]).replace('None', ''))) for lst in lst1]
    return lst1


def get_temp_specs():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT  public."PPMP_temporderdetails".id, public."PPMP_temporderdetails".specifics1,
                public."PPMP_temporderdetails".specifics2,public."PPMP_temporderdetails".specifics3,
                public."PPMP_temporderdetails".specifics4,public."PPMP_temporderdetails".specifics5
                FROM public."PPMP_temporderdetails"
                JOIN public."PPMP_ppmp" ON public."PPMP_temporderdetails".ppmp_id_id = public."PPMP_ppmp".id
                JOIN public."PPMP_costcenter" ON public."PPMP_ppmp".cc_num_id = public."PPMP_costcenter".id

                    ''')

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    dct = {}
    while row is not None:
        lst1.append(list(row))
        row = cur.fetchone()
    cur.close()

    return lst1

def get_temp_order_details(id_):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # year = get_year()[0]

    cur.execute('''SELECT public."PPMP_temporderdetails".client_suggested_price,
   public."PPMP_temporderdetails".client_suggested_unit,
   public."PPMP_temporderdetails".first_quarter_suggested,
   public."PPMP_temporderdetails".second_quarter_suggested,
   public."PPMP_temporderdetails".third_quarter_suggested,
   public."PPMP_temporderdetails".fourth_quarter_suggested,
   public."PPMP_temporderdetails".date

    FROM public."PPMP_temporderdetails" 
    where public."PPMP_temporderdetails".id = %s ''', (id_,))

    row = cur.fetchone()
    lst1 = []
    while row is not None:

        return list(row)
        row = cur.fetchone()
    cur.close()