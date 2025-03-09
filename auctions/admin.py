from django.contrib import admin

from .models import Listing, Comments,Category,Bid
# Register your models here.

admin.site.register(Listing)
#admin.site.register(Auction)
admin.site.register(Comments)
admin.site.register(Bid)
#admin.site.register(Watchlist)
admin.site.register(Category)