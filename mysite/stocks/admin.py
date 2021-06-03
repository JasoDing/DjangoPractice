from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Account)
admin.site.register(Stock_lst)
admin.site.register(Favourite)
admin.site.register(Temp_histroy1)
admin.site.register(RecentStockData)
admin.site.register(contactinfo)
admin.site.register(watchlist)