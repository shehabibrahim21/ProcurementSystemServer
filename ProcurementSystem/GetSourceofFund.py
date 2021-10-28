
# coding: utf-8

# In[7]:

from config import config
import psycopg2
import re
def get_costcenters():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT description FROM public."PPMP_sourceoffund"''')
    

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst1.append((row[0],row[0]))
        row = cur.fetchone()
    cur.close()
    
    return lst1
 


# In[8]:


get_costcenters()

