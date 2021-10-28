

from django.contrib import admin

from .models import Choice, Question,CostCenter,SourceOfFund,PPMP,Category,Item,ItemDescription,Prices,OrderDetails,Signatories_Position,Signatories,PurchaseRequest



admin.site.register(CostCenter)
admin.site.register(SourceOfFund)
admin.site.register(PPMP)
admin.site.register(Category)
admin.site.register(ItemDescription)
admin.site.register(Item)
admin.site.register(Signatories_Position)
admin.site.register(Signatories)
admin.site.register(PurchaseRequest)