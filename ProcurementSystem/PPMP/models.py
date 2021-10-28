from django.db import models
from django.utils import timezone
import datetime
# import Retrieve as  rt
from django.contrib.auth.models import User

class GlobalVariables(models.Model):
    ppmp = ''
    cc_code = ''
    cc_name = ''
    fs_name = ''
    yr = ''
    type = ''
    remarks = ''
    lst_ppmp = ''
#
#
#
#
# class RetrieveData(models.Model):
#
#     list = rt.retrieve()
class Group(models.Model):
    STATUE_CHOICE = (
        ('draft', 'draft'),
        ('future', 'future'),
        ('trash', 'trash'),
        ('publish', 'publish'),
    )
    statue = models.CharField(max_length=10, choices=STATUE_CHOICE)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class CostCenter(models.Model):
    user = models.ManyToManyField(User)
    code = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    name = models.CharField(max_length=300)

    def __str__(self):
         return self.name



class Category(models.Model):
    code =  models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    def __str__(self):
         return self.name

class Item(models.Model):
    general_name =  models.CharField(max_length=300)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
         return self.general_name

class Signatories_Position(models.Model):
    name =  models.CharField(max_length=300)

    def __str__(self):
         return self.name

class Signatories(models.Model):
    name =  models.CharField(max_length=300)
    position_id = models.ForeignKey(Signatories_Position, on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return self.name

class SourceOfFund(models.Model):
    code = models.CharField(max_length=300)
    description = models.CharField(max_length=300)

    def __str__(self):
         return self.description



class SourceOfFund(models.Model):
    code = models.CharField(max_length=300)
    description = models.CharField(max_length=300)

    def __str__(self):
         return self.code

class PPMP(models.Model):
    sof_num = models.ForeignKey(SourceOfFund, on_delete=models.CASCADE)
    cc_num = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    type = models.CharField(max_length=300, default = 0)


class ItemDescription(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    specifics1 = models.CharField(max_length=300,blank = False)
    specifics2 = models.CharField(max_length=300,blank = False)
    specifics3 = models.CharField(max_length=300,blank =  False)
    specifics4 = models.CharField(max_length=300,blank =  False)
    specifics5 = models.CharField(max_length=300,blank =  False)

    def __str__(self):
         return  str(self.item_id) + " " + self.specifics1 + " " + self.specifics2 + " "+ self.specifics3 + " " + self.specifics4 + " " + self.specifics5

class Prices(models.Model):
    price = models.FloatField(default=0)
    item_id = models.ForeignKey(ItemDescription, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    unit  = models.CharField(max_length=300, default = 0)

    def __str__(self):
         return str(self.item_id) + str(self.price)


class OrderDetails(models.Model):
    ppmp_id = models.ForeignKey(PPMP, on_delete=models.CASCADE)
    item_description_id = models.ForeignKey(ItemDescription, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(ppmp_id) + str(item_description_id)


class PurchaseRequest(models.Model):
    orderdetails_id = models.ForeignKey(OrderDetails, on_delete=models.CASCADE)
    specification_details = models.CharField(max_length=2000, default = 0)
    purpose = models.CharField(max_length=2000,default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    
