from config import config
from datetime import datetime
import random
import psycopg2
def get_last_value():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT MAX(id) FROM public."PPMP_temporderdetails"''')
    

    row = cur.fetchone()
    while row is not None:
        return row[0]
        row = cur.fetchone()
  
    cur.close()


# In[ ]:


import psycopg2

def insert_temp_order_details(ppmp_id_id, specifics1,specifics2,specifics3,specifics4,specifics5,gen_name,client_suggested_price,client_suggested_unit,first_quarter_suggested,
                              second_quarter_suggested,third_quarter_suggested,fourth_quarter_suggested):
        dateTimeObj = datetime.now()
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        id_ = get_last_value()
        if id_ is None:
            id_ = 0
        else:
            id_ = int(id_) + 1
            
            
        sql = """INSERT INTO public."PPMP_temporderdetails"(id,ppmp_id_id,date,specifics1,specifics2,specifics3,
        specifics4,specifics5,general_name,suggested_price,comments,suggested_specs,approved,client_suggested_unit,client_suggested_price,first_quarter_suggested,
        second_quarter_suggested,third_quarter_suggested,fourth_quarter_suggested) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        
        try:
            cur.execute(sql, (id_, ppmp_id_id,str(dateTimeObj).split(' ')[0],specifics1,specifics2,specifics3,specifics4,specifics5,gen_name,0.0,"","","Pending",client_suggested_unit,client_suggested_price,
                              first_quarter_suggested,second_quarter_suggested,third_quarter_suggested,fourth_quarter_suggested))
#             cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


def update_approve(id_, approved):
    sql = """ UPDATE public."PPMP_temporderdetails"
                SET approved = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (approved, id_))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def update_specs(id_, specs):
    sql = """ UPDATE public."PPMP_temporderdetails"
                SET suggested_specs = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (specs, id_))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def update_comments(id_, comments):
    sql = """ UPDATE public."PPMP_temporderdetails"
                SET comments = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (comments, id_))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def update_price(id_, price):
    sql = """ UPDATE public."PPMP_temporderdetails"
                SET suggested_price = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (price, id_))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def yes_update(id_, price, comments, specs):
    update_price(id_, price)
    update_comments(id_, comments)
    update_specs(id_, specs)
    update_approve(id_, 'Approved')

def no_update(id_, price, comments, specs):
    update_price(id_, price)
    update_comments(id_, comments)
    update_specs(id_, specs)
    update_approve(id_, 'N')


def get_ppmp_item_id(gen_name):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # year = get_year()[0]

    cur.execute('''SELECT public."PPMP_item".id

    FROM public."PPMP_item"

    where public."PPMP_item".general_name = %s 

    ''', (gen_name,))

    row = cur.fetchone()
    lst1 = []
    while row is not None:
        return row[0]
    cur.close()


def get_last_value_itemdescription():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT MAX(id) FROM public."PPMP_itemdescription"''')

    row = cur.fetchone()
    while row is not None:
        return row[0]
        row = cur.fetchone()

    cur.close()


def get_last_value_prices():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT MAX(id) FROM public."PPMP_prices"''')

    row = cur.fetchone()
    while row is not None:
        return row[0]
        row = cur.fetchone()

    cur.close()


def get_last_value_price():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT MAX(id) FROM public."PPMP_prices"''')

    row = cur.fetchone()
    while row is not None:
        return row[0]
        row = cur.fetchone()

    cur.close()
def get_gen_specs(id_):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # year = get_year()[0]

    cur.execute('''SELECT public."PPMP_temporderdetails".general_name,
    public."PPMP_temporderdetails".specifics1,
    public."PPMP_temporderdetails".specifics2,
    public."PPMP_temporderdetails".specifics3,
    public."PPMP_temporderdetails".specifics4,
    public."PPMP_temporderdetails".specifics5

    FROM public."PPMP_temporderdetails"

    where public."PPMP_temporderdetails".id = %s 

    ''', (id_,))

    row = cur.fetchone()
    lst1 = []
    while row is not None:
        return list(row)
    cur.close()


def get_last_order_details():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT MAX(id) FROM public."PPMP_orderdetails"''')

    row = cur.fetchone()
    while row is not None:
        return row[0]
        row = cur.fetchone()

    cur.close()


def get_itemcode():
    conn = psycopg2.connect(host="localhost", database="hr_database", user="postgres", password="Bankai21")
    cur = conn.cursor()

    cur.execute('''SELECT itemcode FROM public."PPMP_itemdescription"''')

    row = cur.fetchone()
    lst_ = []
    while row is not None:
        lst_.append(row[0])
        row = cur.fetchone()
    cur.close()
    return lst_

def insert_itemdescription(temp_id, price, unit, first_quantity, second_quantity, third_quantity, fourth_quantity,
                           date,ppmp_id_id):
    lst_ = get_gen_specs(temp_id)

    print(lst_)
    gen = lst_[0]
    specifics1 = lst_[1]
    specifics2 = lst_[2]
    specifics3 = lst_[3]
    specifics4 = lst_[4]
    specifics5 = lst_[5]
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    id_ = get_last_value_itemdescription()
    if id_ is None:
        id_ = 0
    else:
        id_ = int(id_) + 1

    item_id_id = get_ppmp_item_id(gen)

    unique = False
    lst_itemcode = get_itemcode()
    while unique == False:

        itemcode = 'B' + str(random.randint(0, 99999))
        if itemcode not in lst_itemcode:
            unique = True
    
    sql = """INSERT INTO public."PPMP_itemdescription"(id,specifics1,specifics2,specifics3,
        specifics4,specifics5,item_id_id,itemcode) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""

    try:
        cur.execute(sql, (id_, specifics1, specifics2, specifics3, specifics4, specifics5, item_id_id,itemcode))
        #             cur.fetchone()[0]
        conn.commit()
        # cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)



    dateTimeObj = datetime.now
    # date_created = str(dateTimeObj).split(' ')[0]
    id_price = get_last_value_price()
    if id_price is None:
        id_price = 0
    else:
        id_price = int(id_price) + 1

    sql = """INSERT INTO public."PPMP_prices"(id,price,date_created,
        unit,item_id_id) VALUES(%s,%s,%s,%s,%s);"""

    try:
        cur.execute(sql, (id_price, price, datetime.now(), unit, id_))
        #             cur.fetchone()[0]
        conn.commit()
        # cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    id_orderdetails = get_last_order_details()
    if id_orderdetails is None:
        id_orderdetails = 0
    else:
        id_orderdetails = int(id_orderdetails) + 1

    sql = """INSERT INTO public."PPMP_orderdetails"(id,item_description_id_id,ppmp_id_id,price_id,
    first_quantity,second_quantity,third_quantity,fourth_quantity,date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

    try:
        cur.execute(sql, (id_orderdetails, id_, ppmp_id_id, id_price,
                          first_quantity, second_quantity, third_quantity, fourth_quantity, date))
        #             cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

