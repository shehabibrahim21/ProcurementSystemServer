#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import re
from config import config

def get_cc():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT name FROM public."PPMP_costcenter"''')

    row = cur.fetchone()
    lst1 = []
    str_ = ""
    while row is not None:
        lst1.append((row[0], row[0]))
        row = cur.fetchone()
    cur.close()

    return lst1

