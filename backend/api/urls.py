from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/me/', views.me_view, name='me'),

    # Rooms
    path('rooms/', views.room_list_view, name='room-list'),
    path('rooms/<int:room_id>/', views.room_detail_view, name='room-detail'),
    path('rooms/<int:room_id>/join/', views.room_join_view, name='room-join'),
    path('rooms/<int:room_id>/leave/', views.room_leave_view, name='room-leave'),
    path('rooms/<int:room_id>/messages/', views.room_messages_view, name='room-messages'),
    path('rooms/<int:room_id>/ai-ask/', views.ai_ask_view, name='ai-ask'),
    path('rooms/<int:room_id>/summary/', views.session_summary_view, name='session-summary'),
    path('rooms/<int:room_id>/quiz/', views.quiz_generate_view, name='quiz-generate'),
    path('rooms/<int:room_id>/quiz/evaluate/', views.quiz_evaluate_view, name='quiz-evaluate'),

    # Admin
    path('admin/stats/', views.admin_stats_view, name='admin-stats'),

    # Study Materials
    path('materials/', views.materials_list_view, name='materials-list'),
    path('materials/<int:material_id>/', views.material_detail_view, name='material-detail'),

    # Badges & Gamification
    path('badges/', views.badges_list_view, name='badges-list'),
    path('badges/user/', views.user_badges_view, name='user-badges'),
    path('badges/award/', views.award_badge_view, name='award-badge'),

    # User Progress & Profile
    path('users/<int:user_id>/progress/', views.user_progress_view, name='user-progress'),
    path('users/progress/', views.user_progress_view, name='my-progress'),
    path('users/<int:user_id>/profile/', views.user_profile_view, name='user-profile'),
    path('users/profile/', views.user_profile_view, name='my-profile'),

    # Forum
    path('forum/posts/', views.forum_posts_list_view, name='forum-posts-list'),
    path('forum/posts/<int:post_id>/', views.forum_post_detail_view, name='forum-post-detail'),
    path('forum/posts/<int:post_id>/replies/', views.forum_replies_view, name='forum-replies'),
    path('forum/replies/<int:reply_id>/', views.forum_reply_detail_view, name='forum-reply-detail'),

    # Study Schedule
    path('schedule/', views.schedule_list_view, name='schedule-list'),
    path('schedule/<int:schedule_id>/', views.schedule_detail_view, name='schedule-detail'),
    path('schedule/<int:schedule_id>/rsvp/', views.schedule_rsvp_view, name='schedule-rsvp'),
]
