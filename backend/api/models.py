from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class UserProfile(models.Model):
    """Extended user profile with learning preferences."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    preferred_subjects = models.CharField(max_length=500, blank=True, default='')  # comma-separated
    learning_goal = models.CharField(max_length=255, blank=True, default='')
    timezone = models.CharField(max_length=50, default='UTC')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class StudyRoom(models.Model):
    """A virtual study room where students can collaborate."""
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    capacity = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # AI teacher settings
    ai_teaching_style = models.CharField(
        max_length=50,
        default='guided',
        choices=[
            ('guided', 'Step-by-step guidance'),
            ('direct', 'Direct answers'),
            ('socratic', 'Socratic method'),
        ]
    )
    ai_difficulty = models.CharField(
        max_length=20,
        default='medium',
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ]
    )
    ai_instructions = models.TextField(
        blank=True,
        default='Explain step-by-step, guide the student but don\'t give direct answers.'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.subject})"


class RoomMember(models.Model):
    """Tracks users who have joined a study room."""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_online = models.BooleanField(default=False)

    class Meta:
        unique_together = ('room', 'user')
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"


class ChatMessage(models.Model):
    """A chat message in a study room."""
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    content = models.TextField()
    is_ai = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        sender = 'AI Teacher' if self.is_ai else (self.user.username if self.user else 'Unknown')
        return f"{sender}: {self.content[:50]}"


class StudyMaterial(models.Model):
    """Study resources: PDFs, documents, videos uploaded by instructors/admins."""
    MATERIAL_TYPES = [
        ('pdf', 'PDF Document'),
        ('doc', 'Word Document'),
        ('video', 'Video'),
        ('image', 'Image'),
        ('link', 'External Link'),
    ]
    
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, default='')
    subject = models.CharField(max_length=100)
    semester = models.CharField(max_length=50, blank=True, default='')  # e.g., "Spring 2026"
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES, default='pdf')
    
    # File or URL
    file = models.FileField(
        upload_to='study_materials/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'ppt', 'pptx', 'mp4', 'jpg', 'png'])]
    )
    url = models.URLField(blank=True, null=True)  # For external links or videos
    
    # Metadata
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='materials_uploaded')
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, related_name='materials', blank=True, null=True)
    is_public = models.BooleanField(default=True)  # Visible to all students
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.subject})"


class Badge(models.Model):
    """Achievement badges for gamification."""
    BADGE_TYPES = [
        ('content_creator', 'Content Creator'),
        ('active_participant', 'Active Participant'),
        ('ai_explorer', 'AI Explorer'),
        ('forum_expert', 'Forum Expert'),
        ('study_streak', 'Study Streak'),
        ('quiz_master', 'Quiz Master'),
    ]
    
    name = models.CharField(max_length=100)
    badge_type = models.CharField(max_length=50, choices=BADGE_TYPES, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', blank=True, null=True)
    criteria = models.TextField(blank=True, default='')  # How to earn this badge
    points = models.IntegerField(default=10)  # Points awarded for earning badge
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """Tracks earned badges by users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class UserProgress(models.Model):
    """Track user learning progress and statistics."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progress')
    
    # Statistics
    total_sessions = models.IntegerField(default=0)
    total_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # Hours spent studying
    total_ai_questions = models.IntegerField(default=0)
    materials_uploaded = models.IntegerField(default=0)
    forum_posts = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    
    # Streaks
    current_streak = models.IntegerField(default=0)  # Days
    longest_streak = models.IntegerField(default=0)  # Days
    last_active = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Progress"


class ForumPost(models.Model):
    """Main forum thread/question post."""
    CATEGORY_CHOICES = [
        ('General', 'General Discussion'),
        ('Homework', 'Homework Help'),
        ('Exam Prep', 'Exam Preparation'),
        ('Resources', 'Resource Sharing'),
        ('Question', 'Question'),
    ]
    
    title = models.CharField(max_length=300)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    subject = models.CharField(max_length=100, blank=True, default='')
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, related_name='forum_posts', blank=True, null=True)
    
    is_pinned = models.BooleanField(default=False)
    is_solved = models.BooleanField(default=False)  # Marks if question is answered
    
    views_count = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return self.title


class ForumReply(models.Model):
    """Reply to a forum post."""
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_replies')
    content = models.TextField()
    
    is_accepted = models.BooleanField(default=False)  # Marks best/accepted answer
    upvotes = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_accepted', '-upvotes', 'created_at']

    def __str__(self):
        return f"Reply by {self.author.username} to {self.post.title[:30]}"


class StudySchedule(models.Model):
    """Scheduled study sessions."""
    FREQUENCY_CHOICES = [
        ('One-time', 'One-time'),
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Bi-weekly', 'Bi-weekly'),
    ]
    
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    
    room = models.ForeignKey(StudyRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedules')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_sessions')
    
    scheduled_at = models.DateTimeField()  # When the session will occur
    duration_minutes = models.IntegerField(default=60)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='once')
    max_participants = models.IntegerField(default=10)
    
    # Tracking
    reminder_sent = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_at']

    def __str__(self):
        return f"{self.title} - {self.scheduled_at.strftime('%Y-%m-%d %H:%M')}"


class ScheduleReminder(models.Model):
    """Tracks which users were reminded about a scheduled session."""
    schedule = models.ForeignKey(StudySchedule, on_delete=models.CASCADE, related_name='reminders')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_sent_at = models.DateTimeField(auto_now_add=True)
    is_attending = models.BooleanField(default=False)  # RSVP

    class Meta:
        unique_together = ('schedule', 'user')

    def __str__(self):
        return f"Reminder: {self.user.username} - {self.schedule.title}"
