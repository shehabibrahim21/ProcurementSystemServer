#!/usr/bin/env python
# coding: utf-8

# In[29]:

from config import config
import psycopg2
import re
def get_items(cat_code):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(''' SELECT public."PPMP_itemdescription".id,
    public."PPMP_item".general_name,public."PPMP_itemdescription".specifics1,
    public."PPMP_itemdescription".specifics2,public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4,public."PPMP_itemdescription".specifics5
    FROM public."PPMP_itemdescription" 
    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id
    JOIN public."PPMP_category" ON public."PPMP_item".category_id_id = public."PPMP_category".id
    WHERE public."PPMP_category".id = %s 

    ''', (str(cat_code),))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    lst3 = []
    dct = {}
    while row is not None:
        lst2.append(list(row))
        #         return row[0]
        row = cur.fetchone()
    for i in lst2:
        str_ = " ".join(i[1:])
        str_ = str_.replace("None","")
        str_ = re.sub(' +', ' ', str_)
        str_ = str_.strip()
        # lst1.append([i[0],str_])
        dct[str_] = i[0]
        lst3.append(str_)
    cur.close()
    return dct, "   ".join(lst3)


def get_items_des(cat_code):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(''' SELECT public."PPMP_itemdescription".id,
    public."PPMP_item".general_name,public."PPMP_itemdescription".specifics1,
    public."PPMP_itemdescription".specifics2,public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4,public."PPMP_itemdescription".specifics5
    FROM public."PPMP_itemdescription" 
    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id
    JOIN public."PPMP_category" ON public."PPMP_item".category_id_id = public."PPMP_category".id
    WHERE public."PPMP_category".id = %s 

    ''', (str(cat_code),))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    lst3 = []
    while row is not None:
        lst2.append(list(row))
        #         return row[0]
        row = cur.fetchone()
    for i in lst2:
        str_ = " ".join(i[1:])
        str_ = str_.replace("None","")
        str_ = re.sub(' +', ' ', str_)
        str_ = str_.strip()
        lst1.append([i[0],str_])
        lst3.append(str_)
    cur.close()
    return lst1


def get_price_details():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(''' SELECT public."PPMP_prices".item_id_id,public."PPMP_prices".price,public."PPMP_prices".unit

    FROM public."PPMP_prices" 

    ''')

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    lst3 = []
    while row is not None:
        lst2.append(list(row))
        #         return row[0]
        row = cur.fetchone()
    return lst2


# def get_item_details(catcode):
#     lst_items = get_items_des(catcode)
#     lst_prices = get_price_details()
#     lst_fin = []
#     for i in lst_items:
#         lst_temp = []
#         for u in lst_prices:
#             if i[0] == u[0]:
#                 lst_temp = u[1:]
#         if lst_temp:
#             lst_ = i + lst_temp
#         if lst_[1:4] not in lst_fin:
#             lst_fin.append(lst_[1:4])
#     lst_fin = [item for sublist in lst_fin for item in sublist]
#     lst_fin = [str(i) for i in lst_fin]
#     str_ = "   ".join(lst_fin)
#     str_ = str_.replace('\n','')
#     return str_

def get_item_details(catcode):
    lst_items = get_items_des(catcode)
    lst_prices = get_price_details()
    #     print(lst_items)
    #     print("-----------------------------------")
    #     print(lst_prices)
    lst_fin = []
    for i in lst_items:
        lst_temp = []
        for u in lst_prices:
            #             print(i[0],u[0])
            if i[0] == u[0]:
                lst_temp = u[1:]
        #         print(lst_temp)
        if lst_temp:
            lst_ = i + lst_temp
        try:
            if lst_[1:4] not in lst_fin:
                lst_fin.append(lst_[1:4])
        except:
            pass
    lst_fin = [item for sublist in lst_fin for item in sublist]
    lst_fin = [str(i) for i in lst_fin]
    str_ = "   ".join(lst_fin)
    str_ = str_.replace('\n', '')
    return str_


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