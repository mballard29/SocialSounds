from django.contrib import admin

from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['owner']

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['album_id', 'owner']
    
    """
    TODO:
    could add a "preview" function to return an HTML tag for the player
    this should be able to be used to embed Spotify web player
    use base_url property and full_url method in Player model
    can allow tags "preview.allow_tags" or something similar
    """

class ItemAdmin(admin.ModelAdmin):
    list_display = ['owner', 'player', 'created_at']

class LikeAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
