
# coding: utf-8

# In[4]:

from config import config
import psycopg2
import re
def get_gen(id_):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT general_name FROM public."PPMP_item" where category_id_id = %s''',(str(id_),))
    

    row = cur.fetchone()
    lst1 = []
    str_ = ""
    while row is not None:
        str_ = row[0] + "   " + str_
#         return row[0]
        row = cur.fetchone()
    cur.close()
    
    return str_


# In[24]:


import psycopg2
import re
def get_spec(id_):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT specifics1,specifics2,specifics3,specifics4,specifics5 FROM public."PPMP_itemdescription"
    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id where 
    public."PPMP_item".category_id_id = %s''',(str(id_),))
    

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst2.extend(list((row[0],row[1],row[2],row[3],row[4])))
#         return row[0]
        row = cur.fetchone()
    cur.close()
    lst2 = [word.strip() for word in lst2 if word != 'None']
    return "   ".join(lst2)


def get_spec1():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT specifics1,specifics2,specifics3,specifics4,specifics5 FROM public."PPMP_itemdescription"
    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id ''')

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst2.extend(list((row[0], row[1], row[2], row[3], row[4])))
        #         return row[0]
        row = cur.fetchone()
    cur.close()
    lst2 = [word.strip() for word in lst2 if word != 'None']
    return "   ".join(lst2)
