from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django import forms


class Profile(models.Model):
    
    ROLE_CHOICES = (
        ('consumer', 'Consumer'),
        ('staff', 'Staff'),
    )
    
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    website_url = models.CharField(max_length=255, blank=True, null=True)
    follows = models.ManyToManyField('self', blank=True)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES)
    # all profiles are public
    
    def __str__(self):
        return 'Profile: %s' % self.owner.username

class Player(models.Model):
    # this is the Spotify album_id that works with embedded Spotify player and spotipy
    album_id = models.CharField(max_length=255)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False)

    def __str__(self):
        return "Player: %s" % self.album_id

    @property
    def embed_url(self):
        album = str(self.album_id)
        if album.find("track") != -1:
            index = album.find("track") + 6
            return "https://open.spotify.com/embed/track/%s/" % (album[index:]) 
        if album.find("album") != -1:
            index = album.find("album") + 6
            return "https://open.spotify.com/embed/album/%s/" % (album[index:])

    @property
    def embed_html_tag_compact(self):
        return "%s%s%s" % ('<iframe src="', self.embed_url, '" width="360" height="440" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>')

class Item(models.Model):       # post
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Item: %s: %s" % (self.owner.username, self.player.album_id)

    @property
    def total_likes(self):
        return Like.objects.filter(item_id=self.id).count()

    @property
    def likes(self):
        array = []
        for like in Like.objects.filter(item_id=self.id):
            array.append(like.owner.username)
        return array

    @property
    def total_comments(self):
        return Comment.objects.filter(item_id=self.id).count()

    @property
    def comments(self):
        array = []
        for comment in Comment.objects.filter(item_id=self.id):
            c = dict()
            c['username'] = comment.owner.username
            c['body'] = comment.body
            c['is_caption'] = comment.is_caption
            array.append(c)
        return array

class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    # one User gets one Like per Item
    class Meta:
        unique_together = ('item', 'owner',)

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    body = models.TextField(max_length=150)
    is_caption = models.BooleanField(blank=False, null=False)
    commented_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
