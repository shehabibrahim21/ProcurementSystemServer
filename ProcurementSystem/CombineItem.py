#!/usr/bin/env python
# coding: utf-8

# In[45]:


import psycopg2
import re
from config import config
def get_transactions(ppmp_id, item_id):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # year = get_year()[0]

    cur.execute('''SELECT * FROM public."PPMP_orderdetails" where "PPMP_orderdetails".ppmp_id_id = %s and "PPMP_orderdetails".item_description_id_id = %s''', (ppmp_id,item_id))

    row = cur.fetchone()
    lst1 = []
    while row is not None:
        lst1.append(list(row))
#         return row[0]
        row = cur.fetchone()
    cur.close()
    return lst1


# In[46]:


def combine(lst):

    date = lst[-1][-1]

    fq = 0
    sq = 0
    tq = 0
    frq = 0
    dct = {}
    #     lst.reverse()
    for i in lst:
        key = str(i[1]) + " " + i[-1].split('-')[0]
        if key not in dct:
            dct[key] = i
        else:
            lst1 = dct[key][4:8]
            lst2 = i[4:8]
            lst3 = [sum(x) for x in zip(lst1, lst2)]
    #         print(lst3)
            lst4 = dct[key]
            lst4[4:8] = lst3

            dct[key] = lst4
        
        
    return dct


# In[ ]:


def delete_order_details(lst,ppmp_id):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    sql = """DELETE FROM public."PPMP_orderdetails" WHERE public."PPMP_orderdetails".item_description_id_id = %s
    and public."PPMP_orderdetails".ppmp_id_id = %s;"""
    cur.execute(sql, (lst[1],ppmp_id))
    conn.commit()
    cur.close()

# In[47]:


def insert_order_details(ppmp_id,item_id):
    dct = combine(get_transactions(ppmp_id,item_id))

    for key in dct:

        id_ = int(dct[key][0]) + 1
        lst = dct[key]
        delete_order_details(lst, ppmp_id)
        conn = psycopg2.connect(host="localhost", database="hr_database", user="postgres", password="Bankai21")
        cur = conn.cursor()
        sql = """INSERT INTO public."PPMP_orderdetails"(id, item_description_id_id,ppmp_id_id,price_id,first_quantity,second_quantity,third_quantity, fourth_quantity,date) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        try:
            cur.execute(sql, (
                id_, lst[1], lst[2], lst[3], lst[4], lst[5], lst[6], lst[7], lst[8]))
            #             cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

