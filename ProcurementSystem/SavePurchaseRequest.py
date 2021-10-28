from config import config
from datetime import datetime
import psycopg2
def get_last_value():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    cur.execute('''SELECT MAX(id) FROM public."PPMP_purchaserequest"''')
    

    row = cur.fetchone()
    while row is not None:
        return row[0]
        row = cur.fetchone()
  
    cur.close()



def purchase_request(specification_details,purpose,orderdetails_id_id):
    dateTimeObj = datetime.now()
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    id_ = get_last_value()
    if id_ is None:
        id_ = 0
    else:
        id_ = int(id_) + 1
    sql = """INSERT INTO public."PPMP_purchaserequest"(id, specification_details,purpose,
    date_created,orderdetails_id_id) VALUES(%s,%s,%s,%s,%s);"""

    try:
        cur.execute(sql, (id_, specification_details,purpose,datetime.now() ,orderdetails_id_id))
        #             cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        

