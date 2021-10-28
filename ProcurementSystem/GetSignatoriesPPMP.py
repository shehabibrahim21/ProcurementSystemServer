
from config import config
import psycopg2
import re


def get_signatories_ppmp(cc_name):
    signatories_needed = ['Chancellor', 'Acting Head, Budget Management Office', 'Director of Research']
    if cc_name in ['SCS Fiduciary (Cont)', 'SCS-Fiduciary', 'SCS (Continuing)', 'SCS Graduate',
                   'College of Computer Studies']:
        signatories_needed.append('Financial Assistant of CCS')
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    lst1 = []
    # year = get_year()[0]
    dct = {}
    for i in signatories_needed:
        cur.execute('''SELECT public."PPMP_signatories".name

        FROM public."PPMP_signatories" 
        JOIN public."PPMP_signatories_position" ON
        public."PPMP_signatories".position_id_id = public."PPMP_signatories_position".id
        where "PPMP_signatories_position".name = %s ''', (str(i),))

        row = cur.fetchone()

        while row is not None:
            #             lst1.append(list((row,i)))
            dct[i] = row[0]
            row = cur.fetchone()

    #         lst_fin.append(lst1[-1][0])

    return dct

def get_signatories_ap():
    signatories_needed = ['Chancellor', 'Head, PSD/ Bac Secretariat', 'BAC, Chairperson']

    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    lst1 = []
    # year = get_year()[0]
    dct = {}
    for i in signatories_needed:
        cur.execute('''SELECT public."PPMP_signatories".name

        FROM public."PPMP_signatories" 
        JOIN public."PPMP_signatories_position" ON
        public."PPMP_signatories".position_id_id = public."PPMP_signatories_position".id
        where "PPMP_signatories_position".name = %s ''', (str(i),))

        row = cur.fetchone()

        while row is not None:
            #             lst1.append(list((row,i)))
            dct[i] = row[0]
            row = cur.fetchone()

    #         lst_fin.append(lst1[-1][0])

    return dct
