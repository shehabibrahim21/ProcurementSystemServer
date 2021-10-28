
# coding: utf-8

# In[5]:


import psycopg2
import re
from config import config


def get_categories():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute('''SELECT name
                FROM public."PPMP_category" ''')
    

    row = cur.fetchone()
    str_ = ""
    while row is not None:
#         str1 = ",".join(list(row))
#         str1 = re.sub(' +', ' ', str1)
        str_ = row[0] + "   " + str_
        # lst1.append(row[0])
        row = cur.fetchone()
    cur.close()
    return str_

