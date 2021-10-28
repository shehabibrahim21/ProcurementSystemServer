import psycopg2
import re
from datetime import datetime
from config import config
import datetime as dt


def get_costcenters():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT description FROM public."PPMP_sourceoffund"''')

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst1.append((row[0], row[0]))
        row = cur.fetchone()
    cur.close()

    return lst1

def get_category():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT name FROM public."PPMP_category"''')

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst1.append((row[0], row[0]))
        row = cur.fetchone()
    cur.close()
    lst1.sort()
    return lst1


def get_year():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT DISTINCT(year) FROM public."PPMP_ppmp" ORDER BY year''')

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst1.append((row[0], row[0]))
        row = cur.fetchone()
    cur.close()
    lst1.reverse()
    return lst1


def get_type():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT DISTINCT(type) FROM public."PPMP_ppmp"''')

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst1.append((row[0], row[0]))
        row = cur.fetchone()
    cur.close()

    return lst1


def get_code(desc):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT code FROM public."PPMP_category" where 
    public."PPMP_category".name = %s''', (str(desc),))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    dct = {}
    while row is not None:
        return row[0]
        row = cur.fetchone()
    cur.close()



def get_id(desc):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT id FROM public."PPMP_category" where 
    public."PPMP_category".name = %s''', (str(desc),))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    dct = {}
    while row is not None:
        return row[0]
        row = cur.fetchone()
    cur.close()

def sof_get_id(desc):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT id FROM public."PPMP_sourceoffund" where 
    public."PPMP_sourceoffund".description = %s''', (str(desc),))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    dct = {}
    while row is not None:
        return row[0]
        row = cur.fetchone()
    cur.close()

def get_last_value_app():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT MAX(id) FROM public."PPMP_app"''')

    row = cur.fetchone()
    while row is not None:
        return row[0]
        row = cur.fetchone()

    cur.close()


def edit_order_details(id_,app_id):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        sql_update_query = """Update public."PPMP_orderdetails" set app_id = %s where id = %s"""
        cur.execute(sql_update_query, (app_id, id_))
        conn.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if (conn):
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")


def get_order_details(source_of_fund, type_, year, qrtr, category):
    #     app_id = insert_app(source_of_fund, category, type_, year)

    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''
    SELECT

    public."PPMP_item".general_name, 
    public."PPMP_itemdescription".specifics1, public."PPMP_itemdescription".specifics2, public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4, public."PPMP_itemdescription".specifics5,

    public."PPMP_prices".unit, public."PPMP_prices".price,
    public."PPMP_orderdetails".first_quantity, public."PPMP_orderdetails".second_quantity, 
    public."PPMP_orderdetails".third_quantity, public."PPMP_orderdetails".fourth_quantity,

    public."PPMP_costcenter".name,
    public."PPMP_orderdetails".ID

    FROM public."PPMP_orderdetails" 

    JOIN public."PPMP_itemdescription" ON public."PPMP_orderdetails".item_description_id_id = public."PPMP_itemdescription".id

    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id

    JOIN public."PPMP_prices" ON public."PPMP_orderdetails".price_id = public."PPMP_prices".id 

    JOIN public."PPMP_category" ON public."PPMP_item".category_id_id = public."PPMP_category".id

    JOIN public."PPMP_ppmp" ON public."PPMP_ppmp".id = public."PPMP_orderdetails".ppmp_id_id    

    JOIN public."PPMP_sourceoffund" ON public."PPMP_ppmp".sof_num_id = public."PPMP_sourceoffund".id     

    JOIN public."PPMP_costcenter" ON public."PPMP_ppmp".cc_num_id = public."PPMP_costcenter".id  

    WHERE 

    public."PPMP_sourceoffund".description = %s AND

    public."PPMP_ppmp".type = %s AND

    public."PPMP_ppmp".year = %s AND

    public."PPMP_category".name = %s 

    ''', (str(source_of_fund), str(type_), str(year), str(category)))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst1.append(list(row))
        row = cur.fetchone()
    cur.close()
    i = 1
    for lst in lst1:
        lst.insert(9, float(lst[7]) * int(lst[8]))
        lst.insert(11, float(lst[7]) * int(lst[10]))
        lst.insert(13, float(lst[7]) * int(lst[12]))
        lst.insert(15, float(lst[7]) * int(lst[14]))
        lst.insert(-1, int(lst[8]) + int(lst[10]) + int(lst[12]) + int(lst[14]))
        lst.insert(-1, float(lst[7]) * (int(lst[8]) + int(lst[10]) + int(lst[12]) + int(lst[14])))
        lst.insert(0, i)
        str_ = " ".join(lst[2:7])
        str_ = str_.replace('None', '')
        str_ = re.sub(' +', ' ', str_)
        str_ = str(lst[1]) + ", " + str_
        str_ = str_.strip()
        lst.insert(1, str_)
        del lst[2:8]
        i += 1
    return lst1


def get_order_details_compressed(source_of_fund, type_, year, qrtr, category):
    #     app_id = insert_app(source_of_fund, category, type_, year)
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''
    SELECT

    public."PPMP_item".general_name, 
    public."PPMP_itemdescription".specifics1, public."PPMP_itemdescription".specifics2, public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4, public."PPMP_itemdescription".specifics5,

    public."PPMP_prices".unit, public."PPMP_prices".price,
    public."PPMP_orderdetails".first_quantity, public."PPMP_orderdetails".second_quantity, 
    public."PPMP_orderdetails".third_quantity, public."PPMP_orderdetails".fourth_quantity,

    public."PPMP_costcenter".name

    FROM public."PPMP_orderdetails" 

    JOIN public."PPMP_itemdescription" ON public."PPMP_orderdetails".item_description_id_id = public."PPMP_itemdescription".id

    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id

    JOIN public."PPMP_prices" ON public."PPMP_orderdetails".price_id = public."PPMP_prices".id 

    JOIN public."PPMP_category" ON public."PPMP_item".category_id_id = public."PPMP_category".id

    JOIN public."PPMP_ppmp" ON public."PPMP_ppmp".id = public."PPMP_orderdetails".ppmp_id_id    

    JOIN public."PPMP_sourceoffund" ON public."PPMP_ppmp".sof_num_id = public."PPMP_sourceoffund".id     

    JOIN public."PPMP_costcenter" ON public."PPMP_ppmp".cc_num_id = public."PPMP_costcenter".id  

    WHERE 

    public."PPMP_sourceoffund".description = %s AND

    public."PPMP_ppmp".type = %s AND

    public."PPMP_ppmp".year = %s AND

    public."PPMP_category".name = %s 

    ''', (str(source_of_fund), str(type_), str(year), str(category)))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst1.append(list(row))
        row = cur.fetchone()
    cur.close()
    i = 1
    for lst in lst1:
        lst.insert(9, float(lst[7]) * int(lst[8]))
        lst.insert(11, float(lst[7]) * int(lst[10]))
        lst.insert(13, float(lst[7]) * int(lst[12]))
        lst.insert(15, float(lst[7]) * int(lst[14]))
        lst.insert(-1, int(lst[8]) + int(lst[10]) + int(lst[12]) + int(lst[14]))
        lst.insert(-1, float(lst[7]) * (int(lst[8]) + int(lst[10]) + int(lst[12]) + int(lst[14])))
        lst.insert(0, i)
        str_ = " ".join(lst[2:7])
        str_ = str_.replace('None', '')
        str_ = re.sub(' +', ' ', str_)
        str_ = str(lst[1]) + ", " + str_
        str_ = str_.strip()
        lst.insert(1, str_)
        del lst[2:8]
        i += 1

    lst_ = lst1
    new_lst = []
    for index_, lst in enumerate(lst_):

        for index1, lst1 in enumerate(lst_):

            if lst != lst1:

                if lst[1] == lst1[1]:
                    for i in range(4, 14):
                        lst[i] = lst[i] + lst1[i]
                    if lst[-1] != lst1[-1]:
                        lst[-1] = 'Various CC'
                    lst_.remove(lst1)

        new_lst.append(lst)
    quarter_lst = []
    if qrtr == 'First Quarter':
        for i in new_lst:
            del i[6:13]
            quarter_lst.append(i)
    elif qrtr == 'Second Quarter':
        for i in new_lst:
            del i[4:6]
            del i[6:11]
            quarter_lst.append(i)
    elif qrtr == 'Third Quarter':
        for i in new_lst:
            del i[4:8]
            del i[6:9]
            quarter_lst.append(i)
    elif qrtr == 'Fourth Quarter':

        for i in new_lst:
            del i[4:11]
            quarter_lst.append(i)
    return quarter_lst


def insert_app(id_, source_of_fund, description, type_, year, quarter, category, qr_code):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT id FROM public."PPMP_app" where item_description = %s and source_of_fund = %s and type = %s and year = %s
    and quarter = %s and category = %s
    ''', (str(description), str(source_of_fund), str(type_), int(year), str(quarter), str(category)))

    row = cur.fetchone()
    print(row)
    lst1 = []
    if row is None:

        dateTimeObj = dt.datetime.now()
        sql = """INSERT INTO public."PPMP_app"(id,date_created,item_description,quarter,year,type,source_of_fund,category,qr_code,group_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

        row = cur.fetchone()

        try:
            cur.execute(sql, (
            id_, str(dateTimeObj).split(' ')[0], description, quarter, year, type_, source_of_fund, category, qr_code,None))

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return id_
    else:
        return row[0]


import datetime as dt


def update_app(source_of_fund, type_, year, qrtr, category):
    lst = get_order_details(source_of_fund, type_, year, qrtr, category)
    lst_compressed = get_order_details_compressed(source_of_fund, type_, year, qrtr, category)

    app_id = 0
    if get_last_value_app():
        app_id = get_last_value_app() + 1

    x = dt.datetime.now()
    str_ = str(x)
    str_ = str_.replace('-', '')
    str_ = str_.replace('.', '')
    str_ = str_.replace(':', '')
    str_ = str_.replace(' ', '')
    qr_code = int(str_[:14])

    for i in lst_compressed:

        app_id = get_last_value_app()
        if app_id is None:
            app_id = 0
        else:
            app_id = int(app_id) + 1
        app_id = insert_app(app_id, source_of_fund, i[1], type_, year, qrtr, category, qr_code)

        for u in lst:
            if i[1] == u[1]:
                edit_order_details(u[-1], app_id)
def get_app_values():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT id FROM public."PPMP_app" where item_description = %s and source_of_fund = %s and type = %s and year = %s
    and quarter = %s
    ''', (str(description), str(source_of_fund), str(type_), int(year),str(quarter)))

    row = cur.fetchone()
    print(row)
    lst1 = []
    if row is None:


        dateTimeObj = datetime.now()
        sql = """INSERT INTO public."PPMP_app"(id,date_created,item_description,quarter,year,type,source_of_fund,category) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""


        row = cur.fetchone()

        try:
            cur.execute(sql, (id_, str(dateTimeObj).split(' ')[0],description,quarter,year,type_,source_of_fund,category))

            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return id_
    else:
        return row[0]


def get_order_details_rows(app_id):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''
    SELECT

    public."PPMP_item".general_name, 
    public."PPMP_itemdescription".specifics1, public."PPMP_itemdescription".specifics2, public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4, public."PPMP_itemdescription".specifics5,

    public."PPMP_prices".unit, public."PPMP_prices".price,
    public."PPMP_orderdetails".first_quantity, public."PPMP_orderdetails".second_quantity, 
    public."PPMP_orderdetails".third_quantity, public."PPMP_orderdetails".fourth_quantity,

    public."PPMP_costcenter".name,
    public."PPMP_orderdetails".ID

    FROM public."PPMP_orderdetails" 

    JOIN public."PPMP_itemdescription" ON public."PPMP_orderdetails".item_description_id_id = public."PPMP_itemdescription".id

    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id

    JOIN public."PPMP_prices" ON public."PPMP_orderdetails".price_id = public."PPMP_prices".id 

    JOIN public."PPMP_category" ON public."PPMP_item".category_id_id = public."PPMP_category".id

    JOIN public."PPMP_ppmp" ON public."PPMP_ppmp".id = public."PPMP_orderdetails".ppmp_id_id    

    JOIN public."PPMP_sourceoffund" ON public."PPMP_ppmp".sof_num_id = public."PPMP_sourceoffund".id     

    JOIN public."PPMP_costcenter" ON public."PPMP_ppmp".cc_num_id = public."PPMP_costcenter".id  

    WHERE 

    public."PPMP_orderdetails".app_id = %s''', (str(app_id),))

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst1.append(list(row))
        row = cur.fetchone()
    return lst1
    cur.close()


def create_app(source_of_fund, category, type_, year, quarter):
    update_app(source_of_fund, type_, year, quarter, category)
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT id,qr_code FROM public."PPMP_app" where  source_of_fund = %s and type = %s and year = %s
    and quarter = %s and category = %s
    ''', (str(source_of_fund), str(type_), int(year), str(quarter), str(category)))

    row = cur.fetchone()
    lst_app = []
    while row is not None:
        # print("bla",row[0])
        lst_app.append(row[0])
        qr_code = row[1]
        row = cur.fetchone()
    lst_new = []
    ii = 1
    print(lst_app)
    for i in lst_app:
        print(i)
        lst_ = get_order_details_rows(i)
        print("asdasdas",lst_)
        if lst_:
            if len(lst_) < 2:
                nl = lst_[0][:-1]
                str_ = " ".join(nl[1:6])
                str_ = str_.replace('None', '')
                str_ = re.sub(' +', ' ', str_)
                str_ = str(nl[0]) + ", " + str_
                str_ = str_.strip()
                lst_new.append([ii] + [str_] + nl[6:])
            else:
                fq = 0
                sq = 0
                tq = 0
                frq = 0

                for lst in lst_:
                    fq = fq + lst[8]
                    sq = sq + lst[9]
                    tq = tq + lst[10]
                    frq = frq + lst[11]
                nl = lst[:-1]
                str_ = " ".join(nl[1 :6])
                str_ = str_.replace('None', '')
                str_ = re.sub(' +', ' ', str_)
                str_ = str(nl[0]) + ", " + str_
                str_ = str_.strip()
                lst_new.append([ii] +[str_]+[nl[6],nl[7],fq,sq,tq,frq,"Various Cost Centers"])

            ii = ii + 1

    print(lst_new)
    quarter_lst = []
    if quarter == 'First Quarter':
        for i in lst_new:
            del i[5:-1]
            i.insert(5,int(i[3])*(i[4]))
            quarter_lst.append(i)
    elif quarter == 'Second Quarter':
        for i in lst_new:
            del i[4]
            del i[5:7]
            i.insert(5, int(i[3]) * (i[4]))
            quarter_lst.append(i)
    elif quarter == 'Third Quarter':
        for i in lst_new:
            del i[4:6]
            del i[5]
            i.insert(5, int(i[3]) * (i[4]))
            quarter_lst.append(i)
    elif quarter == 'Fourth Quarter':

        for i in lst_new:
            del i[4:7]
            i.insert(5, int(i[3]) * (i[4]))
            quarter_lst.append(i)

    return quarter_lst,qr_code
    #     return lst_new, qr_code
    # cur.close()
        #     cur.close()
    cur.close()

