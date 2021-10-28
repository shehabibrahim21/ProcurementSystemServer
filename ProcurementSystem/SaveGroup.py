#!/usr/bin/env python
# coding: utf-8

# In[1]:

import datetime as dt
import datetime
import psycopg2
import re
from config import config
def get_id():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT group_id FROM public."PPMP_app"''', )

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    dct = {}
    while row is not None:
        if row[0] is not None:
            lst1.append(int(row[0]))
        row = cur.fetchone()
    cur.close()
    if lst1:
        return max(lst1) + 1 
    else:
        return 0 + 1


# In[2]:


def set_group(lst):
    
    group_id = get_id()
    
    for i in lst:
        editAPP(i,group_id)


# In[3]:


def editAPP(id_,group_id):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql_update_query = """Update public."PPMP_app" set group_id = %s where id = %s"""
        cur.execute(sql_update_query, (group_id, id_))
        conn.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if (conn):
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")        

def get_group_id():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT group_id FROM public."PPMP_app"''', )

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    dct = {}
    while row is not None:
        if row[0] is not None:
            lst1.append(int(row[0]))
        row = cur.fetchone()
    cur.close()
    lst1 = list(set(lst1))
    lst2 = []
    lst2.append(("Select Group","Select Group"))
    for i in lst1:
        lst2.append((i, "Group "+ str(i)))
    return lst2


def determine_quarter():
    string = str(datetime.datetime.now()).split(' ')[0].split('-')[1]
    if string in ['01', '02', '03']:
        return 'First Quarter'
    elif string in ['04', '05', '06']:
        return 'Second Quarter'
    elif string in ['07', '08', '09']:
        return 'Third Quarter'
    elif string in ['10', '11', '12']:
        return 'Fourth Quarter'


def get_group_details_lst():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(''' SELECT public."PPMP_app".id, public."PPMP_app".item_description,public."PPMP_app".year, "PPMP_app".category

    FROM public."PPMP_app"


    ''', )

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    #     dct = {}
    while row is not None:
        lst1.append(list(row))
        row = cur.fetchone()
    cur.close()
    return lst1


def get_order_details_lst():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(''' SELECT public."PPMP_orderdetails".id,
    public."PPMP_item".general_name,public."PPMP_itemdescription".specifics1,
    public."PPMP_itemdescription".specifics2,public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4,public."PPMP_itemdescription".specifics5,
    public."PPMP_ppmp".year,public."PPMP_category".name
    FROM public."PPMP_orderdetails"

    JOIN public."PPMP_prices" ON  public."PPMP_orderdetails".price_id = public."PPMP_prices".id
    JOIN public."PPMP_itemdescription" ON  public."PPMP_orderdetails".item_description_id_id = public."PPMP_itemdescription".id 
    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id
    JOIN public."PPMP_category" ON public."PPMP_item".category_id_id = public."PPMP_category".id
    JOIN public."PPMP_ppmp" ON public."PPMP_orderdetails".ppmp_id_id = public."PPMP_ppmp".id


    ORDER BY public."PPMP_orderdetails".id''', )

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        #         lst2.append(list(row))
        lst_ = list(row)
        while 'None' in lst_:
            lst_.remove('None')
        len_ = len(lst_)

        str_ = ' '.join(lst_[2:len_ - 2])
        str_ = str_.replace('None', '')
        item_ = lst_[1] + ", " + str_
        re.sub(' +', ' ', item_)
        #         return row[0]
        lst3 = [lst_[0], item_, lst_[-2], lst_[-1]]
        lst2.append(lst3)
        row = cur.fetchone()

    cur.close()
    return lst2


def delete_group_app(id_):
    conn = None
    rows_deleted = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute('DELETE FROM public."PPMP_app" WHERE public."PPMP_app".id = %s', (id_,))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def clean_group():
    org_order_details = get_order_details_lst()
    org_group_details = get_group_details_lst()
    rev_order_details = [i[1:] for i in get_order_details_lst()]
    rev_group_details = [i[1:] for i in get_group_details_lst()]

    lst_ = get_group_details_lst()
    for i, u in zip(org_order_details, rev_order_details):
        for ii, uu in zip(org_group_details, rev_group_details):

            if u == uu:
                lst_.remove(ii)

    lst_id = [i[0] for i in lst_]

    for i in lst_id:
        delete_group_app(i)





def get_group_app():
    clean_group()
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(''' SELECT public."PPMP_app".item_description,
    public."PPMP_app".group_id

    FROM public."PPMP_app" 
    WHERE public."PPMP_app".quarter = %s  and public."PPMP_app".group_id != %s

    ''', (str(determine_quarter()), ""))

    row = cur.fetchone()
    lst2 = []
    dct = {}
    while row is not None:
        lst3 = list(row)
        temp = []
        if lst3[1] in dct.keys():
            if type(dct[lst3[1]]) == list:
                temp = dct[lst3[1]]
            else:
                temp.append(dct[lst3[1]])

            temp.append(lst3[0])
            dct[lst3[1]] = temp
        else:
            dct[lst3[1]] = lst3[0]
        row = cur.fetchone()
    cur.close()
    lst5 = []
    for key in dct.keys():
        lst4 = []
        lst = dct[key]
        if type(lst) == list:
            for elem in lst:
                lst_ = elem.split(',')
                for i in lst_:
                    if i not in lst4:
                        lst4.append(i)
        else:
            lst4 = lst.split(',')
        str_ = " ".join(lst4)
        str_ = re.sub("\s\s+", " ", str_)
        lst5.append("Group " + key + " (" + str_ + ")")

    lst2 = list(dct.keys())
    lst3 = []
    for i in lst2:
        lst3.append("Group " + i)
    return "   ".join(lst5)

def get_app_id(group_id):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''
    SELECT

    public."PPMP_app".id


    FROM public."PPMP_app" 

    WHERE 

    public."PPMP_app".group_id = %s''', (str(group_id),))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst1.append(row[0])
        row = cur.fetchone()
    return lst1
    cur.close()

def delete_group(id_):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()


        sql_update_query = """Update public."PPMP_app" set group_id = %s where id = %s"""
        cur.execute(sql_update_query, (None, id_))
        conn.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if (conn):
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

def get_group_app_for_select():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(''' SELECT public."PPMP_app".item_description,
    public."PPMP_app".group_id

    FROM public."PPMP_app" 
    WHERE public."PPMP_app".quarter = %s  and public."PPMP_app".group_id != %s

    ''', (str(determine_quarter()), ""))

    row = cur.fetchone()
    lst2 = []
    dct = {}
    while row is not None:
        lst3 = list(row)
        temp = []
        if lst3[1] in dct.keys():
            if type(dct[lst3[1]]) == list:
                temp = dct[lst3[1]]
            else:
                temp.append(dct[lst3[1]])

            temp.append(lst3[0])
            dct[lst3[1]] = temp
        else:
            dct[lst3[1]] = lst3[0]
        row = cur.fetchone()
    cur.close()
    lst5 = []
    for key in dct.keys():
        lst4 = []
        lst = dct[key]
        if type(lst) == list:
            for elem in lst:
                lst_ = elem.split(',')
                for i in lst_:
                    if i not in lst4:
                        lst4.append(i)
        else:
            lst4 = lst.split(',')
        str_ = " ".join(lst4)
        str_ = re.sub("\s\s+", " ", str_)
        lst5.append((key,"Group " + key + " (" + str_ + ")"))

    lst2 = list(dct.keys())
    lst3 = []
    for i in lst2:
        lst3.append("Group " + i)
    return lst5


def get_group_details(group_id, dct):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(''' SELECT public."PPMP_app".id,public."PPMP_app".category

    FROM public."PPMP_app"



    WHERE public."PPMP_app".group_id = %s

    ''', (str(group_id),))

    row = cur.fetchone()
    lst1 = []
    #     dct = {}
    while row is not None:
        dct[row[0]] = list(row)[1:]
        #         return row[0]
        row = cur.fetchone()
    cur.close()

def get_group_order_details(app_id, dct):
    conn = psycopg2.connect(host="localhost", database="hr_database", user="postgres", password="Bankai21")
    cur = conn.cursor()

    cur.execute(''' SELECT

    public."PPMP_item".general_name,

    public."PPMP_itemdescription".specifics1, public."PPMP_itemdescription".specifics2, 
    public."PPMP_itemdescription".specifics3, public."PPMP_itemdescription".specifics4, 
    public."PPMP_itemdescription".specifics5, 

    public."PPMP_orderdetails".first_quantity,  public."PPMP_orderdetails".second_quantity, 
    public."PPMP_orderdetails".third_quantity, public."PPMP_orderdetails".fourth_quantity,

    public."PPMP_prices".price,
    public."PPMP_prices".unit,
    public."PPMP_costcenter".name

    FROM public."PPMP_orderdetails"

    JOIN public."PPMP_itemdescription" ON public."PPMP_orderdetails".item_description_id_id = public."PPMP_itemdescription".id

    JOIN public."PPMP_prices" ON public."PPMP_orderdetails".price_id = public."PPMP_prices".id

    JOIN public."PPMP_item" ON public."PPMP_item".id = public."PPMP_itemdescription".item_id_id

    JOIN public."PPMP_ppmp" ON public."PPMP_orderdetails".ppmp_id_id = public."PPMP_ppmp".id

    JOIN public."PPMP_costcenter" ON public."PPMP_ppmp".cc_num_id = public."PPMP_costcenter".id

    WHERE public."PPMP_orderdetails".app_id = %s

    ''', (str(app_id),))

    row = cur.fetchone()
    lst1 = []
    while row is not None:
        if len(dct[app_id]) == 14:
            lst_old = dct[app_id]
            lst_new = [lst_old[0]] + list(row)
            lst_new2 = lst_old[:7] +[lst_old[7]+lst_new[7]] + [lst_old[8]+lst_new[8]] + [lst_old[9]+lst_new[9]] + [lst_old[10]+lst_new[10]]+ [lst_old[11]] + [lst_old[12]] + [lst_old[13] + "and+" + lst_new[13]]
            dct[app_id] = lst_new2
        else:
            dct[app_id] = dct[app_id] + list(row)
        row = cur.fetchone()
    cur.close()

    return dct



def get_group_details_combined(group_id):
    dct = {}
    get_group_details(group_id, dct)
#     print("aaa",dct,"sss")
    for i in dct.keys():
        get_group_order_details(i, dct)
#     print("aaa",dct,"sss")
    lst = []
    for i in dct.keys():
        if len(dct[i]) > 13:
            lst.append(dct[i])
#     print("aaa111",lst,"sss111")
    for i in lst:
        lst2 = i[2:7]
        while 'None' in lst2:
            lst2.remove('None')
        str_ = "<br/>".join(lst2)
        i.append(str_)
    return lst