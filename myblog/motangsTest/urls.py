from django.urls import path
from .views import index,post_detail,post_list,post_share,post_search
from .feeds import LastestPostFeed
#post_list,PostListView

urlpatterns = [
    path('index/',index),
    ####
    path('',post_list,name='post_list'),
    path('tag/<slug:tag_slug>/',post_list, name='post_list_by_tag'),
    #（同一url）
    ####
    # path('',PostListView.as_view(),name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',post_detail,name= 'post_detail'),
    path('<int:post_id>/share/',post_share,name='post_share'),
    path('feed/', LastestPostFeed(), name='post_feed'),
    path('search/', post_search, name='post_search'),
    
]
