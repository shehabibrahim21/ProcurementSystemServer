import datetime
import psycopg2
import re
# from datetime import datetime
from config import config
import datetime as dt

def determine_quarter():
    string = str(datetime.datetime.now()).split(' ')[0].split('-')[1]
    if string in ['01','02','03']:
        return 'First Quarter'
    elif string in ['04','05','06']:
        return 'Second Quarter'
    elif string in ['07','08','09']:
        return 'Third Quarter'
    elif string in ['10','11','12']:
        return 'Fourth Quarter'


def determine_year():
    return str(datetime.datetime.now()).split(' ')[0].split('-')[0]


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


def show_list(year=determine_year(), quarter=determine_quarter()):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT id,qr_code FROM public."PPMP_app" where   year = %s and quarter = %s and group_id is %s
    ''', (int(year), str(quarter),None))


    row = cur.fetchone()
    lst_app = []
    while row is not None:
        lst_app.append(row[0])
        qr_code = row[1]
        row = cur.fetchone()
    lst_new = []
    ii = 1
    #     print(lst_app)
    for i in lst_app:
        #         print(i)
        lst_ = get_order_details_rows(i)
        #         print("asdasdas",lst_)
        if lst_:
            if len(lst_) < 2:
#                 print(lst_[0])
                nl = lst_[0][:-1]
                str_ = " ".join(nl[1:6])
                str_ = str_.replace('None', '')
                str_ = re.sub(' +', ' ', str_)
                str_ = str(nl[0]) + ", " + str_
                str_ = str_.strip()
                lst_new.append([ii] + [str_] + nl[6:]+[i])
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
                str_ = " ".join(nl[1:6])
                str_ = str_.replace('None', '')
                str_ = re.sub(' +', ' ', str_)
                str_ = str(nl[0]) + ", " + str_
                str_ = str_.strip()
                lst_new.append([ii] + [str_] + [nl[6], nl[7], fq, sq, tq, frq, "Various Cost Centers",i])

            ii = ii + 1
    # print(lst_new)
    quarter_lst = []
    if quarter == 'First Quarter':
        for i in lst_new:
            del i[5:-1]
            i.insert(5, int(i[3]) * (i[4]))
            quarter_lst.append(i)
    elif quarter == 'Second Quarter':
        for i in lst_new:
            del i[4]
            del i[5:7]
            quarter_lst.append(i)
    elif quarter == 'Third Quarter':
        for i in lst_new:
            del i[4:6]
            del i[5]
            quarter_lst.append(i)
    elif quarter == 'Fourth Quarter':

        for i in lst_new:
            del i[4:7]
            quarter_lst.append(i)

    lst_new = []
    for i in quarter_lst:
        i.insert(5, int(i[3]) * int(i[4]))
        lst_new.append(i)

    return lst_new
    cur.close()




def show_list_group(year=determine_year(), quarter=determine_quarter(),group = ""):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT id,qr_code FROM public."PPMP_app" where   year = %s and quarter = %s and group_id = %s
    ''', (int(year), str(quarter),str(group)))

    row = cur.fetchone()
    lst_app = []
    while row is not None:
        lst_app.append(row[0])
        qr_code = row[1]
        row = cur.fetchone()
    lst_new = []
    ii = 1
    print(lst_app)
    for i in lst_app:
        #         print(i)
        lst_ = get_order_details_rows(i)
        print(lst_)
        if lst_:
            if len(lst_) < 2:
#                 print(lst_[0])
                nl = lst_[0][:-1]
                str_ = " ".join(nl[1:6])
                str_ = str_.replace('None', '')
                str_ = re.sub(' +', ' ', str_)
                str_ = str(nl[0]) + ", " + str_
                str_ = str_.strip()
                lst_new.append([ii] + [str_] + nl[6:]+[i])
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
                str_ = " ".join(nl[1:6])
                str_ = str_.replace('None', '')
                str_ = re.sub(' +', ' ', str_)
                str_ = str(nl[0]) + ", " + str_
                str_ = str_.strip()
                lst_new.append([ii] + [str_] + [nl[6], nl[7], fq, sq, tq, frq, "Various Cost Centers",i])

            ii = ii + 1
    quarter_lst = []
    if quarter == 'First Quarter':
        for i in lst_new:
            del i[5:-1]
            i.insert(5, int(i[3]) * (i[4]))
            quarter_lst.append(i)
    elif quarter == 'Second Quarter':
        for i in lst_new:
            del i[4]
            del i[5:7]
            quarter_lst.append(i)
    elif quarter == 'Third Quarter':
        for i in lst_new:
            del i[4:6]
            del i[5]
            quarter_lst.append(i)
    elif quarter == 'Fourth Quarter':

        for i in lst_new:
            del i[4:7]
            quarter_lst.append(i)

    lst_new = []
    for i in quarter_lst:
        i.insert(5, int(i[3]) * int(i[4]))
        lst_new.append(i)

    return lst_new
    cur.close()




