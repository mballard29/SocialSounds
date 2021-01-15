import os
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate 
from django.contrib import messages 
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer

from api.auth.utils import AuthTools
from api import settings as api_settings
from .models import *
from .serializers import *
from .forms import PostForm

import urllib.parse

# This is really dumb and ugly, but this is just temporary until we
# work out handling user authentication tokens for Spotify
os.environ['SPOTIPY_CLIENT_ID'] = '446f486d921147e79de265cda0a0949a'
os.environ['SPOTIPY_CLIENT_SECRET'] = '1d73a2e13e484680aeb2ae7d1da07a1b'

spotify = spotipy.client.Spotify(client_credentials_manager=SpotifyClientCredentials())

def NewPost(request):
    # def get(self, request):
    #     return render(request, self.template_view)

    # def post(self, request):  
    user = request.user
    template_view = 'api/newpost.html'
    print(request)
    print(request.method)
    print(request.POST)
    if request.method == "POST": 
        player_data = {}
        if 'album_id' in request.POST: 
            album_id = request.POST['album_id']
            caption = request.POST['caption']
            user = request.user 

            player_data = {
                'album_id':album_id,
                'owner_id': user, 
                'caption': caption
            }

            player, created = Player.objects.get_or_create(album_id=album_id, owner=user)
            print(player)
            player.save() 

            item, created = Item.objects.get_or_create(player=player, owner=user, caption=caption)
            item.save()
            
            return redirect('/api/items/')


    return render(request, template_view)


class ItemList(generics.ListCreateAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/detail.html'

    queryset = Item.objects.all()
    # queryset = Item.objects.filter(owner=user)
    serializer_class = ItemSerializer

    # ensures you need to be logged in to view items
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    # def post(self, request): 

    def get(self, request):
        user = request.user 
        # posts = Item.objects.filter(owner = user)
        posts = Item.objects.all()
        template = loader.get_template(self.template_name)
        context = {
            'posts': posts 
        }
        return HttpResponse(template.render(context, request))
        # self.object = self.get_object()
        # return render(request, self.template_name, {'posts': self.queryset})
        # return Response({'posts': self.object}, template_name=self.template_name)
        # return render(self.template_name, {'posts': self.serializer_class.data})

    def list(self, request):
        self.serializer_class = ItemSerializer
        return super(ItemList, self).list(request)
        # return render(request, self.template_name, )
        # return Response({'queryset':queryset})

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer

    # ensures you need to be logged in to view items
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def retrieve(self, request, pk):
        queryset = self.get_object()
        serializer = ItemDetailSerializer(queryset, many=False)
        return Response(serializer.data)

class PlayerList(generics.ListCreateAPIView):
    template_view = 'api/newpost.html'

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    # ensures you need to be logged in to view players
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def list(self, request):
        self.serializer_class = PlayerSerializer
        return super(PlayerList, self).list(request)

class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Player.objects.all()
    serializer_class = PlayerDetailSerializer

    # ensures you need to be logged in to view players
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def retrieve(self, request, pk):
        queryset = self.get_object()
        serializer = PlayerDetailSerializer(queryset, many=False)
        return Response(serializer.data)

# allows for POST of likes
class LikeView(generics.CreateAPIView):

    serializer_class = LikeViewSerializer

    def post(self, request):
        
        # read data as a dict to string theough dumps
        # convert to JSON dict through loads
        dataRead = json.dumps(request.data)
        data = json.loads(dataRead)

        if not 'item_id' in data:
            return Response({'error': 'no item_id in request.'}, status=status.HTTP_400_BAD_REQUEST)

        item = Item.objects.get(pk=data['item_id'])

        try:
            like = Like()
            like.item = item
            like.owner = request.user
            like.save()
        except IntegrityError:
            return Response({'error': 'This item has already been liked by this particular user.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ItemDetailSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

# allows for POST of comments
class CommentView(generics.CreateAPIView):

    serializer_class = CommentViewSerializer

    def post(self, request):
        
        # read data as a dict to string theough dumps
        # convert to JSON dict through loads
        dataRead = json.dumps(request.data)
        data = json.loads(dataRead)

        if not 'item_id' in data:
            return Response({'error': 'no item_id in request.'}, status=status.HTTP_400_BAD_REQUEST)

        if not 'body' in data:
            return Response({'error': 'no body in request.'}, status=status.HTTP_400_BAD_REQUEST)

        item = Item.objects.get(pk=data['item_id'])

        comment = Comment()
        comment.item = item
        comment.body = data['body']
        comment.is_caption = data['is_caption']
        comment.owner = request.user
        comment.save()

        serializer = ItemDetailSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(('GET',))
def spotify_search(request, query='', type='album'):
    result = spotify.search(query, type=type)
    return Response(result, status=status.HTTP_200_OK) 
