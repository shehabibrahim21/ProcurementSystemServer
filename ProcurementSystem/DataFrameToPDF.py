#!/usr/bin/env python
# coding: utf-8

# In[1]:



import numpy as np
from jinja2 import Environment, FileSystemLoader
import psycopg2
import re
import pandas as pd
from pandas import DataFrame
import pdfkit as pdf
from config import config

# In[ ]:


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
#     print(lst2)
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


# In[ ]:


def convert_pdf(ppmp_id,year,code,cost_center,source_fund,type_,acc_code,acc_name):
    lst = get_order_details_all(ppmp_id)
    header = ['Code','Description','Unit','Unit Price','1st Qrtr Qty','1st Qrtr Amount','2nd Qrtr Qty','2nd Qrtr Amount','3rd Qrtr Qty','3rd Qrtr Amount','4th Qrtr Qty','4th Qrtr Amount'] 
    df = pd.DataFrame( columns = header, data = lst )
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("template.html")
    template_vars = {"title" : "Project Procurement Management Plan",
                    "year":year,
                     "code":code,
                     "cost_center":cost_center,
                     "source_fund":source_fund,
                     "ppmp_id":ppmp_id,
                     "type":type_,
                     "acc_code":acc_code,
                     "acc_name":acc_name
                    
                    
                    }
    html_out = template.render(template_vars)
    
    directory="http://192.168.1.2:8000/media/"
    onedrive= "http://192.168.1.2:8000/media/"

    path_wkhtmltopdf = "http://192.168.1.2:8000/media/wkhtmltopdf/bin/wkhtmltopdf.exe"


    config=pdf.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header' : [        ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ],
    'no-outline': None,
    'orientation':'Landscape'
    }   
    
    

    # assign the html file location into html_file
    html_file = directory+'template.html'

    # assign the pdf file one drive location into pdf_file
    pdf_file = onedrive+'template.pdf'

    # make the index start from 1 instead of 0
    # dataframe = dataframe.reset_index()
    # dataframe.index += 1

    # # drop a column name 'index'
    # dataframe=dataframe.drop(columns=['index'])

    # convert data frame into html format
    df_to_html = df.to_html()


    html_out = template.render(template_vars)

    # open the html file and put the newly rendered html in it
    with open(html_file, "w") as file:
        file.write(html_out)

    # convert html to pdf

    pdf.from_file(html_file,pdf_file,configuration=config,options=options)

    

