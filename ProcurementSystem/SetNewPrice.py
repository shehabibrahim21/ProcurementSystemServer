from config import config
import psycopg2
import re
from config import config
from datetime import datetime
def get_price(item_id):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # year = get_year()[0]

    cur.execute('''SELECT public."PPMP_prices".id

    FROM public."PPMP_prices" 
    where "PPMP_prices".item_id_id = %s ''', (str(item_id),))

    row = cur.fetchone()
    lst1 = []
    while row is not None:
        lst1.append(list(row))
        row = cur.fetchone()
    cur.close()
    conn.close()
    
    return lst1  
       


# In[2]:


def get_last_value():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute('''SELECT MAX(id) FROM public."PPMP_prices"''')

    row = cur.fetchone()
    while row is not None:
        return row[0]
        row = cur.fetchone()
  
    cur.close()
    conn.close()


# In[3]:


def set_new_price(item_id,type_,value):
    item_id = int(item_id)
    if not get_price(item_id):
        print("sulod")
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = """INSERT INTO public."PPMP_prices"(id,price,date_created,unit,item_id_id) VALUES(%s,%s,%s,%s,%s);"""

        dateTimeObj = datetime.now()

        id_ = get_last_value()
        if id_ is None:
            id_ = 0
        else:
            id_ = int(id_) + 1

        try:
            if type_ == "price":
                cur.execute(sql, (
                id_, value,str(dateTimeObj).split(' ')[0],"",item_id))
            elif type_ == "unit":
                cur.execute(sql, (
                id_, 0,str(dateTimeObj).split(' ')[0],value,item_id))                
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    else:

        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        if type_ == "price":
            try:
                value = int(value)
                sql_update_query = """Update public."PPMP_prices" set price = %s where item_id_id = %s"""
                cur.execute(sql_update_query, (value, item_id))
                conn.commit()
            
            except (Exception, psycopg2.Error) as error:
                print("Error in update operation", error)

        else:
            try:
                sql_update_query = """Update public."PPMP_prices" set unit = %s where item_id_id = %s"""
                cur.execute(sql_update_query, (value, item_id))
                conn.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error in update operation", error)

      

            
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")


def edit_order_details(id_, value, type_):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    if type_ == "item_description":
        try:
            value = int(value)
            sql_update_query = """Update public."PPMP_orderdetails" set item_description_id_id = %s where id = %s"""
            cur.execute(sql_update_query, (value, id_))
            conn.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)

    elif type_ == "fq_qty":
        try:
            sql_update_query = """Update public."PPMP_orderdetails" set first_quantity = %s where id = %s"""
            cur.execute(sql_update_query, (value, id_))
            conn.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)

    elif type_ == "sq_qty":
        try:
            sql_update_query = """Update public."PPMP_orderdetails" set second_quantity = %s where id = %s"""
            cur.execute(sql_update_query, (value, id_))
            conn.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)

    elif type_ == "tq_qty":
        try:
            sql_update_query = """Update public."PPMP_orderdetails" set third_quantity = %s where id = %s"""
            cur.execute(sql_update_query, (value, id_))
            conn.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)

    elif type_ == "frq_qty":
        try:
            sql_update_query = """Update public."PPMP_orderdetails" set fourth_quantity = %s where id = %s"""
            cur.execute(sql_update_query, (value, id_))
            conn.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)

    cur.close()
    conn.close()
    print("PostgreSQL connection is closed")


