import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import StudyMaterial, Badge, UserBadge, UserProgress, ForumPost, RoomMember

def backfill_badges():
    users = User.objects.all()
    for user in users:
        progress, _ = UserProgress.objects.get_or_create(user=user)
        
        # 1. Content Creator
        if StudyMaterial.objects.filter(uploaded_by=user).exists():
            badge = Badge.objects.get(badge_type='content_creator')
            if not UserBadge.objects.filter(user=user, badge=badge).exists():
                UserBadge.objects.create(user=user, badge=badge)
                progress.total_points += badge.points
                print(f"Awarded Content Creator to {user.username}")
        
        # 2. Forum Expert
        post_count = ForumPost.objects.filter(author=user).count()
        if post_count >= 5:
            badge = Badge.objects.get(badge_type='forum_expert')
            if not UserBadge.objects.filter(user=user, badge=badge).exists():
                UserBadge.objects.create(user=user, badge=badge)
                progress.total_points += badge.points
                print(f"Awarded Forum Expert to {user.username}")
        
        # 3. Active Participant
        session_count = RoomMember.objects.filter(user=user).count()
        if session_count >= 5:
            badge = Badge.objects.get(badge_type='active_participant')
            if not UserBadge.objects.filter(user=user, badge=badge).exists():
                UserBadge.objects.create(user=user, badge=badge)
                progress.total_points += badge.points
                print(f"Awarded Active Participant to {user.username}")
        
        # Sync statistics
        progress.materials_uploaded = StudyMaterial.objects.filter(uploaded_by=user).count()
        progress.forum_posts = post_count
        progress.total_sessions = session_count
        progress.save()

if __name__ == '__main__':
    backfill_badges()
