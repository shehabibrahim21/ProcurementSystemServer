from config import config
import psycopg2
def retrieve_item():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT * FROM public."Item"''')
    

    row = cur.fetchone()
    lst =[]
    while row is not None:
        lst.append(row)
        row = cur.fetchone()
    cur.close()
    return lst


# In[56]:


def retrieve_specifications(lst_specificscode):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT * FROM public."Specifications" where specificscode IN  %s''',(tuple(lst_specificscode),))

    row = cur.fetchone()
    lst =[]
    while row is not None:
        lst.append(row)
        row = cur.fetchone()
    cur.close()
    return lst


# In[ ]:


def retrieve():
    lst_items = retrieve_item()

    lst_specificscode = []
    for i in lst_items:
        lst_specificscode.append(str(i[4]))

    lst_sc = retrieve_specifications(lst_specificscode)

    final_lst = []
    for i, u in zip(lst_items, lst_sc):
        u = list(u)
        while (' ' in u):
            u.remove(' ')
        #         print(u)
        str1 = ", ".join(u[:-1])
        str1 = str1.replace('_', ' ')
        temp_lst = [i[0], i[3], str1, i[1], str(format(i[2], '.2f')), i[5]]
        final_lst.append(temp_lst)

    return final_lst