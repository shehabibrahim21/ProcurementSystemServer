from django.urls import path
from django.conf.urls import url, include
from . import views
from django.views.generic import TemplateView
app_name = 'PPMP'
urlpatterns = [
    path('', views.index, name='index'),
    path(r'^index/print_rfq-(?P<parameter>[\w-]+).html', views.print_rfq, name='print_rfq'),
    path(r'^index/create_rfq-(?P<parameter>[\w-]+).html', views.create_rfq, name='create_rfq'),
    path(r'^index/change_group-(?P<parameter>[\w-]+).html', views.change_group, name='change_group'),
    path(r'^index/set_group-(?P<parameter>[\w-]+).html', views.set_group, name='set_group'),
    path(r'^index/edit_ppmp-(?P<parameter>[\w-]+).html', views.edit_ppmp, name='edit_ppmp'),
    path(r'^index/group_items-(?P<parameter>[\w-]+).html', views.group_items, name='group_items'),
    path(r'^index/edit_items_delete-(?P<parameter>[\w-]+).html', views.edit_items_delete, name='edit_items_delete'),
    path(r'^index/savedetails-(?P<parameter>[\w-]+).html', views.savedetails, name='savedetails'),
    path(r'^index/test-(?P<parameter>[\w-]+).html', views.test, name='test'),
    path(r'^index/set_price-(?P<parameter>[\w-]+).html', views.set_price, name='set_price'),
    path(r'^index/view_pr-(?P<parameter>[\w-]+).html', views.view_pr, name='view_pr'),
    path(r'^index/show_pr-(?P<parameter>[\w-]+).html', views.show_pr, name='show_pr'),
    path(r'^index/purchase_request-(?P<parameter>[\w-]+).html', views.purchase_request, name='purchase_request'),
    path(r'^index/purchase_request_save-(?P<parameter>[\w-]+).html', views.purchase_request_save, name='purchase_request_save'),
    path(r'^index/print_ppmp-(?P<parameter>[\w-]+).html', views.print_ppmp,  name='print_ppmp'),
    path(r'^index/print_app-(?P<parameter>[\w-]+).html', views.print_app, name='print_app'),
    path(r'^index/print_pr-(?P<parameter>[\w-]+).html', views.print_pr, name='print_pr'),
    path(r'^index/add_create_ppmp_category-(?P<parameter>[\w-]+).html', views.add_create_ppmp_category, name='add_create_ppmp_category'),
    path(r'^index/suggest_item-(?P<parameter>[\w-]+).html', views.suggest_item, name='suggest_item'),
    path(r'^index/extend_modal_four-(?P<parameter>[\w-]+).html', views.extend_modal_four, name='extend_modal_four'),
    path(r'^index/search_gen_specifics_modal_four-(?P<parameter>[\w-]+).html', views.search_gen_specifics_modal_four, name='search_gen_specifics_modal_four'),
    path(r'^index/add_items_modal_four-(?P<parameter>[\w-]+).html', views.add_items_modal_four,name='add_items_modal_four'),
    path(r'^index/insert_order_temporary_details-(?P<parameter>[\w-]+).html', views.insert_order_temporary_details,  name='insert_order_temporary_details'),
    path(r'^index/edit_items_modal_three-(?P<parameter>[\w-]+).html', views.edit_items_modal_three, name='edit_items_modal_three'),
    path(r'^index/change_category_modal_three-(?P<parameter>[\w-]+).html', views.change_category_modal_three, name='change_category_modal_three'),
    path(r'^index/change_category_create_ppmp-(?P<parameter>[\w-]+).html', views.change_category_create_ppmp,name='change_category_create_ppmp'),
    path(r'^index/index-(?P<parameter>[\w-]+).html', views.ppmp, name='ppmp'),
    path(r'^index/create_ppmp-(?P<parameter>[\w-]+).html', views.create_ppmp, name='create_ppmp'),
    path(r'^index/cost_center_modal_one-(?P<parameter>[\w-]+).html', views.cost_center_modal_one, name='cost_center_modal_one'),
    path(r'^index/update_year_modal_one-(?P<parameter>[\w-]+).html', views.update_year_modal_one, name='update_year_modal_one'),
    path(r'^index/clicked_modal_one-(?P<parameter>[\w-]+).html', views.clicked_modal_one, name='clicked_modal_one'),
    path(r'^index/app-(?P<parameter>[\w-]+).html', views.app, name='app'),
    path(r'^index/reports-(?P<parameter>[\w-]+).html', views.reports, name='reports'),
    path(r'^index/requests-(?P<parameter>[\w-]+).html', views.requests, name='requests'),
    path(r'^index/requestsyes-(?P<parameter>[\w-]+).html', views.requestsyes, name='requestsyes'),
    path(r'^index/requestsno-(?P<parameter>[\w-]+).html', views.requestsno, name='requestsno'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),


]