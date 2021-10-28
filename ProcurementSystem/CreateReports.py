
# coding: utf-8

# In[1]:

from config import config
import psycopg2
import re
def get_costcenters():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT id,name FROM public."PPMP_costcenter"''')
    

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst1.append(row[0:2])
        row = cur.fetchone()
    cur.close()
    
    return lst1
 

def get_ppmp():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT public."PPMP_costcenter".name, public."PPMP_category".name,public."PPMP_sourceoffund".description,
    public."PPMP_ppmp".year,  
    public."PPMP_item".general_name, 
    public."PPMP_itemdescription".specifics1, public."PPMP_itemdescription".specifics2, public."PPMP_itemdescription".specifics3,
    public."PPMP_itemdescription".specifics4, public."PPMP_itemdescription".specifics5,
    
    public."PPMP_prices".price,
    public."PPMP_orderdetails".first_quantity, public."PPMP_orderdetails".second_quantity, 
    public."PPMP_orderdetails".third_quantity, public."PPMP_orderdetails".fourth_quantity, 
    public."PPMP_orderdetails".date 
    
    FROM public."PPMP_costcenter" 
    
    JOIN public."PPMP_ppmp" ON  public."PPMP_costcenter".id =  public."PPMP_ppmp".cc_num_id
    
    JOIN public."PPMP_orderdetails" ON public."PPMP_ppmp".id = public."PPMP_orderdetails".ppmp_id_id
    
    JOIN public."PPMP_sourceoffund" ON public."PPMP_ppmp".sof_num_id = public."PPMP_sourceoffund".id 
    
    JOIN public."PPMP_itemdescription" ON public."PPMP_orderdetails".item_description_id_id = public."PPMP_itemdescription".id
    
    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id
    
    JOIN public."PPMP_prices" ON public."PPMP_orderdetails".price_id = public."PPMP_prices".id 
    
    JOIN public."PPMP_category" ON public."PPMP_item".category_id_id = public."PPMP_category".id
    
    ''')
    

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst1.append(list(row))
        row = cur.fetchone()
    cur.close()
    
    return lst1
 





def generate_report():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT public."PPMP_costcenter".name, public."PPMP_category".name,public."PPMP_sourceoffund".description,
    public."PPMP_ppmp".year,  
    public."PPMP_item".general_name, 

    public."PPMP_orderdetails".date ,
    public."PPMP_orderdetails".first_quantity, public."PPMP_orderdetails".second_quantity, 
    public."PPMP_orderdetails".third_quantity, public."PPMP_orderdetails".fourth_quantity


    FROM public."PPMP_costcenter" 

    JOIN public."PPMP_ppmp" ON  public."PPMP_costcenter".id =  public."PPMP_ppmp".cc_num_id

    JOIN public."PPMP_orderdetails" ON public."PPMP_ppmp".id = public."PPMP_orderdetails".ppmp_id_id

    JOIN public."PPMP_sourceoffund" ON public."PPMP_ppmp".sof_num_id = public."PPMP_sourceoffund".id 

    JOIN public."PPMP_itemdescription" ON public."PPMP_orderdetails".item_description_id_id = public."PPMP_itemdescription".id

    JOIN public."PPMP_item" ON public."PPMP_itemdescription".item_id_id = public."PPMP_item".id

    JOIN public."PPMP_prices" ON public."PPMP_orderdetails".price_id = public."PPMP_prices".id 

    JOIN public."PPMP_category" ON public."PPMP_item".category_id_id = public."PPMP_category".id

    ''')

    row = cur.fetchone()
    lst1 = []
    lst2 = []
    while row is not None:
        lst_temp = list(row)
        lst_f = lst_temp[:6]
        lst_s = [int(i) for i in lst_temp[6:]]
        sum_ = sum(lst_s)
        lst_f.append(sum_)
        lst1.append(lst_f)
        row = cur.fetchone()
    cur.close()

    return lst1


def generate_lists():
    lst = generate_report()
    lst_cc = list(set([i[0] for i in lst]))
    lst_cat = list(set([i[1] for i in lst]))
    lst_item = list(set([i[4] for i in lst]))
    lst_dates = list(set([i[5][:7] for i in lst]))

    lst_yr = [i[:4] for i in lst_dates]
    lst_yr_qrtr = []
    qrts = ['First Quarter', 'Second Quarter', 'Third Quarter', 'Fourth Quarter']
    for i in lst_yr:
        for u in qrts:
            lst_yr_qrtr.append(str(i) + " " + str(u))
    return lst_cc, lst_cat, lst_item, lst_yr_qrtr


input_ = ['College of Computer Studies', 'asdasd', 'Bond Paper', '']


def check(input_):
    lst = generate_report()

    frst = ['01', '02', '03']
    scnd = ['04', '05', '06']
    thrd = ['07', '08', '09']
    frth = ['10', '11', '12']

    for lst_ in lst:
        if lst_[5].split('-')[1] in frst:
            lst_[5] = lst_[5].split('-')[0] + " " + "First Quarter"
        elif lst_[5].split('-')[1] in scnd:
            lst_[5] = lst_[5].split('-')[0] + " " + "Second Quarter"
        elif lst_[5].split('-')[1] in thrd:
            lst_[5] = lst_[5].split('-')[0] + " " + "Third Quarter"
        elif lst_[5].split('-')[1] in frth:
            lst_[5] = lst_[5].split('-')[0] + " " + "Fourth Quarter"

    lst_left1 = []

    #     for i in lst:
    lst_0 = [i[0] for i in lst]
    if input_[0] in lst_0:
        for i in lst:
            if i[0] == input_[0]:
                lst_left1.append(i)
    else:
        lst_left1 = lst

    lst_0 = [i[1] for i in lst_left1]
    lst_left2 = []
    if input_[1] in lst_0:

        for i in lst_left1:
            if i[1] == input_[1]:
                lst_left2.append(i)
    else:
        lst_left2 = lst_left1

    lst_0 = [i[4] for i in lst_left2]
    lst_left3 = []
    if input_[2] in lst_0:

        for i in lst_left2:
            if i[4] == input_[2]:
                lst_left3.append(i)
    else:
        lst_left3 = lst_left2

    lst_0 = [i[5] for i in lst_left3]
    lst_left4 = []
    if input_[3] in lst_0:

        for i in lst_left3:
            if i[5] == input_[3]:
                lst_left4.append(i)

    return lst_left4
