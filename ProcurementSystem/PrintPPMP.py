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
# from datetime import datetime

import datetime
import pandas as pd
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


def lst_item_no(lst):
    lst_new = []
    lst_new.append(" ")
    lst_new.append(" ")
    ii = 1
    #     print(lst)
    for i in lst:
        p = 0
        for u in i[1:7]:
            if p == 0:
                lst_new.append(" ")
                lst_new.append(ii)
            elif u != 'None':
                lst_new.append(" ")
            p = p + 1
        ii = ii + 1
    lst_new.append(" ")
    lst_new.append(" ")
    return lst_new


def lst_qty(lst):
    lst_new = []
    lst_new.append(" ")
    lst_new.append(" ")
    quarter = determine_quarter()
    # print("SUlod", lst,"   end")
    for i in lst:
        # print("awww", i)
        p = 0
        for u in i[1:7]:
            # print("awww" ,i)
            if p == 0:
                lst_new.append(" ")
                if quarter == 'First Quarter':
                    lst_new.append(i[7])
                elif quarter == 'Second Quarter':
                    lst_new.append(i[8])
                elif quarter == 'Third Quarter':
                    lst_new.append(i[9])
                elif quarter == 'Fourth Quarter':
                    lst_new.append(i[10])
            elif u != 'None':
                lst_new.append(" ")
            p = p + 1
    lst_new.append(" ")
    lst_new.append(" ")
    return lst_new


def lst_unit(lst):
    lst_new = []
    lst_new.append("For:")
    lst_new.append(" ")
    for i in lst:

        p = 0
        for u in i[1:7]:
            if p == 0:
                lst_new.append(" ")
                lst_new.append(i[12])
            elif u != 'None':
                lst_new.append(" ")
            p = p + 1
    lst_new.append(" ")
    lst_new.append(" ")
    return lst_new


def lst_particulars(lst):
    lst_new = []
    category = lst[0][0]
    lst_cost_center = []
    for i in lst:
        if "and+" in i[-2]:
           lst_cc = i[-2].split("and+")
           for i in lst_cc:
               if i not in lst_cost_center:
                   lst_cost_center.append(i)
        elif i[-2] not in lst_cost_center:
            lst_cost_center.append(i[-2])
    cost_center = ", ".join(lst_cost_center)

    lst_new.append(cost_center )
    str_ = "     "  + category
    lst_new.append(str_)
    for i in lst:
        lst_new.append(" ")
        for u in i[1:7]:
            if u != 'None':
                lst_new.append(u)
    lst_new.append(" ")
    lst_new.append("")
    return lst_new


def lst_approved_unit_abc(lst):
    lst_new = []
    lst_new.append(" ")
    lst_new.append(" ")
    quarter = determine_quarter()
    sum_ = 0
    for i in lst:
        # f"{num:,}"
        p = 0
        for u in i[1:7]:
            if p == 0:
                lst_new.append(" ")
                if quarter == 'First Quarter':
                    sum_ = sum_ + float(i[7]) * float(i[11])
                    float_ = float(i[7]) * float(i[11])
                    float_ = f"{float_:,}"
                    lst_new.append(float_)
                elif quarter == 'Second Quarter':
                    sum_ = sum_ + float(i[8]) * float(i[11])
                    float_ = float(i[8]) * float(i[11])
                    float_ = f"{float_:,}"
                    lst_new.append(float_)
                elif quarter == 'Third Quarter':
                    sum_ = sum_ + float(i[9]) * float(i[11])
                    float_ = float(i[9]) * float(i[11])
                    float_ = f"{float_:,}"
                    lst_new.append(float_)
                elif quarter == 'Fourth Quarter':
                    sum_ = sum_ + float(i[10]) * float(i[11])
                    float_ = float(i[10]) * float(i[11])
                    float_ = f"{float_:,}"
                    lst_new.append(float_)
            elif u != 'None':
                lst_new.append(" ")
            p = p + 1
    lst_new.append(" ")
    lst_new.append("Total : " + f"{sum_:,}")
    return lst_new


def blank_list(lst):
    lst_new = []
    for i in lst:
        lst_new.append(" ")
        for u in i[1:7]:
            if u != 'None':
                lst_new.append(" ")
    lst_new.append(" ")
    lst_new.append(" ")
    lst_new.append(" ")
    lst_new.append(" ")
    return lst_new




def print_ppmp(fs_name,yr,type,remarks,cat_name,cat_code,lst_god,cc_code,cc_name,ppmp,dct_signatories,first_name,last_name):


    lst_new = []
    total_amount = 0
    fq = 0
    sq = 0
    tq = 0
    frq = 0
    for i in lst_god:
        lst_new.append([i[2], i[1],i[3], i[4]+i[6]+i[8]+i[10],i[3] * (i[4]+i[6]+i[8]+i[10]),i[4],i[3]*i[4], i[6],i[3]*i[6],i[8],i[3]*i[8],i[10],i[3]*i[10] ])
        total_amount = total_amount + (i[3] * (i[4]+i[6]+i[8]+i[10]))
        fq = fq + i[3]*i[4]
        sq = sq + i[3]*i[6]
        tq = tq + i[3]*i[8]
        frq = frq + i[3]*i[10]
    total_amount = float("{:.2f}".format(total_amount))
    fq = float("{:.2f}".format(fq))
    sq = float("{:.2f}".format(sq))
    tq = float("{:.2f}".format(tq))
    frq = float("{:.2f}".format(frq))
    input_data = ppmp
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

    df = pd.DataFrame(lst_new,columns=[[' ','DETAILS','UNIT','TOTAL','TOTAL','FIRST QUARTER','FIRST QUARTER','SECOND QUARTER','SECOND QUARTER','THIRD QUARTER','THIRD QUARTER',
                                        'FOURTH QUARTER','FOURTH QUARTER'],
        ['Unit','(Nomenclature & Description) ','PRICE','QTY','AMOUNT','QTY','AMOUNT','QTY','AMOUNT',
                                       'QTY','AMOUNT','QTY','AMOUNT']])
    name_csv = "ppmp_"+ str(cat_name) +"_"+ str(cc_name) +"_"+ str(yr) +"_.csv"
    df.to_csv(name_csv)
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
      <link rel="stylesheet" type="text/css" href="style.css"/>

      <body>

        <div id="wrapper">
          <div id="first">
          MSU - Iligan Institute of Technology <br><br>
          OFFICE OF THE BAC SECRETARIAT (OBS)<br/>
          Tel. No. (063) 225-4926 <br><br>

          PROJECT PROCUREMENT MANAGEMENT PLAN, {yr} <br/>
          Cost Center: <u><b>{cc_code}</b></u> &nbsp; &nbsp;&nbsp; <u><b>{cc_name}</b></u><br/>
          Source of Fund: <u><b>{fs_name}</b></u><br/>
          PPMP ID: {ppmp}&nbsp; &nbsp;&nbsp;{type}<br/>
          Account Code:{cat_code}&nbsp; &nbsp;&nbsp;{cat_name}
          </div>
          <div id="second">
        <img src="qrcode001.png" alt="">
          </div>
          <div id="third">
         
       
      <img src="msuiit.jpg" style="width:150px;height:150px;">
          </div>

        </div>
        <br/>
        <div id = "date_info"> {date_now}</div>
        {table}
     
        <div>
       
        <table id = "table_bottom">

        <tr>
        <td id ="blank">&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp;</td> 
        <td id ="running_total"> Running Total >></td>
        <td id = "total_amount">&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; </td>
        
        <td >&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp;</td>
        <td >{total_amount}</td>
        <td >&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; </td>
        <td ">{fq} </td>
        <td >&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; </td>
        <td ">{sq}</td>
        <td "> &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp;</td>
        <td >{tq} </td>
        <td >&nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; </td>
        <td >{frq}</td>
        </tr>
        </table>
        </div>
        <br/>
        <br/>
        <div id ="bottom">
        
        <div id="block">
        Prepared by:
       
        <p  style="text-align:center;"><u>{signatory1}</u></p>
      
        <p  style="text-align:center;"> Financial Assistant </p>
         
        </div>

        <div id="block">
        <br/>
       
        <p  style="text-align:center;"><u>{signatory2}</u></p>
      
        <p  style="text-align:center;"> Director of Research </p>
         
        </div>
        

        
        <div id="block">
        <br/>
       
        <p  style="text-align:center;"><u>{signatory4}</u></p>
      
        <p  style="text-align:center;"> Acting Head, Budget Management Office</p>
         
        </div>
        
        <div id="block">
        Approved by:
       
        <p  style="text-align:center;"><u>{signatory5}</u></p>
      
        <p  style="text-align:center;"> Chancellor</p>
         
        </div>
                                       
        </div>
      </body>
    </html>
    '''

    first_signatory = first_name + " " + last_name

    with open('df.html', 'w') as f:
        f.write(html_string.format(table=df.to_html(classes='table-style',index=False),yr = yr,cc_code=cc_code,cc_name=cc_name,fs_name=fs_name,ppmp=ppmp,type=type,cat_code = cat_code,cat_name=cat_name,
                                   total_amount =total_amount,fq=fq,sq=sq,tq=tq,frq=frq,
                                   signatory1 =dct_signatories['Financial Assistant of CCS'].upper(),
                                   signatory2 =dct_signatories['Director of Research'].upper(),
                                   signatory4 = dct_signatories['Acting Head, Budget Management Office'].upper(),
                                   signatory5 = dct_signatories['Chancellor'].upper(),
                                   date_now = date_now))
   # new_message = message.format(URL=a)
    path_wkhtmltopdf = r'media\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        "enable-local-file-access": None,
        "orientation":"landscape"
    }


    pdfkit.from_file("df.html", "print_ppmp.pdf", configuration=config, options=options)


# !/usr/bin/env python
# coding: utf-8

# In[ ]:


def print_rfq(lst):
    date_ = str(datetime.datetime.now()).split(' ')[0]
    # lst = get_group_details_combined(14)
    df = pd.DataFrame({'Item No.': lst_item_no(lst),
                       'Qty': lst_qty(lst),
                       'Unit': lst_unit(lst),
                       'PARTICULARS': lst_particulars(lst),
                       'Approved Unit ABC': lst_approved_unit_abc(lst),
                       'Unit Price': blank_list(lst),
                       'Total Price': blank_list(lst),
                       })
    html = df.to_html().replace("\\n","<br>")
    html_string = '''

    <html>
      <head>
      <title>HTML Pandas Dataframe with CSS</title>
       <meta name="pdfkit-page-size" content="Legal"/>
       <meta name="pdfkit-orientation" content="Landscape"/>
      </head>
      <link rel="stylesheet" type="text/css" href="style_rfq.css"/>

      <body>
    <div id = "main_div">

    
    <div id ="logo">
      <img src="msuiit4.jpg" style="width:150px;height:150px;">
    </div>
    <div id = "iit_details">
    Republic of the Philippines <br/>
    Mindanao State University <br/>
    ILIGAN INSTITUTE OF TECHNOLOGY <br/>
    Andres Bonifacio Ave. Iligan City <br/>
    Telefax #(063) 221-4059
    </div>
    
        <div id = "right_div">
        <table id = "table1">
        <tr>
        <td>RFQ No.:</td>
        <td>____________________</td>
        </tr> 
        <tr>
        <td>Date:</td>
        <td><u>{date_}</u></td>
        </tr> 
        <tr>
        <td>PR/ JOR No.:</td>
        <td>____________________</td>
        </tr> 
        <tr>
        <td>BAC-RES No.:</td>
        <td>____________________</td>
        </tr> 
        <tr>
        <td>App No.:</td>
        <td>____________________</td>
        </tr> 
        <tr>
        <td>PPMP ID:</td>
        <td>____________________</td>
        </tr> 
        <tr>
        <td>Mode of Proc:</td>
        <td>____________________</td>
        </tr> 
        <tr>
        <td>Fund Source:</td>
        <td>____________________</td>
        </tr> 
        </table>
    </div>
    
 <div id ="suppliers_name">
<table id = "table1">
 <tr>
 <td> ____________________________________<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Supplier's name
 </td></tr>
 <tr>
  <td> ____________________________________<br/>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Address/ Contact #
 </td>
 </tr>

 </table>
 <br/>
 <b> Gentlemen:</b><br/>
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The MSU-IIT has a requirement for the following: 
 
  </div>
 
 <br/>  
    </div>

        <div id ="main_table">
       
       {table}
      
       <p id ="term1">
       
       Delivery Term: 30 Calendar Days upon receipt of P.O.
       </p>
       <p id ="term2">
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Note:  1.)Total Offer should not exceed Approved Budget for the Contract,otherwise considered non-responsive.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.) Award should be given on ( ) Lot Basis/ ( ) per item Basis. <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.) Please indicate <b> BRAND </b> when applicable.
       </p>

 <p id ="term2">
 
 The Value-Added Tax of 5% plus 1% (supplies/ materials), or 5% plus 2% (services) income payment/s made by a 
 government office shall be deducted and withheld on gross playment of purchase/s-R.A. 7649 NIR/RR No. 10-92
 No. 12-94.
 </p>
 <p id ="term4">
 
Please quote your lowest government price stating the number of days within which you can make delivery and the
number of days by which your price will hold through. Any alteration/ erasure in your quotation shall be properly
initialed. The Bid/ Canvass will be opened at 10:00 am on _______________ 2021. <b>You are request d to return this 
quotation in a sealed envelope not later than the above scheduled date.</b> Said quotation must be dropped in the 
bid box at the BAC Secretariate of the Institute. MSU-IIT reserves the right to reject any or all offers that 
maybe considererd most advantageous to the Institute.
 </p>
 
 <div id = "bot_left">
<br/><br/>
________________________________<br/>
<b>Name & Signature of Canvasser</b>

<br/>
<br/>
<br/>
<br/>
SUPPLIER: ________________________________<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Signature Over Printed Name</b>
 <br/>
 Contact No.: ________________________________<br/>
&nbsp;&nbsp;&nbsp;e-mail add: ________________________________
 
 </div>
 
 <div id = "bot_right">
 Very truly yours, <br/>
 <b>MSU- Iligan Insitute of Technology</b>
 <br/><br/><br/><br/><br/>
 <br/>
 <u><b>KRISTELA DIANA MAY R. DELA RAMA </b></u>
 <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Cost Center Head
 </div>
 
 </div>
      </body>
    </html>
    '''



    with open('df.html', 'w') as f:
        f.write(html_string.format(table=df.to_html(classes='table-style',index=False),date_=date_))


    # new_message = message.format(URL=a)
    path_wkhtmltopdf = r'media\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        "enable-local-file-access": None
    }

    pdfkit.from_file("df.html", "print_rfq.pdf", configuration=config, options=options)

