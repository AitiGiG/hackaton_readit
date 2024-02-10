from django.contrib import admin
from .models import GamePassport, PostGame, GameLike, GameComment, Activity, ActivityParticipation, Platform

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(GamePassport)
class GamePassportAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'gender', 'experience_years']
    search_fields = ['nickname', 'user__username', 'gender']
    list_filter = ['gender', 'platforms']

@admin.register(PostGame)
class PostGameAdmin(admin.ModelAdmin):
    list_display = ['passport', 'text']
    search_fields = ['passport__nickname', 'text']
    list_filter = ['passport__gender']

@admin.register(GameLike)
class GameLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user']
    search_fields = ['post__text', 'user__username']

@admin.register(GameComment)
class GameCommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'text']
    search_fields = ['post__text', 'user__username', 'text']

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'description']
    search_fields = ['title', 'creator__username', 'description']
    list_filter = ['creator']

@admin.register(ActivityParticipation)
class ActivityParticipationAdmin(admin.ModelAdmin):
    list_display = ['activity', 'participant', 'is_ready']
    search_fields = ['activity__title', 'participant__username']
    list_filter = ['is_ready']