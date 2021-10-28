
# coding: utf-8

# In[7]:

from config import config
import psycopg2
import re
def get_order_details(id_):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute(''' SELECT item_description_id_id,price_id,first_quantity,second_quantity, third_quantity, fourth_quantity 
    FROM public."PPMP_orderdetails" WHERE  id = %s''',(str(id_),))
    

    row = cur.fetchone()
#     lst1 = []
#     lst2 = []
    while row is not None:
        return list(row)
        row = cur.fetchone()
    cur.close()
#     lst2 = [word.strip() for word in lst2 if word != 'None']
#     return "   "./join(lst2)


# In[9]:


def get_price_details(id_):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute(''' SELECT price,unit
    FROM public."PPMP_prices" WHERE  id = %s''',(str(id_),))
    

    row = cur.fetchone()
#     lst1 = []
#     lst2 = []
    while row is not None:
        return list(row)
        row = cur.fetchone()
    cur.close()    


# In[17]:


import psycopg2
import re
def get_itemdescriptions(id_):
    conn = psycopg2.connect(host="localhost",database="hr_database", user="postgres", password="Bankai21")
    cur = conn.cursor()
    
    cur.execute('''SELECT general_name, specifics1,specifics2,specifics3,specifics4,specifics5 FROM public."PPMP_itemdescription"
    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id where 
    public."PPMP_itemdescription".id = %s''',(str(id_),))
    

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
#         lst2.extend(list((row[0],row[1],row[2],row[3],row[4])))
        return list(row)
        row = cur.fetchone()
    cur.close()
#     lst2 = [word.strip() for word in lst2 if word != 'None']
#     return "   ".join(lst2)


# In[27]:


def get_details(num):
    final_lst = []
    lst1 = get_order_details(num)
    lst3 = get_itemdescriptions(lst1[0])
    final_lst.extend(lst3)
    lst2 = get_price_details(lst1[1])
    final_lst.extend(lst2)
    final_lst.extend(lst1[2:])

    
    return final_lst
