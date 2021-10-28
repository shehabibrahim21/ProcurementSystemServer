import psycopg2
import re
from config import config

def get_order_details_all(ppmp_id):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(''' SELECT public."PPMP_orderdetails".id,
    public."PPMP_item".general_name,public."PPMP_itemdescription".specifics1,
    public."PPMP_itemdescription".specifics2,public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4,public."PPMP_itemdescription".specifics5,
    public."PPMP_prices".unit,public."PPMP_prices".price, public."PPMP_orderdetails".first_quantity,
    public."PPMP_orderdetails".second_quantity,public."PPMP_orderdetails".third_quantity,
    public."PPMP_orderdetails".fourth_quantity FROM public."PPMP_orderdetails" 

    JOIN public."PPMP_prices" ON  public."PPMP_orderdetails".price_id = public."PPMP_prices".id
    JOIN public."PPMP_itemdescription" ON  public."PPMP_orderdetails".item_description_id_id = public."PPMP_itemdescription".id 
    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id
    JOIN public."PPMP_category" ON public."PPMP_item".category_id_id = public."PPMP_category".id
    WHERE public."PPMP_orderdetails".ppmp_id_id = %s
    
    ORDER BY public."PPMP_orderdetails".id''',(str(ppmp_id),))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst2.append(list(row))
        #         return row[0]
        row = cur.fetchone()
    cur.close()
    #     return lst2
    #     lst2.insert(9,float(lst2[8]) * lst2[9])
    print(lst2)
    for lst in lst2:
        lst.insert(10, float(lst[8]) * lst[9])
        lst.insert(12, float(lst[8]) * lst[11])
        lst.insert(14, float(lst[8]) * lst[13])
        lst.insert(16, float(lst[8]) * lst[15])

    lst3 = []
    for lst in lst2:
        lst2_new = []
        for i, u in enumerate(lst):
            if i not in [1, 2, 3, 4, 5, 6]:
                lst2_new.append(u)
            if i == 1:
                str_ = ' '.join(lst[1:7])
                str_ = str_.replace('None', '')
                re.sub(' +', ' ', str_)
                lst2_new.append(str_)
        lst3.append(lst2_new)

    return lst3


def get_order_details(cat_code, ppmp_id):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(''' SELECT public."PPMP_orderdetails".id,
    public."PPMP_item".general_name,public."PPMP_itemdescription".specifics1,
    public."PPMP_itemdescription".specifics2,public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4,public."PPMP_itemdescription".specifics5,
    public."PPMP_prices".unit,public."PPMP_prices".price, public."PPMP_orderdetails".first_quantity,
    public."PPMP_orderdetails".second_quantity,public."PPMP_orderdetails".third_quantity,
    public."PPMP_orderdetails".fourth_quantity FROM public."PPMP_orderdetails" 

    JOIN public."PPMP_prices" ON  public."PPMP_orderdetails".price_id = public."PPMP_prices".id
    JOIN public."PPMP_itemdescription" ON  public."PPMP_orderdetails".item_description_id_id = public."PPMP_itemdescription".id 
    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id
    JOIN public."PPMP_category" ON public."PPMP_item".category_id_id = public."PPMP_category".id
    WHERE public."PPMP_category".id = %s AND public."PPMP_orderdetails".ppmp_id_id = %s

    ORDER BY public."PPMP_orderdetails".id''', (str(cat_code), str(ppmp_id)))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst2.append(list(row))
        #         return row[0]
        row = cur.fetchone()
    cur.close()
    #     return lst2
    #     lst2.insert(9,float(lst2[8]) * lst2[9])
    print(lst2)
    for lst in lst2:
        lst.insert(10, float(lst[8]) * lst[9])
        lst.insert(12, float(lst[8]) * lst[11])
        lst.insert(14, float(lst[8]) * lst[13])
        lst.insert(16, float(lst[8]) * lst[15])

    lst3 = []
    for lst in lst2:
        lst2_new = []
        for i, u in enumerate(lst):
            if i not in [1, 2, 3, 4, 5, 6]:
                lst2_new.append(u)
            if i == 1:
                str_ = ' '.join(lst[1:7])
                str_ = str_.replace('None', '')
                re.sub(' +', ' ', str_)
                lst2_new.append(str_)
        lst3.append(lst2_new)

    return lst3