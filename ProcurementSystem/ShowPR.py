from config import config
import psycopg2
import re
def show_pr(orderdetails_id):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # year = get_year()[0]

    cur.execute('''SELECT public."PPMP_purchaserequest".specification_details,
     public."PPMP_purchaserequest".purpose,public."PPMP_purchaserequest".id
    

    FROM public."PPMP_purchaserequest" 
    where "PPMP_purchaserequest".orderdetails_id_id = %s ''', (orderdetails_id,))

    row = cur.fetchone()
    lst1 = []
    while row is not None:
#         lst1.append(list(row))
        return list(row)
        row = cur.fetchone()


def get_pr_details(orderdetails_id):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # year = get_year()[0]

    cur.execute('''SELECT 
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



    WHERE  public."PPMP_orderdetails".id = %s

    ORDER BY public."PPMP_orderdetails".id''', (orderdetails_id,))

    row = cur.fetchone()
    lst1 = list(row)
    #     while row is not None:
    # #         lst1.append(list(row))
    #         lst1 = list(row)
    # #         row = cur.fetchone()

    item_ = " ".join(lst1[0:5])
    item_ = item_.replace('None', '')
    item_ = re.sub(' +', ' ', item_)
    item_ = item_.strip()
    item_
    return (item_, sum(lst1[-4:]), sum(lst1[-4:]) * lst1[7], lst1[6],lst1[7])



