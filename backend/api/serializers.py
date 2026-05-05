from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    StudyRoom, RoomMember, ChatMessage, StudyMaterial, Badge,
    UserBadge, UserProgress, ForumPost, ForumReply, StudySchedule,
    ScheduleReminder, UserProfile
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RoomMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = RoomMember
        fields = ['id', 'user', 'role', 'joined_at', 'is_online']


class StudyRoomSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = StudyRoom
        fields = [
            'id', 'name', 'subject', 'description', 'created_by',
            'capacity', 'is_active', 'created_at', 'updated_at',
            'ai_teaching_style', 'ai_difficulty', 'ai_instructions',
            'member_count', 'is_member',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.members.filter(user=request.user).exists()
        return False


class StudyRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyRoom
        fields = ['name', 'subject', 'description', 'capacity',
                  'ai_teaching_style', 'ai_difficulty', 'ai_instructions']


class ChatMessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'sender_name', 'content', 'is_ai', 'created_at']

    def get_sender_name(self, obj):
        if obj.is_ai:
            return 'AI Teacher'
        return obj.user.username if obj.user else 'Unknown'


class AIAskSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=2000)


# ─── Study Materials ─────────────────────────────────────────

class StudyMaterialSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = StudyMaterial
        fields = [
            'id', 'title', 'description', 'subject', 'semester',
            'material_type', 'file', 'url', 'uploaded_by', 'room',
            'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = ['uploaded_by', 'created_at', 'updated_at']


class StudyMaterialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'subject', 'semester', 'material_type', 'file', 'url', 'room', 'is_public']


# ─── Badges & Gamification ──────────────────────────────────

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'badge_type', 'description', 'icon', 'criteria', 'points', 'created_at']


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = ['id', 'badge', 'earned_at']


class UserProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProgress
        fields = [
            'id', 'user', 'total_sessions', 'total_hours', 'total_ai_questions',
            'materials_uploaded', 'forum_posts', 'total_points',
            'current_streak', 'longest_streak', 'last_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    badges = serializers.SerializerMethodField()
    progress = UserProgressSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'avatar', 'preferred_subjects', 'learning_goal', 'timezone', 'badges', 'progress', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_badges(self, obj):
        badges = obj.user.earned_badges.all()
        return UserBadgeSerializer(badges, many=True).data


# ─── Forum ───────────────────────────────────────────────────

class ForumReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = ForumReply
        fields = ['id', 'author', 'content', 'is_accepted', 'upvotes', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']


class ForumPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = ForumReplySerializer(many=True, read_only=True)
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = ForumPost
        fields = [
            'id', 'title', 'content', 'category', 'subject', 'author',
            'room', 'is_pinned', 'is_solved', 'views_count', 'upvotes',
            'replies', 'reply_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'views_count', 'created_at', 'updated_at']

    def get_reply_count(self, obj):
        return obj.replies.count()


class ForumPostCreateSerializer(serializers.ModelSerializer):
    room = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'category', 'subject', 'room']


class ForumReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumReply
        fields = ['content', 'post']


# ─── Study Schedule ─────────────────────────────────────────

class ScheduleReminderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ScheduleReminder
        fields = ['id', 'user', 'reminder_sent_at', 'is_attending']


class StudyScheduleSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    reminders = ScheduleReminderSerializer(many=True, read_only=True)

    class Meta:
        model = StudySchedule
        fields = [
            'id', 'title', 'subject', 'description', 'room', 'organizer',
            'scheduled_at', 'duration_minutes', 'frequency', 'max_participants',
            'reminder_sent', 'is_cancelled', 'reminders', 'created_at'
        ]
        read_only_fields = ['organizer', 'reminder_sent', 'created_at']


class StudyScheduleCreateSerializer(serializers.ModelSerializer):
    room = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = StudySchedule
        fields = ['title', 'subject', 'description', 'room', 'scheduled_at', 'duration_minutes', 'frequency', 'max_participants']
