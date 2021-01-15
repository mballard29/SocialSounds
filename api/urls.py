from django.urls import path, include
from .views import *
from .auth import urls as auth_urls

app_name = 'api'
urlpatterns = [
    path('auth/', include(auth_urls)),

    path('items/', ItemList.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),

    path('players/', PlayerList.as_view(), name='player-list'),
    path('new_post/', NewPost, name='NewPost'),
    path('players/<int:pk>/', PlayerDetail.as_view(), name='player-detail'),

    path('like/', LikeView.as_view(), name='like'),
    path('comment/', CommentView.as_view(), name='comment'),
    
    path('search/<str:type>/<str:query>/', spotify_search),
    path('search/<str:query>/', spotify_search)
]
