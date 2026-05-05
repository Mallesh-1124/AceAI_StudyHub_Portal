const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// ─── Helper ─────────────────────────────────────────────────

async function request(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw { status: res.status, ...error };
  }

  // Handle 204 No Content
  if (res.status === 204) return null;
  return res.json();
}

// ─── Auth ───────────────────────────────────────────────────

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export async function register(data: {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}): Promise<User> {
  return request('/auth/register/', { method: 'POST', body: JSON.stringify(data) });
}

export async function login(data: {
  username: string;
  password: string;
}): Promise<User> {
  return request('/auth/login/', { method: 'POST', body: JSON.stringify(data) });
}

export async function logout(): Promise<void> {
  return request('/auth/logout/', { method: 'POST' });
}

export async function getMe(): Promise<User> {
  return request('/auth/me/');
}

// ─── Rooms ──────────────────────────────────────────────────

export interface StudyRoom {
  id: number;
  name: string;
  subject: string;
  description: string;
  created_by: User;
  capacity: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  ai_teaching_style: string;
  ai_difficulty: string;
  ai_instructions: string;
  member_count: number;
  is_member: boolean;
  members?: RoomMember[];
}

export interface RoomMember {
  id: number;
  user: User;
  role: string;
  joined_at: string;
  is_online: boolean;
}

export async function getRooms(): Promise<StudyRoom[]> {
  return request('/rooms/');
}

export async function getRoom(id: number): Promise<StudyRoom> {
  return request(`/rooms/${id}/`);
}

export async function createRoom(data: {
  name: string;
  subject: string;
  description?: string;
  capacity?: number;
}): Promise<StudyRoom> {
  return request('/rooms/', { method: 'POST', body: JSON.stringify(data) });
}

export async function deleteRoom(id: number): Promise<void> {
  return request(`/rooms/${id}/`, { method: 'DELETE' });
}

export async function joinRoom(id: number) {
  return request(`/rooms/${id}/join/`, { method: 'POST' });
}

export async function leaveRoom(id: number) {
  return request(`/rooms/${id}/leave/`, { method: 'POST' });
}

// ─── Messages ───────────────────────────────────────────────

export interface ChatMessage {
  id: number;
  user: User | null;
  sender_name: string;
  content: string;
  is_ai: boolean;
  created_at: string;
}

export async function getRoomMessages(roomId: number): Promise<ChatMessage[]> {
  return request(`/rooms/${roomId}/messages/`);
}

export async function askAI(roomId: number, question: string) {
  return request(`/rooms/${roomId}/ai-ask/`, {
    method: 'POST',
    body: JSON.stringify({ question }),
  });
}

// ─── Session Summary ────────────────────────────────────────

export interface SessionSummary {
  summary: string;
  key_topics: string[];
  key_takeaways: string[];
  study_tips: string[];
  difficulty_assessment?: string;
  suggested_next_topics?: string[];
  questions_asked: number;
  ai_responses: number;
  total_messages: number;
}

export async function generateSummary(roomId: number): Promise<SessionSummary> {
  return request(`/rooms/${roomId}/summary/`, { method: 'POST' });
}

// ─── Quiz ───────────────────────────────────────────────────

export interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  correct_answer: string;
  explanation: string;
}

export interface Quiz {
  quiz_title: string;
  questions: QuizQuestion[];
  error?: string;
}

export interface QuizResult {
  id: number;
  question: string;
  your_answer: string;
  correct_answer: string;
  is_correct: boolean;
  explanation: string;
}

export interface QuizEvaluation {
  score: number;
  total: number;
  percentage: number;
  feedback: string;
  results: QuizResult[];
}

export async function generateQuiz(roomId: number, numQuestions = 5): Promise<Quiz> {
  return request(`/rooms/${roomId}/quiz/`, {
    method: 'POST',
    body: JSON.stringify({ num_questions: numQuestions }),
  });
}

export async function evaluateQuiz(
  roomId: number,
  quizData: Quiz,
  answers: Record<string, string>
): Promise<QuizEvaluation> {
  return request(`/rooms/${roomId}/quiz/evaluate/`, {
    method: 'POST',
    body: JSON.stringify({ quiz_data: quizData, answers }),
  });
}

// ─── Admin ──────────────────────────────────────────────────

export interface AdminStats {
  stats: {
    total_rooms: number;
    total_users: number;
    total_messages: number;
    active_members: number;
    ai_messages: number;
  };
  recent_rooms: StudyRoom[];
  recent_messages: ChatMessage[];
}

export interface StudyMaterial {
  id: number;
  title: string;
  description: string;
  subject: string;
  semester: string;
  material_type: string;
  file: string | null;
  url: string | null;
  uploaded_by: User;
  room: number | null;
  is_public: boolean;
  created_at: string;
  updated_at: string;
}

export interface Badge {
  id: number;
  name: string;
  badge_type: string;
  description: string;
  icon: string | null;
  criteria: string;
  points: number;
  created_at: string;
}

export interface UserBadge {
  id: number;
  badge: Badge;
  earned_at: string;
}

export interface UserProfile {
  id: number;
  user: User;
  bio: string;
  avatar: string | null;
  preferred_subjects: string;
  learning_goal: string;
  timezone: string;
  badges: UserBadge[];
  progress: UserProgress;
  created_at: string;
  updated_at: string;
}

export interface UserProgress {
  id: number;
  user: User;
  total_sessions: number;
  total_hours: number;
  total_ai_questions: number;
  materials_uploaded: number;
  forum_posts: number;
  total_points: number;
  current_streak: number;
  longest_streak: number;
  last_active: string;
  created_at: string;
  updated_at: string;
}

export async function getMyProfile(): Promise<UserProfile> {
  return request('/users/profile/');
}

export async function updateMyProfile(data: Partial<{
  bio: string;
  preferred_subjects: string;
  learning_goal: string;
  timezone: string;
}>): Promise<UserProfile> {
  return request('/users/profile/', {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function getMyProgress(): Promise<UserProgress> {
  return request('/users/progress/');
}

export async function getMyBadges(): Promise<UserBadge[]> {
  return request('/badges/user/');
}

export async function getBadges(): Promise<Badge[]> {
  return request('/badges/');
}

export async function getRoomMaterials(roomId: number): Promise<StudyMaterial[]> {
  return request(`/materials/?room_id=${roomId}`);
}

export async function getGlobalMaterials(): Promise<StudyMaterial[]> {
  return request(`/materials/`);
}

export async function uploadMaterial(data: FormData): Promise<StudyMaterial> {
  const url = `${API_BASE}/materials/`;
  const res = await fetch(url, {
    method: 'POST',
    credentials: 'include',
    body: data,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw { status: res.status, ...error };
  }

  return res.json();
}

export async function getAdminStats(): Promise<AdminStats> {
  return request('/admin/stats/');
}

// ─── Forum ───────────────────────────────────────────────────

export interface ForumReply {
  id: number;
  author: User;
  content: string;
  is_accepted: boolean;
  upvotes: number;
  created_at: string;
  updated_at: string;
}

export interface ForumPost {
  id: number;
  title: string;
  content: string;
  category: string;
  subject: string;
  author: User;
  room: number | null;
  is_pinned: boolean;
  is_solved: boolean;
  views_count: number;
  upvotes: number;
  replies: ForumReply[];
  reply_count: number;
  created_at: string;
  updated_at: string;
}

export async function getForumPosts(params?: { subject?: string; category?: string; roomId?: number }): Promise<ForumPost[]> {
  const query = new URLSearchParams()
  if (params?.subject) query.set('subject', params.subject)
  if (params?.category) query.set('category', params.category)
  if (params?.roomId) query.set('room_id', String(params.roomId))
  const queryString = query.toString() ? `?${query.toString()}` : ''
  return request(`/forum/posts/${queryString}`)
}

export async function createForumPost(data: {
  title: string
  content: string
  category: string
  subject: string
  room?: number
}): Promise<ForumPost> {
  return request('/forum/posts/', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function getForumReplies(postId: number): Promise<ForumReply[]> {
  return request(`/forum/posts/${postId}/replies/`)
}

export async function createForumReply(postId: number, content: string): Promise<ForumReply> {
  return request(`/forum/posts/${postId}/replies/`, {
    method: 'POST',
    body: JSON.stringify({ content, post: postId }),
  })
}

// ─── Study Schedule ───────────────────────────────────────────

export interface ScheduleReminder {
  id: number;
  user: User;
  reminder_sent_at: string | null;
  is_attending: boolean;
}

export interface StudySchedule {
  id: number;
  title: string;
  subject: string;
  description: string;
  room: number | null;
  organizer: User;
  scheduled_at: string;
  duration_minutes: number;
  frequency: string;
  max_participants: number;
  reminder_sent: boolean;
  is_cancelled: boolean;
  reminders: ScheduleReminder[];
  created_at: string;
}

export async function getSchedules(params?: { subject?: string; roomId?: number }): Promise<StudySchedule[]> {
  const query = new URLSearchParams()
  if (params?.subject) query.set('subject', params.subject)
  if (params?.roomId) query.set('room_id', String(params.roomId))
  const queryString = query.toString() ? `?${query.toString()}` : ''
  return request(`/schedule/${queryString}`)
}

export async function createSchedule(data: {
  title: string
  subject: string
  description: string
  room?: number
  scheduled_at: string
  duration_minutes: number
  frequency: string
  max_participants: number
}): Promise<StudySchedule> {
  return request('/schedule/', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function rsvpSchedule(scheduleId: number, isAttending = true): Promise<ScheduleReminder> {
  return request(`/schedule/${scheduleId}/rsvp/`, {
    method: 'POST',
    body: JSON.stringify({ is_attending: isAttending }),
  })
}
