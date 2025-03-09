from django.contrib.auth import authenticate, login, logout  
from django.db import IntegrityError  
from django.http import HttpResponse, HttpResponseRedirect  
from django.shortcuts import render, redirect  
from django.urls import reverse  
from decimal import Decimal
from django.contrib import messages
from .models import User, Listing, Comments, Category ,Bid

def index(request):  
    active = Listing.objects.filter(closed = False)
    return render(request, "auctions/index.html", {
        "listings" : active,
    })  


def login_view(request):  
    if request.method == "POST":  
        username = request.POST["username"]  
        password = request.POST["password"]  
        user = authenticate(request, username=username, password=password)  

        if user is not None:  
            login(request, user)  
            return HttpResponseRedirect(reverse("index"))  
        else:  
            return render(request, "auctions/login.html", {  
                "message": "Invalid username and/or password."  
            })  
    else:  
        return render(request, "auctions/login.html")  


def logout_view(request):  
    logout(request)  
    return HttpResponseRedirect(reverse("index"))  


def register(request):  
    if request.method == "POST":  
        username = request.POST["username"]  
        email = request.POST["email"]  
        password = request.POST["password"]  
        confirmation = request.POST["confirmation"]  
        if password != confirmation:  
            return render(request, "auctions/register.html", {  
                "message": "Passwords must match."  
            })  

        try:  
            user = User.objects.create_user(username, email, password)  
            user.save()  
        except IntegrityError:  
            return render(request, "auctions/register.html", {  
                "message": "Username already taken."  
            })  
        login(request, user)  
        return HttpResponseRedirect(reverse("index"))  
    else:  
        return render(request, "auctions/register.html")  
    


def createlistings(request):  
    if request.method == "POST":  
        title = request.POST["title"]  
        description = request.POST["description"]  
        starting_bid = request.POST["starting_bid"]  
        img_url = request.POST["image-url"]
        category = request.POST["category"]
        currentuser = request.user
        

        categorydata = Category.objects.get(categoryName=category)
        bid=Bid(
            bid_price=starting_bid,
            user=currentuser
        )
        bid.save()

        listing = Listing(  
            title=title,  
            description=description,  
            starting_bid=bid,  
            image_url=img_url,
            seller=currentuser,
            category=categorydata,
            current_price=starting_bid,
        )  
        listing.save()  

        return redirect("index")  
    else:  
        return render(request, "auctions/createlistings.html", {
            "category": Category.objects.all(),
        })
    
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    watchlist = request.user in listing.watchlist.all()
    comments = listing.listingscomment.all()
    isowner = listing.seller.username == request.user.username
        

    #or comments=Comments.objects.filter(listing=listing_id)
    return render(request, "auctions/listingpage.html", {
        "listing": listing,
        "watchlist": watchlist,
        "comments" : comments,
        "isowner" : isowner,
    })

def page(request, listing_id):  
    listings = Listing.objects.get(id=listing_id)
    return HttpResponseRedirect(reverse("page", args=(listings.id,)))

def watchlist(request):
    currentuser = request.user
    listings = currentuser.watchlistuser.all
    return render(request, "auctions/watchlist.html",{
        "listings" :listings
    })

def addwatchlist(request, listing_id):
    if request.method == 'POST':
        listingdata=Listing.objects.get(pk=listing_id)
        currentuser=request.user
        listingdata.watchlist.add(currentuser)
        allwatchlistitems = currentuser.watchlistuser.all
        return render(request, "auctions/watchlist.html", {
            "listings": allwatchlistitems, #[] fixed the iteration problem
            'message': f'Added {listingdata} to watchlist!'})
    
def removewatchlist(request, listing_id):
    if request.method == 'POST':
        listingdata=Listing.objects.get(pk=listing_id)
        currentuser=request.user
        listingdata.watchlist.remove(currentuser)
        allwatchlistitems = currentuser.watchlistuser.all
        return render(request, "auctions/watchlist.html", {
            "listings": allwatchlistitems,
            'message': f'Removed {listingdata} From watchlist!'})
    

def categorylist(request):
    cat = Category.objects.all()
    return render(request, "auctions/categorylist.html",{
        "category" : cat
    })

def category(request, category_id):
    cat = Category.objects.get(id=category_id)
    listing = Listing.objects.all()
    return render(request, "auctions/category.html",{
        "category" : cat,
        "listings": listing,
    })

def addcomment(request, listing_id):
    if request.method == "POST": 
        content=request.POST["newcomment"]
        listing=Listing.objects.get(id=listing_id)
        user=request.user

        newcomment = Comments(
            user=user,
            content=content,
            listing=listing,

        )
        newcomment.save()
        return redirect(reverse('listing', args=[listing_id]))
    
def addbid(request, listing_id):
    if request.method == "POST": 
        bid_price=request.POST["newbid"]

        if not bid_price:  
            messages.error(request, "Bid price is required.")  
            return redirect('auctions:listing_page', listing_id=listing_id)
        
        user=request.user
        listing = Listing.objects.get(id=listing_id)

        watchlist= request.user in listing.watchlist.all()
        comments=listing.listingscomment.all()
        print(bid_price)
        print(listing.starting_bid,bid_price)
        #highest_bid = Bid.objects.filter(listing=listing).order_by('-bid_price').first()  


        if Decimal(bid_price) > listing.current_price:  
            newbid = Bid(
                bid_price=bid_price,
                user=user,
            )

            newbid.save()
            listing.current_price = bid_price  
            listing.save()  

        else:
            return render(request, "auctions/listingpage.html", {
            "listing": listing,
            'message': 'failed to update bid! ',
            'update': False, 
            "watchlist": watchlist,
            "comments" : comments,
            })
    
        return render(request, "auctions/listingpage.html", {
            "listing": listing,
            'message': 'bid was updated successfully! ',
            'updated': True, 
            "watchlist": watchlist,
            "comments" : comments,
            })

def close(request, listing_id):
    listing=Listing.objects.get(id=listing_id)
    listing.closed=True
    listing.save()
    active = Listing.objects.filter(closed = False)
    return render(request, "auctions/index.html", {
        "listings" : active,
        "message" : 'Your Auction is Closed!',
    })  


