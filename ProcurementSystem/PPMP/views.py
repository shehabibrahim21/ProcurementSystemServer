from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question


from PPMP.forms import SearchCostCenterForm
from PPMP.forms import SearchItemsForm
from PPMP.forms import SearchQuarterForm
from PPMP.forms import SearchCategoryForm
from PPMP.forms import PriceRequestForm
from PPMP.forms import CommentRequestForm
from PPMP.forms import UnitRequestForm
from PPMP.forms import SOFForm
from PPMP.forms import CATForm
from PPMP.forms import YRForm
from PPMP.forms import TypeForm
from PPMP.forms import PriceSuggestedForm
from PPMP.forms import UnitSuggestedForm
from PPMP.forms import QuarterForm
from PPMP.forms import DynamicForm
from PPMP.forms import PurposeForm
from PPMP.forms import PriceForm
from PPMP.forms import SearchGroupForm
from PPMP.forms import GroupForm
from PPMP.forms import SpecificationDetailsForm
from PPMP.forms import CCForm


from PPMP.forms import CostCenterCode
from PPMP.forms import CostCenterName
from PPMP.forms import YearForm
from PPMP.forms import CategoryForm
from PPMP.forms import SearchItemForm
from PPMP.forms import Specifics1
from PPMP.forms import Specifics2
from PPMP.forms import Specifics3
from PPMP.forms import Specifics4
from PPMP.forms import Specifics5
from PPMP.forms import Quarter1
from PPMP.forms import Quarter2
from PPMP.forms import Quarter3
from PPMP.forms import Quarter4
import SavePurchaseRequest as spr
import DataFrameToPDF as dftp
import CheckTempOrder as cto
import GetAPPValues as gav
import CreateReports as  cr
import InputCleaning as  ic
import GetItemsList as gil
import RetrieveSpecifications as rs
import GetDetails as gd
import GetPPMP as gp
import GetCostCenters as gc
import GetCategory as gcat
import CheckIfExists as cie
import EditItems as ei
import InsertOrderDetails as iod
import InsertTempOrderDetails as itod
import GetOrderDetails as god
import GetOrderDetails2 as god2
import PrintPPMP as pp
import PrintApp as ap
import PrintPR as ppr
import GetSignatoriesPPMP as gsp
import GetOrderDetailsPR as godpr
import ShowPR as showpr
import UnsetPrice as usp
import SetNewPrice as snp
import GetItemsAll as gia
import DelOrderDetails as dod
import ShowListOrderDetails as slod
import SaveGroup as sg
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from HR.forms import SearchForm
import numpy as np
import GetCategoryCode as gcc
import CombineItem as ci
import re

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

lst_num = list(np.arange(0, 99999))
lst_num = [str(i) for i in lst_num]
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
class GlobalVariables():
    ppmp = ''
    ppmp_id = ''
    ppmp_create_id = ''
    item_id = ''
    item_orderdetails_id = ''
    price_id = ''
    cc_code = ''
    cc_name = ''
    fs_name = ''
    yr = ''
    type = ''
    remarks = ''
    lst_ppmp = ''
    lst_ppmp_id = ''
    cat_code = ''
    cat_name = ''
    categories = ''
    lst_god = ''
    prev_mdal = ''
    lst_to_add = ''
    gen_to_add = ''
    specs_to_add = ''
    with_req = ''
    lst_cc = ''
    temp_id =''
    item_name = ''
    date_temp_order_details = ''
    temp_order_details = ''
    lst_app = ''
    cat_val = ''
    yr_val = ''
    type_val = ''
    sof_val = ''
    qrtr_val =  ''
    item_description = ''
    quantity = ''
    unit_cost= ''
    total_cost = ''
    unit = ''
    specifications = ''
    purpose = ''
    app_id = ''
    pr_id = ''
    fqy = 0
    sqy = 0
    tqy = 0
    frqy = 0
    item_description = ''
    dct_items  = {}
    temp_group_items = []
@login_required
def index(request):

    user = request.user
    print('user: ',user)
    GlobalVariables.with_req = cto.check_temp_order()
    GlobalVariables.lst_cc = gc.get_cost_centers(user)
    print(GlobalVariables.lst_cc)
    context = {
        'lst_cc': GlobalVariables.lst_cc,
        'modal_type': 'Zero',
        'with_requests': GlobalVariables.with_req
    }
    return render(request, 'PPMP/index.html', context)
@csrf_exempt
def saveprice(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')

    print("III",id,type,value)
    snp.set_new_price(id,type,value)
    return


@csrf_exempt
def editorderdetails(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')

    print("III",id,type,value)
    if type == 'item_description':
        snp.edit_order_details(id, GlobalVariables.dct_items[value], type)
    else:
        snp.edit_order_details(id, value, type)
    print(GlobalVariables.dct_items)
    return




@csrf_exempt
def saveorderdetails(request):
    # id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    value_des=request.POST.get('value_des','')
    # GlobalVariables.ppmp
    # print("III",id,type,value)
    # snp.set_new_price(id,type,value)
    print("AWWW",type,value,value_des,GlobalVariables.ppmp)
    if type == 'fq_qty':
        GlobalVariables.fqy = value
    elif type == 'sq_qty':
        GlobalVariables.sqy = value
    elif type == 'tq_qty':
        GlobalVariables.tqy = value
    elif type == 'frq_qty':
        GlobalVariables.frqy = value

    GlobalVariables.item_description = value_des
    return
@csrf_exempt
def savetempgroup(request):
    id = int(request.POST.get('id', ''))
    GlobalVariables.temp_group_items.append(id)
    print(GlobalVariables.temp_group_items)
@csrf_exempt
def removetempgroup(request):
    id = int(request.POST.get('id', ''))
    GlobalVariables.temp_group_items.remove(id)
    sg.delete_group(id)
    print(GlobalVariables.temp_group_items)

def create_rfq(request,parameter):
    groupform  = GroupForm(request.POST)
    context = {
    'groupform': groupform,
    'modal_type':'One',
    'all_group': sg.get_group_app(),
    }
    return render(request, 'PPMP/create_rfq.html',context)


def group_items(request,parameter):
    GlobalVariables.temp_group_items = []
    lst = slod.show_list()
    print(lst)

    context = {
    'all_group': sg.get_group_app(),
    'set_group':False,
    'list': lst,
    'modal_type': 'One',
     'searchgroupform': SearchGroupForm(initial={'name':'test'}),
    }
    return render(request, 'PPMP/group_items.html', context)

def set_group(request,parameter):
    print(GlobalVariables.temp_group_items)
    sg.set_group(GlobalVariables.temp_group_items)
    GlobalVariables.temp_group_items = []
    lst = slod.show_list()

    context = {
    'all_group': sg.get_group_app(),
    'searchgroupform': SearchGroupForm(initial={'name':'test'}),
    'set_group':False,
    'list': lst,
    # 'list_group': lst_group,
    'modal_type': 'One',
    }
    return render(request, 'PPMP/group_items.html', context)

def change_group(request,parameter):
    # sg.set_group(GlobalVariables.temp_group_items)
    # print(lst)
    group_id= str(request.POST.get('searchgroupform')).split(' ')[1]
    GlobalVariables.temp_group_items = sg.get_app_id(group_id)
    # GlobalVariables.temp_group_items.append(int(group_id))
    # print("GROUP ID ",group_id)

    lst = slod.show_list()
    lst_group = slod.show_list_group(group = str(group_id))
    # lst_group
    context = {
    'all_group': sg.get_group_app(),
    'searchgroupform': SearchGroupForm(initial={'name':'test'}),
    'set_group':True,
    'list': lst,
    'list_group': lst_group,
    'modal_type': 'One',
    }
    return render(request, 'PPMP/group_items.html', context)


def edit_items_delete(request,parameter):

    dod.delete_oder_details(int(parameter))
    
    GlobalVariables.with_req = cto.check_temp_order()
    categoryform = CategoryForm(request.POST)
    catform = CATForm(request.POST)
    print(GlobalVariables.lst_ppmp_id)
    categories = gcat.get_categories()
    GlobalVariables.fs_name = GlobalVariables.lst_ppmp_id[2]
    GlobalVariables.yr = GlobalVariables.lst_ppmp_id[3]
    GlobalVariables.type = GlobalVariables.lst_ppmp_id[4]
    GlobalVariables.remarks = GlobalVariables.lst_ppmp_id[4]

    GlobalVariables.prev_mdal = 3
    with_categories = True
    cat_code = gcc.get_cat_code(GlobalVariables.cat_name)
    GlobalVariables.cat_code = cat_code
    GlobalVariables.lst_god = god.get_order_details(GlobalVariables.cat_code, GlobalVariables.ppmp_create_id)
    all_items = gia.get_items(cat_code)[1]
    all_items_price = gia.get_item_details(str(cat_code))

    context = {
        'all_items_price': all_items_price,
        'all_items':all_items,
        'with_requests': GlobalVariables.with_req,
        'show': True,
        'lst_god': GlobalVariables.lst_god,
        'cat_code': cat_code,
        'cat_name': GlobalVariables.cat_name,
        'with_categories': with_categories,
        'lst_cc': GlobalVariables.lst_cc,
        'modal_type': 'Seven',
        'with_content': False,
        'cc_code': GlobalVariables.cc_code,
        'cc_name': GlobalVariables.cc_name,
        'fs_name': GlobalVariables.fs_name,
        'yr': GlobalVariables.yr,
        'type': GlobalVariables.type,
        'remarks': GlobalVariables.remarks,
        'categoryform': categoryform,
        'catform': catform,
        "categories": categories,
        'with_requests': GlobalVariables.with_req



    }

    return render(request, 'PPMP/index.html', context)


def edit_ppmp(request,parameter):

    GlobalVariables.with_req = cto.check_temp_order()
    categoryform = CategoryForm(request.POST)
    catform = CATForm(request.POST)
    print(GlobalVariables.lst_ppmp_id)
    categories = gcat.get_categories()
    GlobalVariables.fs_name = GlobalVariables.lst_ppmp_id[2]
    GlobalVariables.yr = GlobalVariables.lst_ppmp_id[3]
    GlobalVariables.type = GlobalVariables.lst_ppmp_id[4]
    GlobalVariables.remarks = GlobalVariables.lst_ppmp_id[4]

    GlobalVariables.prev_mdal = 3
    with_categories = True
    cat_code = gcc.get_cat_code(GlobalVariables.cat_name)
    GlobalVariables.cat_code = cat_code
    GlobalVariables.lst_god = god.get_order_details(GlobalVariables.cat_code, GlobalVariables.ppmp_create_id)
    all_items = gia.get_items(cat_code)[1]
    all_items_price = gia.get_item_details(str(cat_code))

    context = {
        'all_items_price': all_items_price,
        'all_items':all_items,
        'with_requests': GlobalVariables.with_req,
        'show': True,
        'lst_god': GlobalVariables.lst_god,
        'cat_code': cat_code,
        'cat_name': GlobalVariables.cat_name,
        'with_categories': with_categories,
        'lst_cc': GlobalVariables.lst_cc,
        'modal_type': 'Seven',
        'with_content': False,
        'cc_code': GlobalVariables.cc_code,
        'cc_name': GlobalVariables.cc_name,
        'fs_name': GlobalVariables.fs_name,
        'yr': GlobalVariables.yr,
        'type': GlobalVariables.type,
        'remarks': GlobalVariables.remarks,
        'categoryform': categoryform,
        'catform': catform,
        "categories": categories,
        'with_requests': GlobalVariables.with_req



    }

    return render(request, 'PPMP/index.html', context)
def savedetails(request, parameter):
    print("sulod")
    itemdescription_id = GlobalVariables.dct_items[GlobalVariables.item_description]
    ppmp_id_id = GlobalVariables.lst_ppmp_id[0]
    price_id = iod.get_price_detail(itemdescription_id)
    print(itemdescription_id, ppmp_id_id, price_id, GlobalVariables.fqy, GlobalVariables.sqy, GlobalVariables.tqy,
                         GlobalVariables.frqy)
    iod.insert_order_details(itemdescription_id, ppmp_id_id, price_id, GlobalVariables.fqy, GlobalVariables.sqy, GlobalVariables.tqy,
                         GlobalVariables.frqy)


    GlobalVariables.with_req = cto.check_temp_order()
    categoryform = CategoryForm(request.POST)
    catform = CATForm( initial={'cat': GlobalVariables.cat_name})
    print(GlobalVariables.lst_ppmp_id)
    categories = gcat.get_categories()
    GlobalVariables.fs_name = GlobalVariables.lst_ppmp_id[2]
    GlobalVariables.yr = GlobalVariables.lst_ppmp_id[3]
    GlobalVariables.type = GlobalVariables.lst_ppmp_id[4]
    GlobalVariables.remarks = GlobalVariables.lst_ppmp_id[4]



    GlobalVariables.prev_mdal = 3
    # raw_data = request.POST.get('cat')

    # GlobalVariables.cat_name = raw_data
    with_categories = True
    cat_code = gcc.get_cat_code(GlobalVariables.cat_name)

    GlobalVariables.cat_code = cat_code
    GlobalVariables.lst_god = god.get_order_details(GlobalVariables.cat_code, GlobalVariables.ppmp_create_id)
    all_items = gia.get_items(cat_code)[1]
    # GlobalVariables.dct_items = gia.get_items(cat_code)[0]
    all_items_price = gia.get_item_details(str(cat_code))

    context = {
        'all_items_price': all_items_price,
        'all_items':all_items,
        'with_requests': GlobalVariables.with_req,
        'show': True,
        'lst_god': GlobalVariables.lst_god,
        'cat_code': cat_code,
        'cat_name': GlobalVariables.cat_name,
        'with_categories': with_categories,
        'lst_cc': GlobalVariables.lst_cc,
        'modal_type': 'Three',
        'with_content': False,
        'cc_code': GlobalVariables.cc_code,
        'cc_name': GlobalVariables.cc_name,
        'fs_name': GlobalVariables.fs_name,
        'yr': GlobalVariables.yr,
        'type': GlobalVariables.type,
        'remarks': GlobalVariables.remarks,
        'categoryform': categoryform,
        'catform': catform,
        "categories": categories,
        'with_requests': GlobalVariables.with_req



    }

    return render(request, 'PPMP/index.html', context)

def test(request,parameter):

    context = {
        'lst_cc': GlobalVariables.lst_cc,
        'modal_type': 'Zero',
        'with_requests': GlobalVariables.with_req
    }
    return render(request, 'PPMP/index.html', context)

def set_price(request,parameter):
    priceform = PriceForm(request.POST)
    context = {
    'lst_price':usp.show_unset_price(),
    'priceform':priceform


    }



    return render(request, 'PPMP/set_price.html', context)

def print_pr(request,parameter):
    # fs_name = GlobalVariables.fs_name
    # yr = GlobalVariables.yr
    # type = GlobalVariables.type
    # remarks = GlobalVariables.remarks
    # cat_name = GlobalVariables.cat_name
    # cat_code = GlobalVariables.cat_code
    # lst_god = GlobalVariables.lst_god
    # cc_code = GlobalVariables.cc_code
    # cc_name = GlobalVariables.cc_name
    # ppmp = GlobalVariables.ppmp
    # lst_signatories = gsp.get_signatories_ppmp()
    print("GlobalVariables    ",GlobalVariables.item_orderdetails_id, GlobalVariables.item_description, GlobalVariables.quantity, GlobalVariables.unit_cost, GlobalVariables.total_cost, GlobalVariables.unit,GlobalVariables.specifications)
    ppr.print_pr(GlobalVariables.item_orderdetails_id, GlobalVariables.item_description, GlobalVariables.quantity, GlobalVariables.unit_cost, GlobalVariables.total_cost, GlobalVariables.unit,GlobalVariables.specifications,
                 GlobalVariables.purpose,GlobalVariables.pr_id)
    #
    try:
        return FileResponse(open('print_pr.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def show_pr(request,parameter):
    GlobalVariables.item_orderdetails_id = int(parameter)
    lst_spr = showpr.show_pr(int(parameter))
    tup_details = showpr.get_pr_details(int(parameter))
    GlobalVariables.specifications = lst_spr[0]
    print("SPR___",lst_spr[0])
    lst_specifications = lst_spr[0].split("\r\n")
    lst_specifications = [x for x in lst_specifications if x.strip()]
    print(test)
    GlobalVariables.item_description = tup_details[0]
    GlobalVariables.quantity = tup_details[1]
    GlobalVariables.unit_cost =  tup_details[4]
    GlobalVariables.unit = tup_details[3]
    GlobalVariables.total_cost = tup_details[2]
    GlobalVariables.purpose = lst_spr[1]
    GlobalVariables.pr_id = lst_spr[2]
    context = {
    'lst_specifications':lst_specifications,
    'specification_details':lst_spr[0],
    'purpose': GlobalVariables.purpose,
    'item' : GlobalVariables.item_description,
    'qty' : GlobalVariables.quantity,
    'amt' : GlobalVariables.unit_cost,
    'unit' : GlobalVariables.unit,
    'total_amt': GlobalVariables.total_cost,


    }
    return render(request, 'PPMP/show_pr.html', context)






def view_pr(request,parameter):

    if parameter == '999991':
        lst_results = ''
        with_value = True
        cat_val =request.POST.get('cat')
        cc_val = request.POST.get('cc')
        sof_val = request.POST.get('sof')
        yr_val = request.POST.get('yr')


        sofform = SOFForm(request.POST)

        ccform = CCForm(request.POST)
        catform = CATForm(request.POST)
        yrform = YRForm(request.POST)

        print("VALUES: ",cat_val,cc_val,sof_val)
        lst_god = godpr.get_order_details_pr(cat_val,yr_val,cc_val,sof_val)
        context = {
        'ccform':ccform,
        'catform':catform,
        'sofform':sofform,
        'yrform':yrform,
        'lst_god':lst_god,
        'with_content':True

        }


    else:
        ccform = CCForm(request.POST)
        catform = CATForm(request.POST)
        sofform = SOFForm(request.POST)
        yrform = YRForm(request.POST)
        context = {
        'ccform':ccform,
        'catform':catform,
        'sofform':sofform,
        'yrform':yrform,
        'with_content':False

        }

    return render(request, 'PPMP/purchase_request.html', context)




def purchase_request_save(request,parameter):



    sdf = request.POST.get('specification_details_form')
    pf = request.POST.get('purpose_form')
    spr.purchase_request(sdf,pf,GlobalVariables.item_orderdetails_id)
    context = {



    }
    return render(request, 'PPMP/index.html', context)



def purchase_request(request,parameter):

    GlobalVariables.with_req = cto.check_temp_order()
    lst_details = god2.get_details(int(GlobalVariables.item_orderdetails_id))
    dynamic_form = DynamicForm()
    purpose_form = PurposeForm()
    specification_details_form = SpecificationDetailsForm()
    items_name = [item if item != 'None' else '' for item in lst_details[:6]]
    items_name = ' '.join(items_name)
    re.sub(' +', ' ', items_name)
    amount = float(lst_details[6]) * (
                int(lst_details[8]) + int(lst_details[9] + int(lst_details[10]) + int(lst_details[11])))
    cat_code = GlobalVariables.cat_code
    generics = gil.get_gen(cat_code)
    specifics = gil.get_spec(cat_code)

    context = {

        'with_requests': GlobalVariables.with_req,
        'amount': amount,
        'generics': generics,
        'specifics': specifics,
        'items_name': items_name,
        'price': lst_details[6],
        'unit': lst_details[7],
        'purpose_form': purpose_form,
        'specification_details_form':specification_details_form,

        'modal_type': 'Six',
        'dynamic_form': dynamic_form

    }
    return render(request, 'PPMP/index.html', context)

def print_rfq(request,parameter):
    group_val = request.POST.get('group')
    group_val = group_val.split(' ')[1]
    lst_group_details = sg.get_group_details_combined(str(group_val))
    print(lst_group_details)
    pp.print_rfq(lst_group_details)

    try:
        return FileResponse(open('print_rfq.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def print_ppmp(request,parameter):

    fs_name = GlobalVariables.fs_name
    yr = GlobalVariables.yr
    type = GlobalVariables.type
    remarks = GlobalVariables.remarks
    cat_name = GlobalVariables.cat_name
    cat_code = GlobalVariables.cat_code
    lst_god = GlobalVariables.lst_god
    cc_code = GlobalVariables.cc_code
    cc_name = GlobalVariables.cc_name
    ppmp = GlobalVariables.ppmp
    dct_signatories = gsp.get_signatories_ppmp(cc_name)
    pp.print_ppmp(fs_name,yr,type,remarks,cat_name,cat_code,lst_god,cc_code,cc_name,ppmp,dct_signatories, request.user.first_name, request.user.last_name,)

    try:
        return FileResponse(open('print_ppmp.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def print_app(request,parameter):


    print(GlobalVariables.lst_app)
    dct_signatories = gsp.get_signatories_ap()
    # ap.print_app(GlobalVariables.lst_app,GlobalVariables.cat_val,GlobalVariables.yr_val,GlobalVariables.type_val,GlobalVariables.sof_val, GlobalVariables.qrtr_val,GlobalVariables.app_id)
    ap.print_app(GlobalVariables.lst_app,GlobalVariables.cat_val,GlobalVariables.yr_val,
                 GlobalVariables.type_val,GlobalVariables.sof_val, GlobalVariables.qrtr_val,
                 GlobalVariables.app_id,dct_signatories)

    try:
        return FileResponse(open('print_app.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()



def add_items_modal_four(request,parameter):

    GlobalVariables.prev_mdal = 8
    q1 = request.POST.get('quarter1')
    q2 = request.POST.get('quarter2')
    q3 = request.POST.get('quarter3')
    q4 = request.POST.get('quarter4')

    if q1 == '':
        q1 = '0'
    if q2 == '':
        q2 = '0'
    if q3 == '':
        q3 = '0'
    if q4 == '':
        q4 = '0'
    print("order_details", GlobalVariables.item_orderdetails_id, "ppmp", GlobalVariables.ppmp, "price_id",
          GlobalVariables.price_id)
    iod.insert_order_details(GlobalVariables.item_id, GlobalVariables.ppmp, GlobalVariables.price_id, q1, q2, q3,q4)

    categoryform = CategoryForm(request.POST)
    searchform = SearchForm(request.POST)
    catform = CATForm( initial={'cat': GlobalVariables.cat_name})
    print("Global Variables: ",GlobalVariables.ppmp )
    ci.insert_order_details(GlobalVariables.ppmp,GlobalVariables.item_id,)
    GlobalVariables.lst_god = god.get_order_details(GlobalVariables.cat_code, GlobalVariables.ppmp_create_id)
    context = {
        'catform':catform,
        'with_requests': GlobalVariables.with_req,
        'lst_god': GlobalVariables.lst_god,
        'cat_code': GlobalVariables.cat_code,
        'cat_name': GlobalVariables.cat_name,
        'with_categories': True,
        'modal_type': 'Three',
        'with_content': False,
        'show':True,
        'cc_code': GlobalVariables.cc_code,
        'cc_name': GlobalVariables.cc_name,
        'fs_name': GlobalVariables.fs_name,
        'yr': GlobalVariables.yr,
        'type': GlobalVariables.type,
        'remarks': GlobalVariables.remarks,
        'categoryform': categoryform,
        'searchform': searchform,
        "categories": GlobalVariables.categories,
        'lst_cc': GlobalVariables.lst_cc,

    }
    return render(request, 'PPMP/index.html', context)


# def print_ppmp(request,parameter):
#
#     #
#     # GlobalVariables.fs_name
#     # GlobalVariables.yr
#     # GlobalVariables.type
#     # GlobalVariables.remarks
#     # GlobalVariables.cat_name
#     # GlobalVariables.cat_code
#     # GlobalVariables.lst_god
#     # GlobalVariables.cc_code
#     # GlobalVariables.cc_name
#     fs_name = GlobalVariables.fs_name
#     yr = GlobalVariables.yr
#     type = GlobalVariables.type
#     remarks = GlobalVariables.remarks
#     cat_name = GlobalVariables.cat_name
#     cat_code = GlobalVariables.cat_code
#     lst_god = GlobalVariables.lst_god
#     cc_code = GlobalVariables.cc_code
#     cc_name = GlobalVariables.cc_name
#     ppmp = GlobalVariables.ppmp
#
#     pp.print_ppmp(fs_name,yr,type,remarks,cat_name,cat_code,lst_god,cc_code,cc_name,ppmp)
#
#     context = {
#
#
#
#     }
#     return render(request, 'PPMP/print_ppmp.html', context)

def extend_modal_four(request, parameter):
    GlobalVariables.with_req = cto.check_temp_order()
    dropdownform = YearForm(request.POST)
    GlobalVariables.prev_mdal = 7
    searchitemform = SearchItemForm(request.POST)
    specifics1 = Specifics1(request.POST)
    specifics2 = Specifics2(request.POST)
    specifics3 = Specifics3(request.POST)
    specifics4 = Specifics4(request.POST)
    specifics5 = Specifics5(request.POST)
    quarter1 = Quarter1(request.POST)
    quarter2 = Quarter2(request.POST)
    quarter3 = Quarter3(request.POST)
    quarter4 = Quarter4(request.POST)
    price_suggested = PriceSuggestedForm(request.POST)
    unit_suggested = UnitSuggestedForm(request.POST)
    cat_code = GlobalVariables.cat_code
    generics = gil.get_gen(cat_code)
    specifics = gil.get_spec(cat_code)

    if searchitemform.is_valid():
        gen = searchitemform.cleaned_data['name'].strip()
        try:
            s1 = request.POST.get('specifics1').strip()
        except:
            s1 = 'None'
        try:
            s2 = request.POST.get('specifics2').strip()
        except:
            s2 = 'None'
        try:
            s3 = request.POST.get('specifics3').strip()
        except:
            s3 = 'None'
        try:
            s4 = request.POST.get('specifics4').strip()
        except:
            s4 = 'None'
        try:
            s5 = request.POST.get('specifics5').strip()
        except:
            s5 = 'None'

        if s1 == '':
            s1 = 'None'
        if s2 == '':
            s2 = 'None'
        if s3 == '':
            s3 = 'None'
        if s4 == '':
            s4 = 'None'
        if s5 == '':
            s5 = 'None'
        print("GEneric:",gen)
        lst = [gen,s1, s2, s3, s4, s5]
        # GlobalVariables.gen_to_add = gen
        # GlobalVariables.specs_to_add = [s1, s2, s3, s4, s5]
        GlobalVariables.lst_to_add = lst
        item_name = " ".join(lst)
        item_name = item_name.replace('None', '')

        context = {
            'extend':True,
            'with_requests': GlobalVariables.with_req,
            'with_gen': True,
            'item_name': GlobalVariables.item_name,
            'found': False,
            'specifics1': specifics1,
            'specifics2': specifics2,
            'specifics3': specifics3,
            'specifics4': specifics4,
            'specifics5': specifics5,
            'generics': generics,
            'specifics': specifics,
            'searchitemform': searchitemform,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'Four',
            'dropdownform': dropdownform,
            'cat_code': cat_code,
            'with_requests': GlobalVariables.with_req,
            'quarter1': quarter1,
            'quarter2': quarter2,
            'quarter3': quarter3,
            'quarter4': quarter4,
            'price_suggested':price_suggested,
            'unit_suggested': unit_suggested
        }




    return render(request, 'PPMP/index.html', context)

def search_gen_specifics_modal_four(request,parameter):
    GlobalVariables.with_req = cto.check_temp_order()
    dropdownform = YearForm(request.POST)
    GlobalVariables.prev_mdal = 7
    searchitemform = SearchItemForm(request.POST)
    specifics1 = Specifics1(request.POST)
    specifics2 = Specifics2(request.POST)
    specifics3 = Specifics3(request.POST)
    specifics4 = Specifics4(request.POST)
    specifics5 = Specifics5(request.POST)
    quarter1 = Quarter1(request.POST)
    quarter2 = Quarter2(request.POST)
    quarter3 = Quarter3(request.POST)
    quarter4 = Quarter4(request.POST)
    cat_code = GlobalVariables.cat_code
    generics = gil.get_gen(cat_code)
    specifics = gil.get_spec(cat_code)

    if searchitemform.is_valid():
        gen = searchitemform.cleaned_data['name'].strip()
        try:
            s1 = request.POST.get('specifics1').strip()
        except:
            s1 = 'None'
        try:
            s2 = request.POST.get('specifics2').strip()
        except:
            s2 = 'None'
        try:
            s3 = request.POST.get('specifics3').strip()
        except:
            s3 = 'None'
        try:
            s4 = request.POST.get('specifics4').strip()
        except:
            s4 = 'None'
        try:
            s5 = request.POST.get('specifics5').strip()
        except:
            s5 = 'None'

        if s1 == '':
            s1 = 'None'
        if s2 == '':
            s2 = 'None'
        if s3 == '':
            s3 = 'None'
        if s4 == '':
            s4 = 'None'
        if s5 == '':
            s5 = 'None'
        print("GEneric:",gen)
        lst = [gen,s1, s2, s3, s4, s5]
        GlobalVariables.gen_to_add = gen
        GlobalVariables.specs_to_add = [s1, s2, s3, s4, s5]
        GlobalVariables.lst_to_add = lst
        item_name = " ".join(lst)
        item_name = item_name.replace('None', '')
        lst_top_three = cie.get_top_three(item_name)
        print(lst_top_three)
        GlobalVariables.item_name = item_name
        print('List',lst)
        print('Cat Code',cat_code)
        if cie.check(lst, cat_code):

            re.sub(' +', ' ', item_name)
            price, unit, GlobalVariables.price_id = cie.get_price_unit(lst, cat_code)
            GlobalVariables.item_id = cie.get_id(lst, cat_code)
            lst1 = [elem for elem in lst if elem != 'None']
            given_items = ' '.join(lst1).upper()
            context = {

                'extend':False,
                'with_requests': GlobalVariables.with_req,
                'quarter1': quarter1,
                'quarter2': quarter2,
                'quarter3': quarter3,
                'quarter4': quarter4,
                'initial': 0,
                'price': price,
                'unit': unit,
                'given_items': given_items,
                'found': True,
                'specifics1': specifics1,
                'specifics2': specifics2,
                'specifics3': specifics3,
                'specifics4': specifics4,
                'specifics5': specifics5,
                'generics': generics,
                'specifics': specifics,
                'searchitemform': searchitemform,
                'lst_cc': GlobalVariables.lst_cc,
                'modal_type': 'Four',
                'dropdownform': dropdownform,
                'cat_code': cat_code,
                'item_name': item_name,
                'with_gen': False

            }

        else:
            print('Not Found!')
            context = {
                'sug1': lst_top_three[0],
                'sug2': lst_top_three[1],
                'sug3': lst_top_three[2],
                'extend':False,
                'with_requests': GlobalVariables.with_req,
                'with_gen': True,
                'item_name': item_name,
                'found': False,
                'specifics1': specifics1,
                'specifics2': specifics2,
                'specifics3': specifics3,
                'specifics4': specifics4,
                'specifics5': specifics5,
                'generics': generics,
                'specifics': specifics,
                'searchitemform': searchitemform,
                'lst_cc': GlobalVariables.lst_cc,
                'modal_type': 'Four',
                'dropdownform': dropdownform,
                'cat_code': cat_code,
                'with_requests': GlobalVariables.with_req
            }

    return render(request, 'PPMP/index.html', context)

def insert_order_temporary_details(request,parameter):
    # GlobalVariables.with_req = cto.check_temp_order()
    # dropdownform = YearForm(request.POST)
    # lst = GlobalVariables.lst_to_add
    # gen = GlobalVariables.gen_to_add
    # specs = GlobalVariables.specs_to_add
    # print("LIST TO ADD",lst[0],lst[1],lst[2],lst[3],lst[4],lst[5])
    # print("PPMP_ID",GlobalVariables.ppmp_create_id)
    client_suggested_price = request.POST.get('price_suggested').strip()
    client_suggested_unit  = request.POST.get('unit_suggested').strip()

    q1 = request.POST.get('quarter1')
    q2 = request.POST.get('quarter2')
    q3 = request.POST.get('quarter3')
    q4 = request.POST.get('quarter4')

    if q1 == '':
        q1 = '0'
    if q2 == '':
        q2 = '0'
    if q3 == '':
        q3 = '0'
    if q4 == '':
        q4 = '0'
    gen = request.POST.get('name')
    s1 = request.POST.get('specifics1')
    s2 = request.POST.get('specifics2')
    s3 = request.POST.get('specifics3')
    s4 = request.POST.get('specifics4')
    s5 = request.POST.get('specifics5')
    print("Aqq ",gen,s1,s2,s3,s4,s5)

    if s1 =='':
        s1 = 'None'
    if s2 =='':
        s2 = 'None'
    if s3 == '':
        s3 = 'None'
    if s4 == '':
        s4 = 'None'
    if s5 =='':
        s5 = 'None'
    itod.insert_temp_order_details(GlobalVariables.ppmp_create_id, s1,s2,s3,s4,s5, gen,client_suggested_price,client_suggested_unit,q1,q2,q3,q4)

    context = {
        'with_requests': GlobalVariables.with_req,
        # 'dropdownform': dropdownform,
    }

    return render(request, 'PPMP/index.html', context)




def edit_items_modal_three(request,parameter):
    GlobalVariables.with_req = cto.check_temp_order()
    # categories = gcat.get_categories()
    lst_details = god2.get_details(int(parameter))
    GlobalVariables.item_orderdetails_id = parameter
    GlobalVariables.prev_mdal = 3

    # items_name = lst_details[:6]
    items_name = [item if item != 'None' else '' for item in lst_details[:6]]
    items_name = ' '.join(items_name)
    re.sub(' +', ' ', items_name)
    amount = float(lst_details[6]) * (
                int(lst_details[8]) + int(lst_details[9] + int(lst_details[10]) + int(lst_details[11])))
    # print(float(lst_details[6]), int(lst_details[8]),amount)
    cat_code = GlobalVariables.cat_code
    generics = gil.get_gen(cat_code)
    specifics = gil.get_spec(cat_code)

    context = {
        'with_requests': GlobalVariables.with_req,
        'amount': amount,
        'generics': generics,
        'specifics': specifics,
        'items_name': items_name,
        'searchitemform': SearchItemForm(initial={'name': lst_details[0]}),
        'price': lst_details[6],
        'unit': lst_details[7],
        'initial1': int(lst_details[8]),
        'initial2': int(lst_details[9]),
        'initial3': int(lst_details[10]),
        'initial4': int(lst_details[11]),
        'quarter1': Quarter1(initial={'quarter1': lst_details[8]}),
        'quarter2': Quarter2(initial={'quarter2': lst_details[9]}),
        'quarter3': Quarter3(initial={'quarter3': lst_details[10]}),
        'quarter4': Quarter4(initial={'quarter4': lst_details[11]}),

        'specifics1': Specifics1(initial={'specifics1': lst_details[1]}),
        'specifics2': Specifics2(initial={'specifics2': lst_details[2]}),
        'specifics3': Specifics3(initial={'specifics3': lst_details[3]}),
        'specifics4': Specifics4(initial={'specifics4': lst_details[4]}),
        'specifics5': Specifics5(initial={'specifics5': lst_details[5]}),


        'modal_type': 'Five',
        'with_requests': GlobalVariables.with_req

    }
    return render(request, 'PPMP/index.html', context)


def change_category_create_ppmp(request,parameter):
    GlobalVariables.with_req = cto.check_temp_order()
    categoryform = CategoryForm(request.POST)
    catform = CATForm(request.POST)
    # print(GlobalVariables.lst_ppmp_id)
    categories = gcat.get_categories()
    GlobalVariables.fs_name = GlobalVariables.lst_ppmp_id[2]
    GlobalVariables.yr = GlobalVariables.lst_ppmp_id[3]
    GlobalVariables.type = GlobalVariables.lst_ppmp_id[4]
    GlobalVariables.remarks = GlobalVariables.lst_ppmp_id[4]



    GlobalVariables.prev_mdal = 3
    raw_data = request.POST.get('cat')

    GlobalVariables.cat_name = raw_data
    with_categories = True
    cat_code = gcc.get_cat_code(raw_data)

    GlobalVariables.cat_code = cat_code
    GlobalVariables.lst_god = god.get_order_details(GlobalVariables.cat_code, GlobalVariables.ppmp_create_id)
    all_items = gia.get_items(cat_code)[1]
    GlobalVariables.dct_items = gia.get_items(cat_code)[0]
    print("CAT_CODE:",cat_code)
    all_items_price = gia.get_item_details(str(cat_code))
    # print("bla32",all_items)
    context = {
        'all_items_price': all_items_price,
        'all_items':all_items,
        'with_requests': GlobalVariables.with_req,
        'show': True,
        'lst_god': GlobalVariables.lst_god,
        'cat_code': cat_code,
        'cat_name': raw_data,
        'with_categories': with_categories,
        'lst_cc': GlobalVariables.lst_cc,
        'modal_type': 'Three',
        'with_content': False,
        'cc_code': GlobalVariables.cc_code,
        'cc_name': GlobalVariables.cc_name,
        'fs_name': GlobalVariables.fs_name,
        'yr': GlobalVariables.yr,
        'type': GlobalVariables.type,
        'remarks': GlobalVariables.remarks,
        'categoryform': categoryform,
        'catform': catform,
        "categories": categories,
        'with_requests': GlobalVariables.with_req



    }

    return render(request, 'PPMP/index.html', context)


def suggest_item(request,parameter):
    GlobalVariables.with_req = cto.check_temp_order()
    dropdownform = YearForm(request.POST)
    categories = gcat.get_categories()
    GlobalVariables.prev_mdal = 7
    searchitemform = SearchItemForm(request.POST)
    specifics1 = Specifics1(request.POST)
    specifics2 = Specifics2(request.POST)
    specifics3 = Specifics3(request.POST)
    specifics4 = Specifics4(request.POST)
    specifics5 = Specifics5(request.POST)
    quarter1 = Quarter1(request.POST)
    quarter2 = Quarter2(request.POST)
    quarter3 = Quarter3(request.POST)
    quarter4 = Quarter4(request.POST)
    cat_code = GlobalVariables.cat_code
    generics = gil.get_gen(cat_code)
    specifics = gil.get_spec(cat_code)
    lst_items = cie.get_item_from_database(str(parameter))
    # 'quarter1': Quarter1(initial={'quarter1': lst_details[8]}),

    context = {
        'with_requests': GlobalVariables.with_req,
        'with_gen': False,
        'found': False,
        'specifics1': Specifics1(initial={'specifics1': lst_items[1]}),
        'specifics2': Specifics2(initial={'specifics2': lst_items[2]}),
        'specifics3': Specifics3(initial={'specifics3': lst_items[3]}),
        'specifics4': Specifics4(initial={'specifics4': lst_items[4]}),
        'specifics5': Specifics5(initial={'specifics5': lst_items[5]}),

        'generics': generics,
        'specifics': specifics,
        'searchitemform': SearchItemForm(initial={'name': lst_items[0]}),
        'lst_cc': GlobalVariables.lst_cc,
        'modal_type': 'Four',
        'dropdownform': dropdownform,
        'cat_code': cat_code,
        'with_requests': GlobalVariables.with_req
    }
    return render(request, 'PPMP/index.html', context)





def add_create_ppmp_category(request,parameter):



    GlobalVariables.with_req = cto.check_temp_order()
    dropdownform = YearForm(request.POST)
    categories = gcat.get_categories()
    GlobalVariables.prev_mdal = 7
    searchitemform = SearchItemForm(request.POST)
    specifics1 = Specifics1(request.POST)
    specifics2 = Specifics2(request.POST)
    specifics3 = Specifics3(request.POST)
    specifics4 = Specifics4(request.POST)
    specifics5 = Specifics5(request.POST)
    quarter1 = Quarter1(request.POST)
    quarter2 = Quarter2(request.POST)
    quarter3 = Quarter3(request.POST)
    quarter4 = Quarter4(request.POST)
    cat_code = GlobalVariables.cat_code
    generics = gil.get_gen(cat_code)
    specifics = gil.get_spec(cat_code)

    if searchitemform.is_valid():
        gen = searchitemform.cleaned_data['name'].strip()
        try:
            s1 = request.POST.get('specifics1').strip()
        except:
            s1 = 'None'
        try:
            s2 = request.POST.get('specifics2').strip()
        except:
            s2 = 'None'
        try:
            s3 = request.POST.get('specifics3').strip()
        except:
            s3 = 'None'
        try:
            s4 = request.POST.get('specifics4').strip()
        except:
            s4 = 'None'
        try:
            s5 = request.POST.get('specifics5').strip()
        except:
            s5 = 'None'

        if s1 == '':
            s1 = 'None'
        if s2 == '':
            s2 = 'None'
        if s3 == '':
            s3 = 'None'
        if s4 == '':
            s4 = 'None'
        if s5 == '':
            s5 = 'None'

        lst = [gen, s1, s2, s3, s4, s5]

        context = {
            'with_requests': GlobalVariables.with_req,
            'with_gen': False,
            'found': False,
            'specifics1': specifics1,
            'specifics2': specifics2,
            'specifics3': specifics3,
            'specifics4': specifics4,
            'specifics5': specifics5,
            'generics': generics,
            'specifics': specifics,
            'searchitemform': searchitemform,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'Four',
            'dropdownform': dropdownform,
            'cat_code': cat_code,
            'with_requests': GlobalVariables.with_req
        }
    return render(request, 'PPMP/index.html', context)

def change_category_modal_three(request,parameter):
    # print("dri")
    GlobalVariables.with_req = cto.check_temp_order()
    categories = gcat.get_categories()
    GlobalVariables.prev_mdal = 4
    cat_val = request.POST.get('category_val')
    categoryform = CategoryForm(request.POST)
    catform = CATForm(request.POST)
    # print(cat_val)
    if cat_val == 'all':
        GlobalVariables.lst_god = god.get_order_details_all(GlobalVariables.ppmp_create_id)

        dftp.convert_pdf(1, "year", "code", "cost_center", "source_fund", "type_", "acc_code", "acc_name")


        categoryform = CategoryForm(request.POST)
        searchform = SearchForm(request.POST)
        with_categories = True
        context = {
            'with_requests': GlobalVariables.with_req,
            'show': False,
            'lst_god': GlobalVariables.lst_god,
            'with_categories': with_categories,
            'categoryform': categoryform,
            'lst_god': GlobalVariables.lst_god,
            'lst_cc': GlobalVariables.lst_cc,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'Three',
            'cc_code': GlobalVariables.cc_code,
            'cc_name': GlobalVariables.cc_name,
            'fs_name': GlobalVariables.fs_name,
            'yr': GlobalVariables.yr,
            'type': GlobalVariables.type,
            'remarks': GlobalVariables.remarks,
            'categoryform': categoryform,
            'catform': catform,
            "categories": categories,
            'with_requests': GlobalVariables.with_req

        }
    else:

        with_categories = False

        context = {
            'with_requests': GlobalVariables.with_req,
            'show': True,
            'lst_god': GlobalVariables.lst_god,
            'with_categories': with_categories,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'Three',
            'with_content': False,
            'cc_code': GlobalVariables.cc_code,
            'cc_name': GlobalVariables.cc_name,
            'fs_name': GlobalVariables.fs_name,
            'yr': GlobalVariables.yr,
            'type': GlobalVariables.type,
            'remarks': GlobalVariables.remarks,
            'categoryform': categoryform,
            'catform': catform,
            "categories": categories,
            'with_requests': GlobalVariables.with_req

        }
    return render(request, 'PPMP/index.html', context)
#
def create_ppmp(request,parameter):
    GlobalVariables.with_req = cto.check_temp_order()

    if parameter == '9999999':
        pass
    else:
        GlobalVariables.ppmp_create_id = GlobalVariables.lst_ppmp_id[0]
        GlobalVariables.fs_name = GlobalVariables.lst_ppmp_id[2]
        GlobalVariables.yr = GlobalVariables.lst_ppmp_id[3]
        GlobalVariables.type = GlobalVariables.lst_ppmp_id[4]
        GlobalVariables.remarks = GlobalVariables.lst_ppmp_id[4]

    categories = gcat.get_categories()
    categoryform = CategoryForm(request.POST)
    catform = CATForm(request.POST)
    # print(GlobalVariables.lst_ppmp_id)

    GlobalVariables.prev_mdal = 3
    with_categories = False

    context = {
        'with_requests': GlobalVariables.with_req,
        'show': True,
        'lst_god': GlobalVariables.lst_god,
        'with_categories': with_categories,
        'lst_cc': GlobalVariables.lst_cc,
        'modal_type': 'Three',
        'with_content': False,
        'cc_code': GlobalVariables.cc_code,
        'cc_name': GlobalVariables.cc_name,
        'fs_name': GlobalVariables.fs_name,
        'yr': GlobalVariables.yr,
        'type': GlobalVariables.type,
        'remarks': GlobalVariables.remarks,
        'categoryform': categoryform,
        'catform': catform,
        "categories": categories,
        'with_requests': GlobalVariables.with_req

    }
    return render(request, 'PPMP/index.html', context)

def cost_center_modal_one(request,parameter):
    print("PARAMETER ",parameter)
    if parameter != '99999999':

        parameter = parameter.replace('[', '')
        parameter = parameter.replace(']', '')
        parameter = parameter.split(',')
        parameter = [word.strip()[1:-1] for word in parameter]
        GlobalVariables.ppmp_id = parameter

    print("COST CENTER MODAL ONE ",GlobalVariables.ppmp_id)
    dropdownform = YearForm(request.POST)
    with_content = True
    show_buttons = False

    # print(GlobalVariables.ppmp)
    lst_ppmp = gp.get_ppmp( GlobalVariables.ppmp_id [0])
    GlobalVariables.lst_ppmp = lst_ppmp
    # print(lst_ppmp)
    GlobalVariables.cc_code =  GlobalVariables.ppmp_id[0]
    GlobalVariables.cc_name =  GlobalVariables.ppmp_id[1]
    GlobalVariables.fs_name = lst_ppmp[0][2]
    GlobalVariables.yr = lst_ppmp[0][3]
    GlobalVariables.type = lst_ppmp[0][4]
    GlobalVariables.remarks = lst_ppmp[0][4]
    context = {
        'with_requests': GlobalVariables.with_req,
        'lst_cc': GlobalVariables.lst_cc,
        'modal_type': 'One',
        'with_content': with_content,
        'course_code':  GlobalVariables.ppmp_id [0],
        'course_name':  GlobalVariables.ppmp_id [1],
        'lst_ppmp': lst_ppmp,
        'dropdownform': dropdownform,
        'show_buttons': show_buttons,
        'with_requests': GlobalVariables.with_req
    }

    return render(request, 'PPMP/index.html', context)


def update_year_modal_one(request,parameter):
    GlobalVariables.with_req = cto.check_temp_order()
    dropdownform = YearForm(request.POST)
    with_content = True

    parameter = GlobalVariables.ppmp_id
    GlobalVariables.yr = request.POST.get('year')
    lst_ppmp = gp.get_ppmp(parameter[0], request.POST.get('year'))
    GlobalVariables.lst_ppmp = lst_ppmp
    GlobalVariables.cc_code = parameter[0]
    GlobalVariables.cc_name = parameter[1]
    GlobalVariables.prev_mdal = 1
    # print(parameter)
    context = {
        'with_requests': GlobalVariables.with_req,
        'lst_cc': GlobalVariables.lst_cc,
        'modal_type': 'One',
        'with_content': with_content,
        'course_code': parameter[0],
        'course_name': parameter[1],
        'lst_ppmp': lst_ppmp,
        'dropdownform': dropdownform,
        'with_requests': GlobalVariables.with_req
    }
    return render(request, 'PPMP/index.html', context)


def clicked_modal_one(request,parameter):
    GlobalVariables.with_req = cto.check_temp_order()



    GlobalVariables.ppmp = parameter
    # print("PPMP ID:",GlobalVariables.ppmp)
    dropdownform = YearForm(request.POST)
    with_content = True
    show_buttons = True

    lst_ppmp_id = []

    for i in GlobalVariables.lst_ppmp:
        if i[0] == int(GlobalVariables.ppmp):
            lst_ppmp_id = i
            break

    GlobalVariables.lst_ppmp_id = lst_ppmp_id
    print(GlobalVariables.lst_ppmp_id)
    context = {
        'with_requests': GlobalVariables.with_req,
        'lst_cc': GlobalVariables.lst_cc,
        'modal_type': 'One',
        'with_content': with_content,
        'lst_ppmp': GlobalVariables.lst_ppmp,
        'lst_ppmp_id': lst_ppmp_id,
        'dropdownform': dropdownform,
        'show_buttons': show_buttons,
        'course_code': GlobalVariables.cc_code,
        'course_name': GlobalVariables.cc_name,
        'with_requests': GlobalVariables.with_req
    }
    return render(request, 'PPMP/index.html', context)

def ppmp(request, parameter):
    GlobalVariables.with_req = cto.check_temp_order()
    print('parameter :', parameter)


    print(GlobalVariables.ppmp, 'start')
    categories = gcat.get_categories()
    GlobalVariables.categories = categories
    dropdownform = YearForm(request.POST)
    user = request.user
    GlobalVariables.lst_cc = gc.get_cost_centers(user)


    if parameter == '999990':
        print('sulod')
        with_content = False
        GlobalVariables.prev_mdal = 1
        context = {
            'with_requests': GlobalVariables.with_req,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'One',
            'with_content': with_content
        }


    # elif parameter == '999991':  ### Update Year
    #     with_content = True
    #
    #     parameter = GlobalVariables.ppmp_id
    #     GlobalVariables.yr = request.POST.get('year')
    #     lst_ppmp = gp.get_ppmp(parameter[0], request.POST.get('year'))
    #     GlobalVariables.lst_ppmp = lst_ppmp
    #     GlobalVariables.cc_code = parameter[0]
    #     GlobalVariables.cc_name = parameter[1]
    #     GlobalVariables.prev_mdal = 1
    #     # print(parameter)
    #     context = {
    #         'with_requests': GlobalVariables.with_req,
    #         'lst_cc': GlobalVariables.lst_cc,
    #         'modal_type': 'One',
    #         'with_content': with_content,
    #         'course_code': parameter[0],
    #         'course_name': parameter[1],
    #         'lst_ppmp': lst_ppmp,
    #         'dropdownform': dropdownform
    #     }
    elif parameter == '9999931': ### Change Category in Create PPMP
        categoryform = CategoryForm(request.POST)
        catform = CATForm(request.POST)
        print(GlobalVariables.lst_ppmp_id)
        # GlobalVariables.ppmp_id = GlobalVariables.lst_ppmp_id[0]
        GlobalVariables.fs_name = GlobalVariables.lst_ppmp_id[2]
        GlobalVariables.yr = GlobalVariables.lst_ppmp_id[3]
        GlobalVariables.type = GlobalVariables.lst_ppmp_id[4]
        GlobalVariables.remarks = GlobalVariables.lst_ppmp_id[4]
        GlobalVariables.prev_mdal = 3
        raw_data = request.POST.get('cat')
        print("raw Data", raw_data)
        GlobalVariables.cat_name = raw_data
        with_categories = True
        cat_code = gcc.get_cat_code(raw_data)
        # print("cat_code", cat_code)
        GlobalVariables.cat_code = cat_code
        GlobalVariables.lst_god = god.get_order_details(GlobalVariables.cat_code, GlobalVariables.ppmp_create_id)
        print(raw_data)
        context = {
            'with_requests': GlobalVariables.with_req,
            'show': True,
            'lst_god': GlobalVariables.lst_god,
            'cat_code': cat_code,
            'cat_name': raw_data,
            'with_categories': with_categories,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'Three',
            'with_content': False,
            'cc_code': GlobalVariables.cc_code,
            'cc_name': GlobalVariables.cc_name,
            'fs_name': GlobalVariables.fs_name,
            'yr': GlobalVariables.yr,
            'type': GlobalVariables.type,
            'remarks': GlobalVariables.remarks,
            'categoryform': categoryform,
            'catform': catform,
            "categories": categories,

        }
    elif parameter == '999993':  ### Create PPMP
        categoryform = CategoryForm(request.POST)
        catform = CATForm(request.POST)
        # print(GlobalVariables.lst_ppmp_id)
        # GlobalVariables.ppmp_id = GlobalVariables.lst_ppmp_id[0]
        GlobalVariables.fs_name = GlobalVariables.lst_ppmp_id[2]
        GlobalVariables.yr = GlobalVariables.lst_ppmp_id[3]
        GlobalVariables.type = GlobalVariables.lst_ppmp_id[4]
        GlobalVariables.remarks = GlobalVariables.lst_ppmp_id[4]
        GlobalVariables.prev_mdal = 3
        with_categories = False

        context = {
            'with_requests': GlobalVariables.with_req,
            'show':True,
            'lst_god': GlobalVariables.lst_god,
            'with_categories': with_categories,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'Three',
            'with_content': False,
            'cc_code': GlobalVariables.cc_code,
            'cc_name': GlobalVariables.cc_name,
            'fs_name': GlobalVariables.fs_name,
            'yr': GlobalVariables.yr,
            'type': GlobalVariables.type,
            'remarks': GlobalVariables.remarks,
            'categoryform': categoryform,
            'catform': catform,
            "categories": categories,

        }
    # elif parameter == '999994':  ### Change Category
    #     GlobalVariables.prev_mdal = 4
    #     # categoryform = CategoryForm(request.POST)
    #     cat_val= request.POST.get('category_val')
    #     categoryform = CategoryForm(request.POST)
    #     catform = CATForm(request.POST)
    #     print(cat_val)
    #     if cat_val == 'all':
    #         GlobalVariables.lst_god = god.get_order_details_all( GlobalVariables.ppmp_id)
    #         categoryform = CategoryForm(request.POST)
    #         searchform = SearchForm(request.POST)
    #         with_categories = True
    #         context = {
    #             'with_requests': GlobalVariables.with_req,
    #             'show': False,
    #             'lst_god': GlobalVariables.lst_god,
    #             'with_categories': with_categories,
    #             'categoryform': categoryform,
    #             'lst_god': GlobalVariables.lst_god,
    #             'lst_cc': GlobalVariables.lst_cc,
    #             'modal_type': 'Three',
    #             'cc_code': GlobalVariables.cc_code,
    #             'cc_name': GlobalVariables.cc_name,
    #             'fs_name': GlobalVariables.fs_name,
    #             'yr': GlobalVariables.yr,
    #             'type': GlobalVariables.type,
    #             'remarks': GlobalVariables.remarks,
    #             'categoryform': categoryform,
    #             'catform': catform,
    #             "categories": categories,
    #
    #         }
    #     else:
    #
    #         with_categories = False
    #
    #         context = {
    #             'with_requests': GlobalVariables.with_req,
    #             'show':True,
    #             'lst_god': GlobalVariables.lst_god,
    #             'with_categories': with_categories,
    #             'lst_cc': GlobalVariables.lst_cc,
    #             'modal_type': 'Three',
    #             'with_content': False,
    #             'cc_code': GlobalVariables.cc_code,
    #             'cc_name': GlobalVariables.cc_name,
    #             'fs_name': GlobalVariables.fs_name,
    #             'yr': GlobalVariables.yr,
    #             'type': GlobalVariables.type,
    #             'remarks': GlobalVariables.remarks,
    #             'categoryform': categoryform,
    #             'catform': catform,
    #             "categories": categories,
    #
    #         }

    elif parameter == '999995':  #### Back
        with_content = True
        show_buttons = False
        parameter = GlobalVariables.ppmp_id
        lst_ppmp = GlobalVariables.lst_ppmp
        GlobalVariables.prev_mdal = 5
        context = {
            'with_requests': GlobalVariables.with_req,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'One',
            'with_content': with_content,
            'course_code': parameter[0],
            'course_name': parameter[1],
            'lst_ppmp': lst_ppmp,
            'dropdownform': dropdownform,
            'show_buttons': show_buttons
        }

    elif parameter == '999996':  #### Back
        with_content = True
        show_buttons = False
        parameter = GlobalVariables.ppmp_id
        lst_ppmp = GlobalVariables.lst_ppmp
        GlobalVariables.prev_mdal = 6
        context = {
            'with_requests': GlobalVariables.with_req,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'One',
            'with_content': with_content,
            'course_code': parameter[0],
            'course_name': parameter[1],
            'lst_ppmp': lst_ppmp,
            'dropdownform': dropdownform,
            'show_buttons': show_buttons
        }


    elif parameter == '999997':  #### Add ITEMS

        GlobalVariables.prev_mdal = 7
        searchitemform = SearchItemForm(request.POST)
        specifics1 = Specifics1(request.POST)
        specifics2 = Specifics2(request.POST)
        specifics3 = Specifics3(request.POST)
        specifics4 = Specifics4(request.POST)
        specifics5 = Specifics5(request.POST)
        quarter1 = Quarter1(request.POST)
        quarter2 = Quarter2(request.POST)
        quarter3 = Quarter3(request.POST)
        quarter4 = Quarter4(request.POST)
        cat_code = GlobalVariables.cat_code
        generics = gil.get_gen(cat_code)
        specifics = gil.get_spec(cat_code)

        if searchitemform.is_valid():
            gen = searchitemform.cleaned_data['name'].strip()
            try:
                s1 = request.POST.get('specifics1').strip()
            except:
                s1 = 'None'
            try:
                s2 = request.POST.get('specifics2').strip()
            except:
                s2 = 'None'
            try:
                s3 = request.POST.get('specifics3').strip()
            except:
                s3 = 'None'
            try:
                s4 = request.POST.get('specifics4').strip()
            except:
                s4 = 'None'
            try:
                s5 = request.POST.get('specifics5').strip()
            except:
                s5 = 'None'

            if s1 == '':
                s1 = 'None'
            if s2 == '':
                s2 = 'None'
            if s3 == '':
                s3 = 'None'
            if s4 == '':
                s4 = 'None'
            if s5 == '':
                s5 = 'None'

            lst = [gen, s1, s2, s3, s4, s5]

            context = {
                'with_requests': GlobalVariables.with_req,
                'with_gen':  False,
                'found': False,
                'specifics1': specifics1,
                'specifics2': specifics2,
                'specifics3': specifics3,
                'specifics4': specifics4,
                'specifics5': specifics5,
                'generics': generics,
                'specifics': specifics,
                'searchitemform': searchitemform,
                'lst_cc': GlobalVariables.lst_cc,
                'modal_type': 'Four',
                'dropdownform': dropdownform,
                'cat_code': cat_code,
            }
    #
    #
    # elif parameter == '9999971':  #### Search General Name and Item Descriptions on Add Items
    #     GlobalVariables.prev_mdal = 7
    #     searchitemform = SearchItemForm(request.POST)
    #     specifics1 = Specifics1(request.POST)
    #     specifics2 = Specifics2(request.POST)
    #     specifics3 = Specifics3(request.POST)
    #     specifics4 = Specifics4(request.POST)
    #     specifics5 = Specifics5(request.POST)
    #     quarter1 = Quarter1(request.POST)
    #     quarter2 = Quarter2(request.POST)
    #     quarter3 = Quarter3(request.POST)
    #     quarter4 = Quarter4(request.POST)
    #     cat_code = GlobalVariables.cat_code
    #     generics = gil.get_gen(cat_code)
    #     specifics = gil.get_spec(cat_code)
    #
    #     if searchitemform.is_valid():
    #         gen = searchitemform.cleaned_data['name'].strip()
    #         try:
    #             s1 = request.POST.get('specifics1').strip()
    #         except:
    #             s1 = 'None'
    #         try:
    #             s2 = request.POST.get('specifics2').strip()
    #         except:
    #             s2 = 'None'
    #         try:
    #             s3 = request.POST.get('specifics3').strip()
    #         except:
    #             s3 = 'None'
    #         try:
    #             s4 = request.POST.get('specifics4').strip()
    #         except:
    #             s4 = 'None'
    #         try:
    #             s5 = request.POST.get('specifics5').strip()
    #         except:
    #             s5 = 'None'
    #
    #         if s1 == '':
    #             s1 = 'None'
    #         if s2 == '':
    #             s2 = 'None'
    #         if s3 == '':
    #             s3 = 'None'
    #         if s4 == '':
    #             s4 = 'None'
    #         if s5 == '':
    #             s5 = 'None'
    #
    #         lst = [gen, s1, s2, s3, s4, s5]
    #         GlobalVariables.lst_to_add = lst
    #         item_name = " ".join(lst)
    #         item_name = item_name.replace('None', '')
    #         if cie.check(lst, cat_code):
    #
    #
    #             re.sub(' +', ' ', item_name)
    #             price, unit, GlobalVariables.price_id = cie.get_price_unit(lst, cat_code)
    #             GlobalVariables.item_id = cie.get_id(lst, cat_code)
    #             lst1 = [elem for elem in lst if elem != 'None']
    #             given_items = ' '.join(lst1).upper()
    #             context = {
    #                 'with_requests': GlobalVariables.with_req,
    #                 'quarter1': quarter1,
    #                 'quarter2': quarter2,
    #                 'quarter3': quarter3,
    #                 'quarter4': quarter4,
    #                 'initial': 0,
    #                 'price': price,
    #                 'unit': unit,
    #                 'given_items': given_items,
    #                 'found': True,
    #                 'specifics1': specifics1,
    #                 'specifics2': specifics2,
    #                 'specifics3': specifics3,
    #                 'specifics4': specifics4,
    #                 'specifics5': specifics5,
    #                 'generics': generics,
    #                 'specifics': specifics,
    #                 'searchitemform': searchitemform,
    #                 'lst_cc': GlobalVariables.lst_cc,
    #                 'modal_type': 'Four',
    #                 'dropdownform': dropdownform,
    #                 'cat_code': cat_code,
    #                 'item_name': item_name,
    #                 'with_gen': False
    #
    #             }
    #
    #         else:
    #             context = {
    #                 'with_requests': GlobalVariables.with_req,
    #                 'with_gen':True,
    #                 'item_name': item_name,
    #                 'found': False,
    #                 'specifics1': specifics1,
    #                 'specifics2': specifics2,
    #                 'specifics3': specifics3,
    #                 'specifics4': specifics4,
    #                 'specifics5': specifics5,
    #                 'generics': generics,
    #                 'specifics': specifics,
    #                 'searchitemform': searchitemform,
    #                 'lst_cc': GlobalVariables.lst_cc,
    #                 'modal_type': 'Four',
    #                 'dropdownform': dropdownform,
    #                 'cat_code': cat_code,
    #             }

    elif parameter == '9999972': ### Insert Temporary Order Details

        print(GlobalVariables.ppmp_id)

        print(GlobalVariables.lst_to_add)
        lst = GlobalVariables.lst_to_add
        itod.insert_temp_order_details(GlobalVariables.ppmp_id,lst[1],lst[2],lst[3],lst[4],lst[5],lst[0])


        context = {
            'with_requests': GlobalVariables.with_req,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'One',
            'with_content': with_content,
            'course_code': parameter[0],
            'course_name': parameter[1],
            'lst_ppmp': lst_ppmp,
            'dropdownform': dropdownform,
            'show_buttons': show_buttons
        }

    # elif parameter == '999998':  #### Add ITEMS
    #     GlobalVariables.prev_mdal = 8
    #     q1 = request.POST.get('quarter1')
    #     q2 = request.POST.get('quarter2')
    #     q3 = request.POST.get('quarter3')
    #     q4 = request.POST.get('quarter4')
    #
    #     if q1 == '':
    #         q1 = '0'
    #     if q2 == '':
    #         q2 = '0'
    #     if q3 == '':
    #         q3 = '0'
    #     if q4 == '':
    #         q4 = '0'
    #     print("order_details",GlobalVariables.item_orderdetails_id,"ppmp", GlobalVariables.ppmp, "price_id",GlobalVariables.price_id)
    #     iod.insert_order_details(GlobalVariables.item_id, GlobalVariables.ppmp, GlobalVariables.price_id, q1, q2, q3,
    #                              q4)
    #
    #     categoryform = CategoryForm(request.POST)
    #     searchform = SearchForm(request.POST)
    #     GlobalVariables.lst_god = god.get_order_details(GlobalVariables.cat_code, GlobalVariables.ppmp_id)
    #     context = {
    #         'with_requests': GlobalVariables.with_req,
    #         'lst_god': GlobalVariables.lst_god,
    #         'cat_code': GlobalVariables.cat_code,
    #         'cat_name': GlobalVariables.cat_name,
    #         'with_categories': True,
    #         'modal_type': 'Three',
    #         'with_content': False,
    #         'cc_code': GlobalVariables.cc_code,
    #         'cc_name': GlobalVariables.cc_name,
    #         'fs_name': GlobalVariables.fs_name,
    #         'yr': GlobalVariables.yr,
    #         'type': GlobalVariables.type,
    #         'remarks': GlobalVariables.remarks,
    #         'categoryform': categoryform,
    #         'searchform': searchform,
    #         "categories": GlobalVariables.categories,
    #         'lst_cc': GlobalVariables.lst_cc,
    #
    #     }
    #
    #

    elif parameter == '9999981':  #### Back From Add Items (Modal Five)


        categoryform = CategoryForm(request.POST)
        searchform = SearchForm(request.POST)
        GlobalVariables.lst_god = god.get_order_details(GlobalVariables.cat_code,GlobalVariables.ppmp_id)
        context = {
            'with_requests': GlobalVariables.with_req,
            'lst_god': GlobalVariables.lst_god,
            'cat_code': GlobalVariables.cat_code,
            'cat_name': GlobalVariables.cat_name,
            'with_categories': True,
            'modal_type': 'Three',
            'with_content': False,
            'cc_code': GlobalVariables.cc_code,
            'cc_name': GlobalVariables.cc_name,
            'fs_name': GlobalVariables.fs_name,
            'yr': GlobalVariables.yr,
            'type': GlobalVariables.type,
            'remarks': GlobalVariables.remarks,
            'categoryform': categoryform,
            'searchform': searchform,
            "categories": GlobalVariables.categories,
            'lst_cc': GlobalVariables.lst_cc,

        }


    elif parameter == '999999':  #### Save ITEMS


        q1 = request.POST.get('quarter1')
        q2 = request.POST.get('quarter2')
        q3 = request.POST.get('quarter3')
        q4 = request.POST.get('quarter4')



        if q1 == '':
            q1 = '0'
        if q2 == '':
            q2 = '0'
        if q3 == '':
            q3 = '0'
        if q4 == '':
            q4 = '0'
        print("Quarters:", q1,q2,q3,q4)
        print(GlobalVariables.item_orderdetails_id)


        categoryform = CategoryForm(request.POST)
        searchform = SearchForm(request.POST)
        ei.editItems(GlobalVariables.item_id, GlobalVariables.item_orderdetails_id, q1,q2,q3,q4)
        GlobalVariables.lst_god = god.get_order_details(GlobalVariables.cat_code,GlobalVariables.ppmp_id)

        context = {
            'with_requests': GlobalVariables.with_req,
            'lst_god': GlobalVariables.lst_god,
            'cat_code': GlobalVariables.cat_code,
            'cat_name': GlobalVariables.cat_name,
            'with_categories': True,
            'modal_type': 'Three',
            'with_content': False,
            'cc_code': GlobalVariables.cc_code,
            'cc_name': GlobalVariables.cc_name,
            'fs_name': GlobalVariables.fs_name,
            'yr': GlobalVariables.yr,
            'type': GlobalVariables.type,
            'remarks': GlobalVariables.remarks,
            'categoryform': categoryform,
            'searchform': searchform,
            "categories": GlobalVariables.categories,
            'lst_cc': GlobalVariables.lst_cc,

        }

    elif parameter == '9999971':  #### Change Item Description in Edit Items

        lst_details = god2.get_details(int(GlobalVariables.item_orderdetails_id))
        GlobalVariables.prev_mdal = 3
        amount = float(lst_details[6]) *( int(lst_details[8])+int(lst_details[9]+int(lst_details[10]) + int(lst_details[11])))

        searchitemform = SearchItemForm(request.POST)
        specifics1 = Specifics1(request.POST)
        specifics2 = Specifics2(request.POST)
        specifics3 = Specifics3(request.POST)
        specifics4 = Specifics4(request.POST)
        specifics5 = Specifics5(request.POST)

        cat_code = GlobalVariables.cat_code
        generics = gil.get_gen(cat_code)
        specifics = gil.get_spec(cat_code)

        if searchitemform.is_valid():
            gen = searchitemform.cleaned_data['name'].strip()
            try:
                s1 = request.POST.get('specifics1').strip()
            except:
                s1 = 'None'
            try:
                s2 = request.POST.get('specifics2').strip()
            except:
                s2 = 'None'
            try:
                s3 = request.POST.get('specifics3').strip()
            except:
                s3 = 'None'
            try:
                s4 = request.POST.get('specifics4').strip()
            except:
                s4 = 'None'
            try:
                s5 = request.POST.get('specifics5').strip()
            except:
                s5 = 'None'

            if s1 == '':
                s1 = 'None'
            if s2 == '':
                s2 = 'None'
            if s3 == '':
                s3 = 'None'
            if s4 == '':
                s4 = 'None'
            if s5 == '':
                s5 = 'None'

            lst = [gen, s1, s2, s3, s4, s5]
            print(lst)
            if cie.check(lst, cat_code):
                item_name = " ".join(lst)
                items_name = item_name.replace('None', '')
                re.sub(' +', ' ', item_name)
                price, unit, GlobalVariables.price_id = cie.get_price_unit(lst, cat_code)
                GlobalVariables.item_id = cie.get_id(lst, cat_code)
                print("ITEM ID", GlobalVariables.item_id)
                lst1 = [elem for elem in lst if elem != 'None']
                # given_items = ' '.join(lst1).upper()

            context = {
                'with_requests': GlobalVariables.with_req,
                'amount':amount,
                'generics':generics,
                'specifics':specifics,
                'items_name':items_name,
                'searchitemform': searchitemform    ,
                'price': lst_details[6],
                'unit':lst_details[7],
                'initial1': int(lst_details[8]),
                'initial2': int(lst_details[9]),
                'initial3': int(lst_details[10]),
                'initial4': int(lst_details[11]),
                'quarter1' : Quarter1(initial =  {'quarter1':lst_details[8]}),
                'quarter2' : Quarter2(initial =  {'quarter2':lst_details[9]}),
                'quarter3' : Quarter3(initial =  {'quarter3':lst_details[10]}),
                'quarter4' : Quarter4(initial =  {'quarter4':lst_details[11]}),


                'specifics1': specifics1,
                'specifics2': specifics2,
                'specifics3': specifics3,
                'specifics4': specifics4,
                'specifics5': specifics5,
                'modal_type': 'Five'
            }

    # elif parameter in lst_num and GlobalVariables.prev_mdal == 3: ### EDIT ITEMS (PRESSING THE + )
    #
    #     lst_details = god2.get_details(int(parameter))
    #     GlobalVariables.item_orderdetails_id = parameter
    #     GlobalVariables.prev_mdal = 3
    #
    #     # items_name = lst_details[:6]
    #     items_name = [item if item != 'None' else '' for item in lst_details[:6] ]
    #     items_name = ' '.join(items_name)
    #     re.sub(' +', ' ', items_name)
    #     amount = float(lst_details[6]) *( int(lst_details[8])+int(lst_details[9]+int(lst_details[10]) + int(lst_details[11])))
    #     # print(float(lst_details[6]), int(lst_details[8]),amount)
    #     cat_code = GlobalVariables.cat_code
    #     generics = gil.get_gen(cat_code)
    #     specifics = gil.get_spec(cat_code)
    #
    #     context = {
    #         'with_requests': GlobalVariables.with_req,
    #         'amount':amount,
    #         'generics':generics,
    #         'specifics':specifics,
    #         'items_name':items_name,
    #         'searchitemform': SearchItemForm (initial={'name': lst_details[0]}),
    #         'price': lst_details[6],
    #         'unit':lst_details[7],
    #         'initial1': int(lst_details[8]),
    #         'initial2': int(lst_details[9]),
    #         'initial3': int(lst_details[10]),
    #         'initial4': int(lst_details[11]),
    #         'quarter1' : Quarter1(initial =  {'quarter1':lst_details[8]}),
    #         'quarter2' : Quarter2(initial =  {'quarter2':lst_details[9]}),
    #         'quarter3' : Quarter3(initial =  {'quarter3':lst_details[10]}),
    #         'quarter4' : Quarter4(initial =  {'quarter4':lst_details[11]}),
    #
    #
    #         'specifics1': Specifics1(initial =  {'specifics1':lst_details[1]}),
    #         'specifics2': Specifics2(initial =  {'specifics2':lst_details[2]}),
    #         'specifics3': Specifics3(initial =  {'specifics3':lst_details[3]}),
    #         'specifics4': Specifics4(initial =  {'specifics4':lst_details[4]}),
    #         'specifics5': Specifics5(initial =  {'specifics5':lst_details[5]}),
    #
    #         'modal_type': 'Five'
    #
    #     }


    elif parameter == '9999911': ### Back From Modal Three

        with_content = True
        show_buttons = True

        lst_ppmp_id = []

        for i in GlobalVariables.lst_ppmp:
            if i[0] == int(GlobalVariables.ppmp):
                lst_ppmp_id = i
                break

        GlobalVariables.lst_ppmp_id = lst_ppmp_id

        context = {
            'with_requests': GlobalVariables.with_req,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'One',
            'with_content': with_content,
            'lst_ppmp': GlobalVariables.lst_ppmp,
            'lst_ppmp_id': lst_ppmp_id,
            'dropdownform': dropdownform,
            'show_buttons': show_buttons,
            'course_code': GlobalVariables.cc_code,
            'course_name': GlobalVariables.cc_name,
        }


    elif parameter in lst_num:  #### Select PPMP ID

        with_content = True
        show_buttons = True
        GlobalVariables.ppmp = parameter
        lst_ppmp_id = []

        for i in GlobalVariables.lst_ppmp:
            if i[0] == int(GlobalVariables.ppmp):
                lst_ppmp_id = i
                break

        GlobalVariables.lst_ppmp_id = lst_ppmp_id

        context = {
            'with_requests': GlobalVariables.with_req,
            'lst_cc': GlobalVariables.lst_cc,
            'modal_type': 'One',
            'with_content': with_content,
            'lst_ppmp': GlobalVariables.lst_ppmp,
            'lst_ppmp_id': lst_ppmp_id,
            'dropdownform': dropdownform,
            'show_buttons': show_buttons,
            'course_code': GlobalVariables.cc_code,
            'course_name': GlobalVariables.cc_name,
        }


    #
    # else:  #### Cost Center PPMP (MODAL ONE)
    #     with_content = True
    #     show_buttons = False
    #     parameter = parameter.replace('[', '')
    #     parameter = parameter.replace(']', '')
    #     parameter = parameter.split(',')
    #     parameter = [word.strip()[1:-1] for word in parameter]
    #     GlobalVariables.ppmp_id = parameter
    #     print(GlobalVariables.ppmp)
    #     lst_ppmp = gp.get_ppmp(parameter[0])
    #     GlobalVariables.lst_ppmp = lst_ppmp
    #     # print(lst_ppmp)
    #     GlobalVariables.cc_code = parameter[0]
    #     GlobalVariables.cc_name = parameter[1]
    #     GlobalVariables.fs_name = lst_ppmp[0][2]
    #     GlobalVariables.yr = lst_ppmp[0][3]
    #     GlobalVariables.type = lst_ppmp[0][4]
    #     GlobalVariables.remarks = lst_ppmp[0][4]
    #     context = {
    #         'with_requests': GlobalVariables.with_req,
    #         'lst_cc': GlobalVariables.lst_cc,
    #         'modal_type': 'One',
    #         'with_content': with_content,
    #         'course_code': parameter[0],
    #         'course_name': parameter[1],
    #         'lst_ppmp': lst_ppmp,
    #         'dropdownform': dropdownform,
    #         'show_buttons': show_buttons
    #     }

    return render(request, 'PPMP/index.html', context)

def reports(request, parameter):

    # searchitemsform = SearchItemsForm(request.POST)
    # searchcostcenterform = SearchCostCenterForm(request.POST)
    # searchquarterform = SearchQuarterForm(request.POST)
    #
    # # 'specifics1': Specifics1(initial={'specifics1': lst_details[1]}),
    # # 'specifics2': Specifics2(initial={'specifics2': lst_details[2]}),
    # # 'specifics3': Specifics3(initial={'specifics3': lst_details[3]}),
    # # 'specifics4': Specifics4(initial={'specifics4': lst_details[4]}),
    # # 'specifics5': Specifics5(initial={'specifics5': lst_details[5]}),
    print(parameter)

    if parameter == '999991':
        GlobalVariables.with_req = cto.check_temp_order()
        print('sulod')
        try:
            cc = request.POST.get('cost_center').strip()
        except:
            cc = 'Filter By Cost Center'
        try:
            cat = request.POST.get('category').strip()
        except:
            cat = 'Filter By Category'
        try:
            item = request.POST.get('items').strip()
        except:
            item = 'Filter By Items'
        try:
            yrq = request.POST.get('quarter').strip()
        except:
            yrq = 'Filter By Year/  Quarter'


        # print('cc: ',cc)
        # print('cat: ',cat)
        # print('item: ',item)
        # print('yrq: ',yrq)

        context = {
            'with_requests': GlobalVariables.with_req,
            'searchcategoryform': SearchCategoryForm(initial={'category': cat}),
            'searchitemsform' : SearchItemsForm(initial={'items': item}),
            'searchcostcenterform' : SearchCostCenterForm(initial={'cost_center': cc}),
            'searchquarterform' :  SearchQuarterForm(initial={'quarter': yrq}),
            'modal_type': 'One',
            'lst_report': cr.check([cc,cat,item,yrq]),
            'lst_cc': "++".join(cr.generate_lists()[0]),
            'lst_category': "++".join(cr.generate_lists()[1]),
            'lst_items' : "++".join(cr.generate_lists()[2]),
            'lst_yr_qrtr' : "++".join(cr.generate_lists()[3]),
        }
    else:
        GlobalVariables.with_req = cto.check_temp_order()
        context = {
            'with_requests': GlobalVariables.with_req,
            'searchcategoryform': SearchCategoryForm(initial={'category': 'Filter By Category'}),
            'searchitemsform' : SearchItemsForm(initial={'items': 'Filter By Items'}),
            'searchcostcenterform' : SearchCostCenterForm(initial={'cost_center': 'Filter By Cost Center'}),
            'searchquarterform' :  SearchQuarterForm(initial={'quarter': 'Filter By Year/  Quarter'}),
            'modal_type': 'One',
            'lst_report': cr.generate_report(),
            'lst_cc': "++".join(cr.generate_lists()[0]),
            'lst_category': "++".join(cr.generate_lists()[1]),
            'lst_items' : "++".join(cr.generate_lists()[2]),
            'lst_yr_qrtr' : "++".join(cr.generate_lists()[3]),
        }

    return render(request, 'PPMP/reports.html', context)


def app(request, parameter):
    GlobalVariables.with_req = cto.check_temp_order()

    if parameter == '999991':
        lst_results = ''
        with_value = True
        GlobalVariables.cat_val = request.POST.get('cat')
        GlobalVariables.yr_val = request.POST.get('yr')
        GlobalVariables.type_val = request.POST.get('type')
        GlobalVariables.sof_val = request.POST.get('sof')
        GlobalVariables.qrtr_val = request.POST.get('quarter')


        sofform = SOFForm(request.POST)
        catform = CATForm(request.POST)
        yrform = YRForm(request.POST)
        typeform = TypeForm(request.POST)
        quarterform = QuarterForm(request.POST)
        tup = gav.create_app(GlobalVariables.sof_val, GlobalVariables.cat_val, GlobalVariables.type_val,
                             GlobalVariables.yr_val, GlobalVariables.qrtr_val)
        print("lst_app",tup[0])
        GlobalVariables.lst_app = tup[0]
        GlobalVariables.app_id = tup[1]


        context = {
            'with_requests': GlobalVariables.with_req,
            'sofform': sofform,
            'catform' : catform,
            'yrform' : yrform,
            'typeform': typeform,
            'quarterform':quarterform,
            'modal_type': 'One',
            'with_value' : with_value,
            'lst_results': lst_results,
            'cat_val':GlobalVariables.cat_val,
            'yr_val': GlobalVariables.yr_val,
            'type_val' : GlobalVariables.type_val,
            'sof_val' : GlobalVariables.sof_val,
            'qrtr_val':GlobalVariables.qrtr_val,
            'code_val': gav.get_code(GlobalVariables.cat_val),
            'lst_app' : GlobalVariables.lst_app
        }


    else:
        with_value = False
        lst_results = []

        sofform = SOFForm(request.POST)
        catform = CATForm(request.POST)
        yrform = YRForm(request.POST)
        typeform = TypeForm(request.POST)
        quarterform = QuarterForm(request.POST)
        context = {
            'with_requests': GlobalVariables.with_req,
            'sofform': sofform,
            'catform' : catform,
            'yrform' : yrform,
            'typeform': typeform,
            'quarterform': quarterform,
            'modal_type': 'One',
            'with_value' : with_value,
            'lst_results': lst_results
        }

    return render(request, 'PPMP/app.html', context)

def requests(request, parameter):
    GlobalVariables.with_req = cto.check_temp_order()

    if parameter == '999996':

        itod.yes_update(GlobalVariables.temp_id,request.POST.get('price_request'), request.POST.get('comment_request'), "")
        gen = GlobalVariables.gen_to_add
        lst_specs = GlobalVariables.specs_to_add
        print("LST_SPECS",lst_specs)
        lst_values = GlobalVariables.temp_order_details
        itod.insert_itemdescription(GlobalVariables.temp_id,request.POST.get('price_request'),request.POST.get('unit_request'),lst_values[2],lst_values[3],lst_values[4],lst_values[5],lst_values[6],GlobalVariables.ppmp)
        # itod.insert_prices(request.POST.get('price_request'), request.POST.get('unit_request'), GlobalVariables.temp_id)
        # ['100', 'ream', 0, 1, 1, 0, '2020-10-17']
    elif parameter == '999995':

        try:
            s1 = request.POST.get('specifics1').strip()
        except:
            s1 = 'None'
        try:
            s2 = request.POST.get('specifics2').strip()
        except:
            s2 = 'None'
        try:
            s3 = request.POST.get('specifics3').strip()
        except:
            s3 = 'None'
        try:
            s4 = request.POST.get('specifics4').strip()
        except:
            s4 = 'None'
        try:
            s5 = request.POST.get('specifics5').strip()
        except:
            s5 = 'None'

        if s1 == '':
            s1 = 'None'
        if s2 == '':
            s2 = 'None'
        if s3 == '':
            s3 = 'None'
        if s4 == '':
            s4 = 'None'
        if s5 == '':
            s5 = 'None'
        specs = "++".join([s1,s2,s3,s4,s5])
        itod.no_update(GlobalVariables.temp_id,"", request.POST.get('comment_request'), specs)

    context = {
        'modal_type': 'One',
        'with_requests': GlobalVariables.with_req,
        'lst_requests': cto.get_temp_order(),
        'with_requests': GlobalVariables.with_req,
    }


    return render(request, 'PPMP/requests.html', context)


def requestsyes(request, parameter):
    pricerequestform = PriceRequestForm(request.POST)
    commentrequestform = CommentRequestForm(request.POST)
    unitrequestform = UnitRequestForm(request.POST)
    GlobalVariables.with_req = cto.check_temp_order()

    val = ''
    for i in cto.get_temp_order():
        if str(parameter) == str(i[0]):
            GlobalVariables.temp_id = i[0]
            val = i
            break
    lst = []
    print("GLOBAL VARIABLES TEMP ID: ",GlobalVariables.temp_id)
    lst_values = cto.get_temp_order_details(int(GlobalVariables.temp_id))
    GlobalVariables.temp_order_details = lst_values
    lst.append(val)
    # ['100', 'ream', 0, 1, 1, 0]
    GlobalVariables.date_temp_order_details = lst_values[6]
    context = {
        'price_suggested':lst_values[0],
        'unit_suggested':lst_values[1],
        'first_quarter':lst_values[2],
        'second_quarter':lst_values[3],
        'third_quarter':lst_values[4],
        'fourth_quater':lst_values[5],
        'pricerequestform':pricerequestform,
        'commentrequestform': commentrequestform,
        'unitrequestform':unitrequestform,
        'modal_type': 'Two',
        'with_requests': GlobalVariables.with_req,
        'lst_requests':lst,
        'with_requests': GlobalVariables.with_req,

    }

    return render(request, 'PPMP/requests.html', context)

def requestsno(request, parameter):
    GlobalVariables.with_req = cto.check_temp_order()
    pricerequestform = PriceRequestForm(request.POST)
    commentrequestform = CommentRequestForm(request.POST)

    specifics = gil.get_spec1()
    for i in cto.get_temp_order():
        if str(parameter) == str(i[0]):
            GlobalVariables.temp_id = i[0]
            val = i
            break
    lst = []
    lst.append(val)

    for i in cto.get_temp_specs():
        if str(parameter) == str(i[0]):
            val1 = i
            break
    context = {
        'specifics': specifics,
        'pricerequestform': pricerequestform,
        'commentrequestform': commentrequestform,
        'modal_type': 'Three',
        'with_requests': GlobalVariables.with_req,
        'lst_requests': lst,
        'specifics1': Specifics1(initial={'specifics1': val1[1]}),
        'specifics2': Specifics2(initial={'specifics2': val1[2]}),
        'specifics3': Specifics3(initial={'specifics3': val1[3]}),
        'specifics4': Specifics4(initial={'specifics4': val1[4]}),
        'specifics5': Specifics5(initial={'specifics5': val1[5]}),
        'with_requests': GlobalVariables.with_req,
    }

    return render(request, 'PPMP/requests.html', context)


class IndexView(generic.ListView):
    template_name = 'PPMP/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'PPMP/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'PPMP/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'PPMP/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('HR:results', args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def get_queryset(self):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]
