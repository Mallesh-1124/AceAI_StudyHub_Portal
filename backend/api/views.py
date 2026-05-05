from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import (
    StudyRoom, RoomMember, ChatMessage, StudyMaterial, Badge,
    UserBadge, UserProgress, ForumPost, ForumReply, StudySchedule,
    ScheduleReminder, UserProfile
)
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    StudyRoomSerializer, StudyRoomCreateSerializer,
    ChatMessageSerializer, AIAskSerializer,
    StudyMaterialSerializer, StudyMaterialCreateSerializer,
    BadgeSerializer, UserBadgeSerializer, UserProgressSerializer, UserProfileSerializer,
    ForumPostSerializer, ForumPostCreateSerializer, ForumReplySerializer, ForumReplyCreateSerializer,
    StudyScheduleSerializer, StudyScheduleCreateSerializer, ScheduleReminderSerializer, RoomMemberSerializer
)


# ─── Auth Views ──────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register a new user."""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login with username and password."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response(
            {'detail': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout the current user."""
    logout(request)
    return Response({'detail': 'Logged out successfully.'})


@api_view(['GET'])
@permission_classes([AllowAny])
def me_view(request):
    """Get the currently authenticated user."""
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(UserSerializer(request.user).data)


# ─── Room Views ──────────────────────────────────────────────

@api_view(['GET', 'POST'])
def room_list_view(request):
    """List all rooms or create a new one."""
    if request.method == 'GET':
        rooms = StudyRoom.objects.filter(is_active=True)
        serializer = StudyRoomSerializer(rooms, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = StudyRoomCreateSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(created_by=request.user)
            # Auto-join creator as admin
            RoomMember.objects.create(room=room, user=request.user, role='admin')
            return Response(
                StudyRoomSerializer(room, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def room_detail_view(request, room_id):
    """Get room details or delete a room."""
    try:
        room = StudyRoom.objects.get(id=room_id)
    except StudyRoom.DoesNotExist:
        return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudyRoomSerializer(room, context={'request': request})
        data = serializer.data
        # Include members list
        members = RoomMember.objects.filter(room=room).select_related('user')
        data['members'] = RoomMemberSerializer(members, many=True).data
        return Response(data)

    if request.method == 'DELETE':
        if not request.user.is_authenticated or room.created_by != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        room.is_active = False
        room.save()
        return Response({'detail': 'Room deleted.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def room_join_view(request, room_id):
    """Join a study room."""
    try:
        room = StudyRoom.objects.get(id=room_id, is_active=True)
    except StudyRoom.DoesNotExist:
        return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

    member, created = RoomMember.objects.get_or_create(
        room=room, user=request.user,
        defaults={'role': 'student'}
    )
    member.is_online = True
    member.save()

    return Response({
        'detail': 'Joined room.' if created else 'Already a member.',
        'role': member.role,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def room_leave_view(request, room_id):
    """Leave a study room."""
    try:
        member = RoomMember.objects.get(room_id=room_id, user=request.user)
        member.is_online = False
        member.save()
        return Response({'detail': 'Left room.'})
    except RoomMember.DoesNotExist:
        return Response({'detail': 'Not a member.'}, status=status.HTTP_404_NOT_FOUND)


# ─── Chat Views ──────────────────────────────────────────────

@api_view(['GET'])
def room_messages_view(request, room_id):
    """List messages for a room."""
    try:
        room = StudyRoom.objects.get(id=room_id)
    except StudyRoom.DoesNotExist:
        return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

    messages = ChatMessage.objects.filter(room=room).select_related('user')[:100]
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)


# ─── AI Teacher (Gemini-powered) ─────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_ask_view(request, room_id):
    """Ask the AI teacher a question — powered by Google Gemini."""
    from .ai_service import ask_ai_teacher

    try:
        room = StudyRoom.objects.get(id=room_id, is_active=True)
    except StudyRoom.DoesNotExist:
        return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AIAskSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    question = serializer.validated_data['question']

    # Save the student's question
    ChatMessage.objects.create(
        room=room, user=request.user, content=question, is_ai=False
    )

    # Get recent messages for context
    recent_msgs = list(ChatMessage.objects.filter(room=room).select_related('user').order_by('-created_at')[:10])
    recent_msgs.reverse()

    # Generate AI response via Gemini
    ai_response = ask_ai_teacher(question, room, recent_msgs)
    ai_msg = ChatMessage.objects.create(
        room=room, user=None, content=ai_response, is_ai=True
    )

    return Response({
        'question': question,
        'response': ai_response,
        'message': ChatMessageSerializer(ai_msg).data,
    })


# ─── Session Summary ─────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def session_summary_view(request, room_id):
    """Generate an AI-powered session summary."""
    from .ai_service import generate_session_summary

    try:
        room = StudyRoom.objects.get(id=room_id)
    except StudyRoom.DoesNotExist:
        return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

    messages = list(ChatMessage.objects.filter(room=room).select_related('user').order_by('created_at'))
    summary = generate_session_summary(room, messages)

    return Response(summary)


# ─── Quiz Generation ─────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def quiz_generate_view(request, room_id):
    """Generate a quiz based on the study session."""
    from .ai_service import generate_quiz

    try:
        room = StudyRoom.objects.get(id=room_id)
    except StudyRoom.DoesNotExist:
        return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

    messages = list(ChatMessage.objects.filter(room=room).select_related('user').order_by('created_at'))
    num_questions = request.data.get('num_questions', 5)
    quiz = generate_quiz(room, messages, num_questions=int(num_questions))

    return Response(quiz)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def quiz_evaluate_view(request, room_id):
    """Evaluate quiz answers and return results."""
    from .ai_service import evaluate_quiz_answers

    quiz_data = request.data.get('quiz_data', {})
    user_answers = request.data.get('answers', {})

    if not quiz_data or not user_answers:
        return Response(
            {'detail': 'quiz_data and answers are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    results = evaluate_quiz_answers(quiz_data, user_answers)
    return Response(results)


# ─── Admin Stats ─────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_stats_view(request):
    """Get platform statistics for the admin dashboard."""
    total_rooms = StudyRoom.objects.filter(is_active=True).count()
    total_users = User.objects.count()
    total_messages = ChatMessage.objects.count()
    active_members = RoomMember.objects.filter(is_online=True).count()
    ai_messages = ChatMessage.objects.filter(is_ai=True).count()

    # Recent rooms
    recent_rooms = StudyRoom.objects.filter(is_active=True)[:10]
    rooms_data = StudyRoomSerializer(recent_rooms, many=True, context={'request': request}).data

    # Recent messages
    recent_messages = ChatMessage.objects.select_related('user', 'room').order_by('-created_at')[:20]
    messages_data = ChatMessageSerializer(recent_messages, many=True).data

    return Response({
        'stats': {
            'total_rooms': total_rooms,
            'total_users': total_users,
            'total_messages': total_messages,
            'active_members': active_members,
            'ai_messages': ai_messages,
        },
        'recent_rooms': rooms_data,
        'recent_messages': messages_data,
    })


# ─── Study Materials ─────────────────────────────────────────

@api_view(['GET', 'POST'])
def materials_list_view(request):
    """List study materials or upload a new one."""
    if request.method == 'GET':
        subject = request.query_params.get('subject', '')
        semester = request.query_params.get('semester', '')
        material_type = request.query_params.get('type', '')
        
        materials = StudyMaterial.objects.filter(is_public=True)
        if subject:
            materials = materials.filter(subject=subject)
        if semester:
            materials = materials.filter(semester=semester)
        if material_type:
            materials = materials.filter(material_type=material_type)
        
        serializer = StudyMaterialSerializer(materials, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = StudyMaterialCreateSerializer(data=request.data)
        if serializer.is_valid():
            material = serializer.save(uploaded_by=request.user)
            return Response(
                StudyMaterialSerializer(material).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def material_detail_view(request, material_id):
    """Get material details or delete material."""
    try:
        material = StudyMaterial.objects.get(id=material_id)
    except StudyMaterial.DoesNotExist:
        return Response({'detail': 'Material not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudyMaterialSerializer(material)
        return Response(serializer.data)

    if request.method == 'DELETE':
        if not request.user.is_authenticated or material.uploaded_by != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        material.delete()
        return Response({'detail': 'Material deleted.'}, status=status.HTTP_204_NO_CONTENT)


# ─── Badges & Gamification ──────────────────────────────────

@api_view(['GET'])
def badges_list_view(request):
    """Get all available badges."""
    badges = Badge.objects.all()
    serializer = BadgeSerializer(badges, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_badges_view(request):
    """Get user's earned badges."""
    user_badges = UserBadge.objects.filter(user=request.user).select_related('badge')
    serializer = UserBadgeSerializer(user_badges, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def award_badge_view(request):
    """Award a badge to a user (admin only)."""
    user_id = request.data.get('user_id')
    badge_id = request.data.get('badge_id')

    if not user_id or not badge_id:
        return Response(
            {'detail': 'user_id and badge_id are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(id=user_id)
        badge = Badge.objects.get(id=badge_id)
    except (User.DoesNotExist, Badge.DoesNotExist):
        return Response({'detail': 'User or badge not found.'}, status=status.HTTP_404_NOT_FOUND)

    user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)

    if not created:
        return Response({'detail': 'User already has this badge.'}, status=status.HTTP_400_BAD_REQUEST)

    # Update user progress
    progress, _ = UserProgress.objects.get_or_create(user=user)
    progress.total_points += badge.points
    progress.save()

    return Response(
        UserBadgeSerializer(user_badge).data,
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_progress_view(request, user_id=None):
    """Get user progress and statistics."""
    if user_id is None:
        user_id = request.user.id

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    progress, _ = UserProgress.objects.get_or_create(user=user)
    serializer = UserProgressSerializer(progress)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile_view(request, user_id=None):
    """Get or update user profile."""
    if user_id is None:
        user_id = request.user.id

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Only allow users to edit their own profile
    if request.method == 'PUT' and user.id != request.user.id and not request.user.is_staff:
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─── Forum ───────────────────────────────────────────────────

@api_view(['GET', 'POST'])
def forum_posts_list_view(request):
    """List forum posts or create a new one."""
    if request.method == 'GET':
        subject = request.query_params.get('subject', '')
        category = request.query_params.get('category', '')
        room_id = request.query_params.get('room_id', '')

        posts = ForumPost.objects.all()
        if subject:
            posts = posts.filter(subject=subject)
        if category:
            posts = posts.filter(category=category)
        if room_id:
            posts = posts.filter(room_id=room_id)

        serializer = ForumPostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = ForumPostCreateSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user)
            # Update user progress
            progress, _ = UserProgress.objects.get_or_create(user=request.user)
            progress.forum_posts += 1
            progress.save()
            return Response(
                ForumPostSerializer(post).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PATCH'])
def forum_post_detail_view(request, post_id):
    """Get, update, or delete a forum post."""
    try:
        post = ForumPost.objects.get(id=post_id)
    except ForumPost.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        post.views_count += 1
        post.save()
        serializer = ForumPostSerializer(post)
        return Response(serializer.data)

    if request.method == 'DELETE':
        if not request.user.is_authenticated or post.author != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({'detail': 'Post deleted.'}, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PATCH':
        if not request.user.is_authenticated or post.author != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        if 'is_solved' in request.data:
            post.is_solved = request.data['is_solved']
        if 'upvotes' in request.data:
            post.upvotes += request.data['upvotes']
        
        post.save()
        serializer = ForumPostSerializer(post)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def forum_replies_view(request, post_id):
    """Get replies for a post or create a new reply."""
    try:
        post = ForumPost.objects.get(id=post_id)
    except ForumPost.DoesNotExist:
        return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        replies = ForumReply.objects.filter(post=post)
        serializer = ForumReplySerializer(replies, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = ForumReplyCreateSerializer(data=request.data)
        if serializer.is_valid():
            reply = serializer.save(author=request.user, post=post)
            # Update user progress
            progress, _ = UserProgress.objects.get_or_create(user=request.user)
            progress.forum_posts += 1
            progress.save()
            return Response(
                ForumReplySerializer(reply).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'PATCH'])
def forum_reply_detail_view(request, reply_id):
    """Update or delete a forum reply."""
    try:
        reply = ForumReply.objects.get(id=reply_id)
    except ForumReply.DoesNotExist:
        return Response({'detail': 'Reply not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        if not request.user.is_authenticated or reply.author != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        reply.delete()
        return Response({'detail': 'Reply deleted.'}, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PATCH':
        if not request.user.is_authenticated or reply.author != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        if 'is_accepted' in request.data:
            reply.is_accepted = request.data['is_accepted']
        if 'upvotes' in request.data:
            reply.upvotes += request.data['upvotes']
        
        reply.save()
        serializer = ForumReplySerializer(reply)
        return Response(serializer.data)


# ─── Study Schedule ─────────────────────────────────────────

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def schedule_list_view(request):
    """List scheduled study sessions or create a new one."""
    if request.method == 'GET':
        subject = request.query_params.get('subject', '')
        room_id = request.query_params.get('room_id', '')

        schedules = StudySchedule.objects.filter(is_cancelled=False)
        if subject:
            schedules = schedules.filter(subject=subject)
        if room_id:
            schedules = schedules.filter(room_id=room_id)

        serializer = StudyScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = StudyScheduleCreateSerializer(data=request.data)
        if serializer.is_valid():
            schedule = serializer.save(organizer=request.user)
            return Response(
                StudyScheduleSerializer(schedule).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def schedule_detail_view(request, schedule_id):
    """Get, update, or delete a scheduled session."""
    try:
        schedule = StudySchedule.objects.get(id=schedule_id)
    except StudySchedule.DoesNotExist:
        return Response({'detail': 'Schedule not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudyScheduleSerializer(schedule)
        return Response(serializer.data)

    if request.method == 'DELETE':
        if schedule.organizer != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        schedule.is_cancelled = True
        schedule.save()
        return Response({'detail': 'Schedule cancelled.'}, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PATCH':
        if schedule.organizer != request.user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = StudyScheduleSerializer(schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def schedule_rsvp_view(request, schedule_id):
    """RSVP to attend a scheduled session."""
    try:
        schedule = StudySchedule.objects.get(id=schedule_id)
    except StudySchedule.DoesNotExist:
        return Response({'detail': 'Schedule not found.'}, status=status.HTTP_404_NOT_FOUND)

    is_attending = request.data.get('is_attending', True)

    reminder, created = ScheduleReminder.objects.get_or_create(
        schedule=schedule,
        user=request.user,
        defaults={'is_attending': is_attending}
    )

    if not created:
        reminder.is_attending = is_attending
        reminder.save()

    return Response(ScheduleReminderSerializer(reminder).data)

