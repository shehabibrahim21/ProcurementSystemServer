
# coding: utf-8

# In[2]:


import psycopg2
import re
from config import config
def get_cat_code(name):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT id FROM public."PPMP_category" where name = %s''',(str(name),))
    

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        return row[0]
        row = cur.fetchone()
    cur.close()

