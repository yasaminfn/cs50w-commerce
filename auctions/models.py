from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName


class Bid(models.Model):
    bid_price = models.DecimalField(max_digits=10, decimal_places=2, default="0")
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bid")
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default="starting_bid")
    image_url = models.URLField(blank=True, null=True, max_length=4000)  
    closed = models.BooleanField(default=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlistuser")

    def __str__(self):  
        return self.title 
    


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="userscommnet")
    content = models.CharField(max_length=300)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name="listingscomment")

    def __str__(self):
        return f"{self.user} commented {self.content} on {self.listing}."
