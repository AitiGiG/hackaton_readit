from rest_framework import serializers
from .models import Platform, GamePassport, PostGame, GameLike, GameComment, Activity, ActivityParticipation

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name']

class GamePassportSerializer(serializers.ModelSerializer):
    platforms = PlatformSerializer(many=True, read_only=True)

    class Meta:
        model = GamePassport
        fields = ['id', 'user', 'nickname', 'description', 'avatar', 'gender', 'platforms', 'experience_years']

class PostGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostGame
        fields = ['id', 'passport', 'image', 'text']

class GameLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameLike
        fields = ['id', 'post', 'user']

class GameCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameComment
        fields = ['id', 'post', 'user', 'text']
        

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'description', 'creator', 'participants', 'selected_participant']

class ActivityParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityParticipation
        fields = ['id', 'activity', 'participant', 'is_ready']