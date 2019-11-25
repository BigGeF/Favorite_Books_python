from django.conf.urls import url
from . import views	
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^show_books$', views.show_books),
    url(r'^show_book_others$', views.show_book_others),
    url(r'^show_books_my/(?P<id>[0-9]+)$', views.show_books_my),
    url(r'^post_user$', views.post_user),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add_book$', views.add_book),
    url(r'^add_to_fav/(?P<id>[0-9]+)$', views.add_to_fav),

]