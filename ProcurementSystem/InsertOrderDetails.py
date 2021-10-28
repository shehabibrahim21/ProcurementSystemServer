
# coding: utf-8

# In[9]:
from config import config
from datetime import datetime
import psycopg2
def get_last_value():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT MAX(id) FROM public."PPMP_orderdetails"''')
    

    row = cur.fetchone()
    while row is not None:
        return row[0]
        row = cur.fetchone()
  
    cur.close()


# In[13]:

def get_price_detail(item_description_id):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(''' SELECT public."PPMP_prices".id

    FROM public."PPMP_prices" 
    
    
    WHERE public."PPMP_prices".item_id_id = %s 

    ''', (str(item_description_id),))


    row = cur.fetchone()
    lst1 = []
    lst2 = []
    lst3 = []
    while row is not None:
        # lst2.append(list(row))
        return row[0]
        row = cur.fetchone()
    # return lst2




def insert_order_details(item_description_id_id, ppmp_id_id, price_id, first_quantity, second_quantiy, third_quantity,
                         fourth_quantity):
    print("sulod sa insert")
    dateTimeObj = datetime.now()
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    id_ = get_last_value()
    if id_ is None:
        id_ = 0
    else:
        id_ = int(id_) + 1

    sql = """INSERT INTO public."PPMP_orderdetails"(id,item_description_id_id,
        ppmp_id_id, price_id,first_quantity, second_quantity,third_quantity, fourth_quantity,date,app_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

    try:
        cur.execute(sql, (
        id_, item_description_id_id, ppmp_id_id, price_id, first_quantity, second_quantiy, third_quantity,
        fourth_quantity,str(dateTimeObj).split(' ')[0],""))
        print("success")
        #             cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)