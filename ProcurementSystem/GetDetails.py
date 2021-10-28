
# coding: utf-8

# In[10]:
import psycopg2
from config import config
def get_generics():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT DISTINCT(genericname) FROM public."Item"''')
    

    row = cur.fetchone()
    lst =[]
    while row is not None:
        lst.append(row[0])
        row = cur.fetchone()
    cur.close()
    return lst


# In[25]:


def get_details(clean, lst_items):
    
    lst_generics = get_generics()
    
    generic_name = ''
    for generic in lst_generics:
        
        if generic in clean:
            generic_name = generic
            break
    
    clean = clean.replace(generic,'')
    
    lst_filtered = []
    for value in lst_items:
        if value[1] == generic_name:
            lst_filtered.append(value)
            
    lst_clean = clean.split(' ')
    lst_clean = [word for word in lst_clean if word]
    lst_clean.sort()
    
    for i in lst_filtered:
        
        lst_itm = i[2].split(', ')
        lst_itm = [word.split() for word in lst_itm]
        lst_itm = [item for sublist in lst_itm for item in sublist]
        # print(lst_itm)
        lst_itm.sort()
        # print(lst_clean, lst_itm)
        if lst_itm == lst_clean:
            itc = i[0]
            gnrc = i[1]
            unt = i[3]
            prc = i[4]
            acc = i[5]
            break
    
    try:
        return itc,gnrc,unt,prc,acc
    except:
        return False        

