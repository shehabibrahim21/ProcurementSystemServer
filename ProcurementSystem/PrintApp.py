#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import psycopg2
import re
import pandas as pd 
import pdfkit

import qrcode
# Link for website

from datetime import date
import datetime
import calendar

def get_id(desc):
    conn = psycopg2.connect(host="localhost", database="hr_database", user="postgres", password="Bankai21")
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
    conn = psycopg2.connect(host="localhost", database="hr_database", user="postgres", password="Bankai21")
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

def get_id_app(source_of_fund, category, type_, year):
    catid = get_id(category)
    sofid = sof_get_id(source_of_fund)
    conn = psycopg2.connect(host="localhost", database="hr_database", user="postgres", password="Bankai21")
    cur = conn.cursor()

    cur.execute('''SELECT id FROM public."PPMP_app" where catcode = %s and sof = %s and type = %s and year = %s''',
                (int(catid), int(sofid), str(type_), int(year)))

    row = cur.fetchone()
    lst1 = []
    if row is not None:
        return row[0]
        cur.close()



def print_app(lst,cat_val,yr_val,type_val,sof_val,qrtr_val,app_id,dct_signatories):

    # id_app = get_id_app(sof_val, cat_val, type_val, yr_val)
    cat_id = get_id(cat_val)
    lst_new = []
    for i in lst:
        # del i[6]
        i.append(' ')
        lst_new.append(i)


    print("lst_new",lst_new)
    total_amount = 0

    for i in lst_new:
        total_amount = total_amount + int(i[5])
    input_data = app_id
    print("APP_ID: ",input_data)
    # Creating an instance of qrcode
    qr = qrcode.QRCode(
        version=1,
        box_size=5,
        border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('qrcode001.png')
    # print("PRINT!!!!!!!!!!!!!!")
    # print(lst_god)

    df = pd.DataFrame(lst_new,columns=[['No.','Item Description','Unit','Unit Price','Quantity','Amount','PMO/End-User','Mode of Procurement']])
    html = df.to_html()

    my_date = date.today()
    weekday = calendar.day_name[my_date.weekday()]
    date_now = weekday + " , " + my_date.strftime("%d %b %Y") + " " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute)


    html_string = '''

    <html>
      <head>
      <title>HTML Pandas Dataframe with CSS</title>
       <meta name="pdfkit-page-size" content="Legal"/>
       <meta name="pdfkit-orientation" content="Landscape"/>
      </head>
      <link rel="stylesheet" type="text/css" href="style_app.css"/>

      <body>

       
       <div class="container" >
        <div class="image" style=" display: inline-block;">
        
        <img src="msuiit1.jpg" style="width:150px;height:150px;">
        </div>
        
        <div class="text"  style=" display: inline-block;">
        Mindanao State University <br/>
        ILIGAN INSTITUTE OF TECHNOLOGY <br/>
        <i>A.Bonifactio Ave., Iligan City</i><br/><br/>
        <b>ANNUAL PROCUREMENT PLAN </b><br/>
        {sof_val} for {qrtr_val} ({type_val})<br/>
        {cat_val} ({cat_id})<br/><br/>
        
        </div>
        
      
        </div>
        
        <div class = "float_right">
        <img src="qrcode001.png" alt="">
        </div>
       
       
         <br/><br/><br/><br/>
        {table}
         <br/>
        <table id= "table_bottom">

        <tr id ="blank_row">
        <td id ="blank">&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp;</td> 
        <td id ="blank">&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp;</td> 
        <td id ="blank">&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp;</td> 
        <td id ="blank">&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp;</td> 
        <td id = "blank"><b>Grand Total </b></td>
        <td id = "blank"><b>{total_amount}</b></td>
        <td id ="blank">&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp;</td> 
        <td id ="blank">&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp;</td>         
        </tr>
        </table>
                                       
        <div id ="bottom">
        
        <div id="block">
        Prepared by:
       
        <p  style="text-align:center;"><u>{signatory1}</u></p>
      
        <p  style="text-align:center;"> 'Head, PSD/ Bac Secretariat' </p>
         
        </div>

        <div id="block">
        <br/>
       
        <p  style="text-align:center;"><u>{signatory2}</u></p>
      
        <p  style="text-align:center;"> 'BAC, Chairperson' </p>
         
        </div>
        

        
        <div id="block">
        <br/>
       
        <p  style="text-align:center;"><u>{signatory3}</u></p>
      
        <p  style="text-align:center;"> Chancellor</p>
         
        </div>
        
       
                                       
        </div>
      </body>
    </html>
    '''



    with open('df.html', 'w') as f:
        f.write(html_string.format(table=df.to_html(classes='table-style',index=False),sof_val=sof_val,type_val=type_val,cat_val=cat_val,cat_id=cat_id,qrtr_val=qrtr_val,total_amount =    f'{float(total_amount):,}',

                                   signatory1=dct_signatories['Head, PSD/ Bac Secretariat'].upper(),
                                   signatory2=dct_signatories['BAC, Chairperson'].upper(),
                                   signatory3=dct_signatories['Chancellor'].upper(),


                                   ))
   # new_message = message.format(URL=a)
    path_wkhtmltopdf = r'media\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        "enable-local-file-access": None,
        "orientation":"landscape"
    }


    pdfkit.from_file("df.html", "print_app.pdf", configuration=config, options=options)

