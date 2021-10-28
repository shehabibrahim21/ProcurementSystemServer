#!/usr/bin/env python
# coding: utf-8

# In[ ]:





def print_rfq(fs_name,yr,type,remarks,cat_name,cat_code,lst_god,cc_code,cc_name,ppmp,lst_signatories,first_name,last_name):


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
                                   total_amount =total_amount,fq=fq,sq=sq,tq=tq,frq=frq,signatory1 =first_signatory.upper(),signatory2 = lst_signatories[1],signatory4 = lst_signatories[3],signatory5 = lst_signatories[4], date_now = date_now))
   # new_message = message.format(URL=a)
    path_wkhtmltopdf = r'media\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        "enable-local-file-access": None,
        "orientation":"landscape"
    }


    pdfkit.from_file("df.html", "print_ppmp.pdf", configuration=config, options=options)

