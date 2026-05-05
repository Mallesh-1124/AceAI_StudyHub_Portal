from django.contrib import admin
from .models import (
    StudyRoom, RoomMember, ChatMessage, StudyMaterial, Badge,
    UserBadge, UserProgress, ForumPost, ForumReply, StudySchedule,
    ScheduleReminder, UserProfile
)

@admin.register(StudyRoom)
class StudyRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_by', 'capacity', 'is_active', 'created_at')
    list_filter = ('is_active', 'subject', 'ai_teaching_style')
    search_fields = ('name', 'subject')

@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'role', 'is_online', 'joined_at')
    list_filter = ('role', 'is_online')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'is_ai', 'content_preview', 'created_at')
    list_filter = ('is_ai',)

    def content_preview(self, obj):
        return obj.content[:80]
    content_preview.short_description = 'Content'


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'semester', 'material_type', 'uploaded_by', 'is_public', 'created_at')
    list_filter = ('material_type', 'subject', 'is_public', 'created_at')
    search_fields = ('title', 'subject')


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'badge_type', 'points', 'created_at')
    list_filter = ('badge_type',)
    search_fields = ('name', 'description')


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'earned_at')
    list_filter = ('badge', 'earned_at')
    search_fields = ('user__username',)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_sessions', 'total_hours', 'total_points', 'current_streak', 'last_active')
    list_filter = ('last_active',)
    search_fields = ('user__username',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'learning_goal', 'timezone', 'created_at')
    list_filter = ('timezone',)
    search_fields = ('user__username', 'preferred_subjects')


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'subject', 'is_pinned', 'is_solved', 'views_count', 'created_at')
    list_filter = ('category', 'is_pinned', 'is_solved', 'created_at')
    search_fields = ('title', 'content')


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'is_accepted', 'upvotes', 'created_at')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('content', 'author__username')


@admin.register(StudySchedule)
class StudyScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'organizer', 'scheduled_at', 'frequency', 'is_cancelled', 'created_at')
    list_filter = ('frequency', 'is_cancelled', 'scheduled_at')
    search_fields = ('title', 'subject')


@admin.register(ScheduleReminder)
class ScheduleReminderAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'user', 'is_attending', 'reminder_sent_at')
    list_filter = ('is_attending', 'reminder_sent_at')
    search_fields = ('user__username', 'schedule__title')
