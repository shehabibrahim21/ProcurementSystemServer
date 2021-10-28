import psycopg2
import re
from config import config

def get_user_id(username):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT id FROM public."auth_user" where username = %s''', (str(username),))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        return row[0]
        row = cur.fetchone()
    cur.close()


def get_cc_id(id_):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT costcenter_id FROM public."PPMP_costcenter_user" where user_id = %s''', (id_,))

    row = cur.fetchone()
    lst1 = []
    while row is not None:
        #         return row

        lst1.append(row[0])
        row = cur.fetchone()
    cur.close()
    return lst1


def get_cost_centers(username):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    lst_cc = get_cc_id(get_user_id(username))
    cur.execute('''SELECT code, name FROM public."PPMP_costcenter"  where id in %s''', (tuple(lst_cc),))

    row = cur.fetchone()
    lst1 = []
    while row is not None:
        #         str1 = ",".join(list(row))
        #         str1 = re.sub(' +', ' ', str1)
        lst1.append([row[0], row[1]])
        row = cur.fetchone()
    cur.close()
    return lst1