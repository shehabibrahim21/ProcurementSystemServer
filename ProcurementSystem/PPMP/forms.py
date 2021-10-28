import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import GetYear as gy
import GetAPPValues as gav
from django.utils.safestring import mark_safe



import GetCostCentersPR as gccpr
import SaveGroup as sg
category_choices = [('category','Category'),('all','All')]
filter_choices = [('cost_center','Cost Center'),
                  ('items','Items'),
                  ('date','Date')]
quarter_choices = [('First Quarter','First Quarter'),
                  ('Second Quarter','Second Quarter'),
                  ('Third Quarter','Third Quarter'),
                  ('Fourth Quarter','Fourth Quarter'),]


sof_choices = gav.get_costcenters()
cat_choices = gav.get_category()
yr_choices = gav.get_year()
# eyr1_choices = [(2020,2020),(2019,2019)]
# print(yr1_choices)
type_choices = gav.get_type()
cc_choices = gccpr.get_cc()
group_choices = sg.get_group_app_for_select()

# class GroupForm(forms.Form):
#
#     )
#     university = forms.ChoiceField(
#         label="Select your university",
#         choices=UNIVERSITIES,
#     )
class SearchGroupForm(forms.Form):
    searchgroupform = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_group','class':'autocomplete_group','size': 60})

    )
class GroupForm(forms.Form):

    group = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_group','class':'autocomplete_group','size': 100})
     )

class PriceForm(forms.Form):
    price_form = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'price_field','class':'price_field','size': 20})
    )

class QuarterForm(forms.Form):

    quarter = forms.CharField(label = False,required=False, widget=forms.Select(choices=quarter_choices))

class UnitRequestForm(forms.Form):
   unit_request= forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'price_request','class':'price_request'})
    )

class PriceRequestForm(forms.Form):
    price_request= forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'price_request','class':'price_request'})
    )
class CommentRequestForm(forms.Form):
    comment_request= forms.CharField(label = False,required=False,
        widget=forms.Textarea(attrs={'id': 'price_request','class':'price_request',"rows":5, "cols":40})
    )

class SOFForm(forms.Form):

    sof = forms.CharField(label = False,required=False, widget=forms.Select(choices=sof_choices))

class CCForm(forms.Form):

    cc = forms.CharField(label = False,required=False, widget=forms.Select(choices=cc_choices))


class CATForm(forms.Form):

    cat = forms.CharField(label = False,required=False, widget=forms.Select(choices=cat_choices))

class YRForm(forms.Form):

    yr = forms.CharField(label = False,required=False, widget=forms.Select(choices=yr_choices))

class TypeForm(forms.Form):

    type = forms.CharField(label = False,required=False, widget=forms.Select(choices=type_choices))

class CategoryForm(forms.Form):

    category_val = forms.CharField(label = False,required=False, widget=forms.Select(choices=category_choices))



class FilterForm(forms.Form):

    filter = forms.CharField(label = False,required=False, widget=forms.Select(choices=filter_choices))




class SearchCostCenterForm(forms.Form):
    cost_center = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_cost_center','class':'autocomplete_cost_center'})
    )

class SearchCategoryForm(forms.Form):
    category = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_category','class':'autocomplete_category'})
    )


class SearchItemsForm(forms.Form):
    items = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_items','class':'autocomplete_items'})
    )

class SearchQuarterForm(forms.Form):
    quarter = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_quarter','class':'autocomplete_quarter'})
    )



class SearchForm(forms.Form):
    name = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_name','class':'autocomplete_name'})
    )



class SearchItemForm(forms.Form):
    name = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_gen','class':'autocomplete_gen','size': 50})
    )
class SearchItemForm1(forms.Form):
    name = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_gen1','class':'autocomplete_gen1','size': 50})
    )


class Specifics1(forms.Form):
    specifics1 = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_item1','class':'autocomplete_item1','size': 50})
    )
class Specifics2(forms.Form):
    specifics2 = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_item2','class':'autocomplete_item2','size': 50})
    )
class Specifics3(forms.Form):
    specifics3 = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_item3','class':'autocomplete_item3','size': 50})
    )
class Specifics4(forms.Form):
    specifics4 = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_item4','class':'autocomplete_item4','size': 50})
    )
class Specifics5(forms.Form):
    specifics5 = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'autocomplete_item5','class':'autocomplete_item5','size': 50})
    )

class Quarter1(forms.Form):
    quarter1 = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'number11','class':'number11','size': 10})
    )

class Quarter2(forms.Form):
    quarter2 = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'number22','class':'number22','size': 10})
    )
class Quarter3(forms.Form):
    quarter3 = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'number33','class':'number33','size': 10})
    )
class Quarter4(forms.Form):
    quarter4 = forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'number44','class':'number44','size': 10})
    )



class CostCenterCode(forms.Form):

    cc_code = forms.CharField(label = False,required=False,
        widget=forms.TextInput()
    )

class CostCenterName(forms.Form):


    cc_name= forms.CharField(label = False,required=False,
        widget=forms.TextInput()
    )

# year_choices = gy.get_year()
# year_choices = [('category','Category'),('all','All')]
class YearForm(forms.Form):

    year= forms.CharField(label='Year',required=False, widget=forms.Select(choices=yr_choices, attrs={'name': 'yc'}))

class PriceSuggestedForm(forms.Form):
    price_suggested= forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'price_request','class':'price_request'})
    )
class UnitSuggestedForm(forms.Form):
    unit_suggested= forms.CharField(label = False,required=False,
        widget=forms.TextInput(attrs={'id': 'price_request','class':'price_request'})
    )

class DynamicForm(forms.Form):
    original_field = forms.CharField(label = False,required = False,widget=forms.TextInput(attrs={'size':70}))
    extra_field_count = forms.CharField(widget=forms.HiddenInput(attrs={'size':70}))

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(DynamicForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['extra_field_{index}'.format(index=index)] = forms.CharField(widget=forms.TextInput())
class SpecificationDetailsForm(forms.Form):

    specification_details_form= forms.CharField(label=False,required=False,  widget=forms.Textarea(attrs={'id': 'price_request','class':'price_request',"rows":10, "cols":70}))

class PurposeForm(forms.Form):

    purpose_form= forms.CharField(label=False,required=False,  widget=forms.Textarea(attrs={'id': 'price_request','class':'price_request',"rows":5, "cols":70}))