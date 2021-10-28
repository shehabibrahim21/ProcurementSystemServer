
import psycopg2
import re
import pickle
from config import config
def get_specifics():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT genericname, specifics1, specifics2, specifics3, specifics4,specifics5
                FROM public."Item" LEFT JOIN public."Specifications" ON 
                public."Item".specificscode = public."Specifications".specificscode 
                ''')

    row = cur.fetchone()
    lst = []
    while row is not None:
        str1 = " ".join(list(row))
        str1 = re.sub(' +', ' ', str1)
        str1 = " __ " + str1
        if str1 not in lst:
            lst.append(str1)
        row = cur.fetchone()
    cur.close()

    with open('dct_syn.pickle', 'rb') as handle:
        dct_syn = pickle.load(handle)

    for val in dct_syn.values():
        str_ = " __ " + " ".join(val)
        lst.append(str_)

    return lst


def get_specifics_cleaned():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute('''SELECT genericname, specifics1, specifics2, specifics3, specifics4,specifics5
                FROM public."Item" LEFT JOIN public."Specifications" ON 
                public."Item".specificscode = public."Specifications".specificscode 
                ''')

    row = cur.fetchone()
    lst = []
    while row is not None:
        str1 = " ".join(list(row))
        str1 = re.sub(' +', ' ', str1)
        str1 = " __ " + str1
        if str1 not in lst:
            lst.append(str1)
        row = cur.fetchone()
    cur.close()

    with open('dct_syn.pickle', 'rb') as handle:
        dct_syn = pickle.load(handle)

    for val in dct_syn.values():
        str_ = " __ " + " ".join(val)
        lst.append(str_)


    lst = [word.replace("("," ") for word in lst]
    lst = [word.replace(")"," ") for word in lst]

    return lst

