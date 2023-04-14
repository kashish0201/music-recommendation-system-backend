from rest_framework import serializers
from .models import Song, Liked_song


#songs serializer


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"


class LikedSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liked_song
        fields = "__all__"