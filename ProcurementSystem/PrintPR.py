
import psycopg2
import re
import pandas as pd 
import pdfkit
import qrcode
from datetime import date
import datetime
import calendar


def print_pr(orderdetails_id, item_description, quantity, unit_cost, total_cost, unit,specifications,purpose,id):
    specifications = specifications.replace('\r\n', '<br/>')
    qr = qrcode.QRCode(
        version=1,
        box_size=5,
        border=5)
    qr.add_data(id)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('qrcode001.png')
    html_string = '''

    <html>
      <head>
      <title>HTML Pandas Dataframe with CSS</title>
       <meta name="pdfkit-page-size" content="Legal"/>
       <meta name="pdfkit-orientation" content="Landscape"/>
      </head>
      <link rel="stylesheet" type="text/css" href="style_pr.css"/>

      <body>

        <table>
        <tbody>
        <tr>
        <td id = "fifteen" >
         Stock/ Property No.
       </td>
        <td id = "ten">Unit </td>
        <td id ="item_description"> Item Description </td>
        <td id ="ten">Quantity</td>
        <td id ="fifteen">Unit Cost</td>
        <td id = "ten">Total Cost</td>
        </tr>

        <tr>
        <td id = "fifteen">
        <br/><br/>
        </td>
        <td id ="ten"><br/>{unit}<br/><br/> </td>
        <td id="item_description"> 
        <br/><b>{item_description}</b><br/>
        {specifications}<br/><br/>
        </td>
        <td id ="ten"> <br/>{quantity}<br/><br/></td>
        <td id ="fifteen"> <br/>{unit_cost}<br/><br/> </td>
        <td id ="ten"> <br/>{total_cost}<br/><br/> </td>
        </tr>
        
        
        
        
        
        </tbody>
        </table>

        <table>
        <tbody>
        
        <tr>
        <td id = "fifteen">
        </td>
        <td id ="ten"> </td>
        <td id="total"> 
        <b>TOTAL</b>
        </td>
        <td id ="ten"> </td>
        <td id ="fifteen">  </td>
        <td id ="ten"> {total_cost} </td>
        </tr>
        </tbody>
        </table>
        <table>
        <tbody>
        <tr><td id ="purpose">
        &nbsp;&nbsp;&nbsp;Purpose: <br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{purpose}
        </td></tr>
        </tbody>
        </table
    </html>
    '''

    with open('df.html', 'w') as f:
        f.write(html_string.format(specifications=specifications, item_description=item_description, quantity=quantity,
                                   unit_cost=unit_cost, total_cost=total_cost, unit=unit,purpose=purpose))
    # new_message = message.format(URL=a)
    path_wkhtmltopdf = r'media\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        "enable-local-file-access": None,
        "orientation": "portrait",
        "--header-html": "header_pr.html"
    }

    pdfkit.from_file("df.html", "print_pr.pdf", configuration=config, options=options)

