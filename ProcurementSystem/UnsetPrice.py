#!/usr/bin/env python
# coding: utf-8

# In[13]:

from config import config
import psycopg2
import re
def show_unset_price():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''
    SELECT
     public."PPMP_itemdescription".id,
    public."PPMP_item".general_name, 
    public."PPMP_itemdescription".specifics1, public."PPMP_itemdescription".specifics2, public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4, public."PPMP_itemdescription".specifics5

    
    FROM public."PPMP_itemdescription" 
    
    
    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id
    
    WHERE public."PPMP_itemdescription".id not in
    
    (SELECT public."PPMP_prices".item_id_id from public."PPMP_prices")
    
    ''')
    

    row = cur.fetchone()
    lst2 = []
    lst1 = []
    lst3 = []
    while row is not None:
        lst2.append(list(row))
        row = cur.fetchone()
    cur.close()
    for i in lst2:
        str_ = " ".join(i[1:])
        str_ = str_.replace("None", "")
        str_ = re.sub(' +', ' ', str_)
        str_ = str_.strip()
        lst1.append([i[0], str_])
        lst3.append(str_)
    cur.close()
    return lst1






