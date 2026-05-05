from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudyMaterial, ChatMessage, UserBadge, Badge, UserProgress, ForumPost, RoomMember

@receiver(post_save, sender=StudyMaterial)
def update_material_stats(sender, instance, created, **kwargs):
    if created and instance.uploaded_by:
        user = instance.uploaded_by
        progress, _ = UserProgress.objects.get_or_create(user=user)
        progress.materials_uploaded += 1
        progress.save()
        
        # Check for Content Creator badge
        try:
            badge = Badge.objects.get(badge_type='content_creator')
            if not UserBadge.objects.filter(user=user, badge=badge).exists():
                UserBadge.objects.create(user=user, badge=badge)
                # Award points
                progress.total_points += badge.points
                progress.save()
        except Badge.DoesNotExist:
            pass

@receiver(post_save, sender=ChatMessage)
def update_ai_stats(sender, instance, created, **kwargs):
    if created and not instance.is_ai and instance.user:
        # Check if this was a question to AI (usually handled in the view, but let's check content)
        # Actually, ai_ask_view already handles it, but let's be safe for other contexts
        pass

@receiver(post_save, sender=ForumPost)
def update_forum_stats(sender, instance, created, **kwargs):
    if created:
        user = instance.author
        progress, _ = UserProgress.objects.get_or_create(user=user)
        progress.forum_posts += 1
        progress.save()
        
        # Check for Forum Expert badge
        if progress.forum_posts >= 5:
            try:
                badge = Badge.objects.get(badge_type='forum_expert')
                if not UserBadge.objects.filter(user=user, badge=badge).exists():
                    UserBadge.objects.create(user=user, badge=badge)
                    progress.total_points += badge.points
                    progress.save()
            except Badge.DoesNotExist:
                pass

@receiver(post_save, sender=RoomMember)
def update_participation_stats(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        progress, _ = UserProgress.objects.get_or_create(user=user)
        progress.total_sessions += 1
        progress.save()
        
        # Check for Active Participant badge
        if progress.total_sessions >= 5:
            try:
                badge = Badge.objects.get(badge_type='active_participant')
                if not UserBadge.objects.filter(user=user, badge=badge).exists():
                    UserBadge.objects.create(user=user, badge=badge)
                    progress.total_points += badge.points
                    progress.save()
            except Badge.DoesNotExist:
                pass
