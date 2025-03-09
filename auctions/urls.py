from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlistings", views.createlistings, name = "createlistings"),
    path("<int:listing_id>", views.listing, name = "listing"),
    path("<int:listing_id>/page", views.page, name = "page"),
    path("categories", views.categorylist, name="categorylist"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addtowatchlist/<int:listing_id>", views.addwatchlist, name="addtowatchlist"),
    path("removewatchlist/<int:listing_id>", views.removewatchlist, name="removewatchlist"),
    path("addcomment/<int:listing_id>", views.addcomment, name="addcomment"),
    path("addbid/<int:listing_id>", views.addbid, name="addbid"),
    path("closeauction/<int:listing_id>", views.close, name="closeauction"),
    
    
]
