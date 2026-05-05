import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Badge

def seed_badges():
    badges = [
        {
            'name': 'Content Creator',
            'badge_type': 'content_creator',
            'description': 'Awarded for uploading your first study material.',
            'criteria': 'Upload 1 study material.',
            'points': 50
        },
        {
            'name': 'Active Participant',
            'badge_type': 'active_participant',
            'description': 'Awarded for participating in 5 study sessions.',
            'criteria': 'Join 5 different study rooms.',
            'points': 100
        },
        {
            'name': 'AI Explorer',
            'badge_type': 'ai_explorer',
            'description': 'Awarded for asking the AI teacher 10 questions.',
            'criteria': 'Ask 10 questions to the AI assistant.',
            'points': 75
        },
        {
            'name': 'Forum Expert',
            'badge_type': 'forum_expert',
            'description': 'Awarded for posting 5 helpful topics in the forum.',
            'criteria': 'Post 5 threads in the forum.',
            'points': 150
        },
        {
            'name': 'Quiz Master',
            'badge_type': 'quiz_master',
            'description': 'Awarded for scoring 100% on a study room quiz.',
            'criteria': 'Get a perfect score on any quiz.',
            'points': 200
        },
        {
            'name': 'Study Streak',
            'badge_type': 'study_streak',
            'description': 'Awarded for a 7-day study streak.',
            'criteria': 'Be active for 7 consecutive days.',
            'points': 250
        }
    ]

    for b in badges:
        badge, created = Badge.objects.get_or_create(
            badge_type=b['badge_type'],
            defaults={
                'name': b['name'],
                'description': b['description'],
                'criteria': b['criteria'],
                'points': b['points']
            }
        )
        if created:
            print(f"Created badge: {badge.name}")
        else:
            print(f"Badge already exists: {badge.name}")

if __name__ == '__main__':
    seed_badges()
