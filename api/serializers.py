from django.db.models.fields import IntegerField, TextField
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = (
            'id',
            'bio',
            'website_url',
        )
        read_only_fields = ('id',)

class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(many=False)

    groups = serializers.SerializerMethodField('get_user_groups')
    def get_user_groups(self, user):
        results = []
        for group in user.groups.all():
            results.append(group.name)

        return results
    class Meta:
        model = User
        fields = (
            'id',
            User.USERNAME_FIELD,
            'first_name',
            'last_name',
            'email',
            'profile',
            'groups',
        )
        read_only_fields = (
            'id',
            'groups',
            'profile',
        )

class UserDetailSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            User.USERNAME_FIELD,
            'first_name',
            'last_name',
            'email',
            'groups',
        )
        read_only_fields = fields


class UserListSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            User.USERNAME_FIELD,
            'first_name',
            'last_name',
            'email',
        )
        read_only_fields = fields

# class UserSerializer(ModelSerializer):
    
#     class Meta:
#         model = User
#         fields = (
#             'id',
#             'username',
#             'email',
#         )

class ItemSerializer(serializers.ModelSerializer):
    
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Item
        fields = (
            'id',
            'player',
            'owner',
            'created_at',
        )
        read_only_fields = ('id',)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class ItemDetailSerializer(serializers.ModelSerializer):
    
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Item
        fields = (
            'id',
            'player',
            'owner',
            'total_likes',
            'likes',
            'total_comments',
            'comments',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id',)

class PlayerSerializer(serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    # TODO: will need to add url, etc in below Meta
    class Meta:
        model = Player
        fields = (
            'id',
            'album_id',
            'owner',
            'embed_url',
            'embed_html_tag_compact',
            'created_at',
        )
        read_only_fields = ('id',)

class PlayerDetailSerializer(serializers.ModelSerializer):

    owner = UserSerializer(many=False, read_only=True)

    # TODO: will need to add url, etc in below Meta
    class Meta:
        model = Player
        fields = (
            'id',
            'album_id',
            'owner',
            'embed_url',
            'embed_html_tag_compact',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id',)

class LikeViewSerializer(serializers.Serializer):
    
    item_id = serializers.IntegerField()

class CommentViewSerializer(serializers.Serializer):
    
    item_id = serializers.IntegerField()
    body = serializers.CharField()
    is_caption = serializers.BooleanField()