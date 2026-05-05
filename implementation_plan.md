# Virtual Study Group — Full Implementation Plan

Build all missing functionality: Django backend (auth, rooms, chat, AI teacher) and three frontend pages (login, study room, admin dashboard).

## User Review Required

> [!IMPORTANT]
> **Database**: The [requirements.txt](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/backend/requirements.txt) lists `mysqlclient`, but for ease of local development this plan uses **SQLite** by default. MySQL can be swapped in later via settings.

> [!IMPORTANT]
> **AI Teacher**: Will use a **mock AI response system** (rule-based) since no AI API key/service is specified. This can be replaced with OpenAI/Gemini later.

> [!IMPORTANT]
> **Video (WebRTC)**: Full peer-to-peer video requires a signaling server and STUN/TURN infrastructure. This plan implements the **video UI with simulated video feeds** (camera preview via `getUserMedia`) but not multi-peer WebRTC connections. Real WebRTC can be added as a follow-up.

---

## Proposed Changes

### Backend — Django Project

#### [NEW] [manage.py](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/backend/manage.py)
Standard Django management script.

#### [NEW] [config/settings.py](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/backend/config/settings.py)
Django settings with DRF, Channels (in-memory layer), CORS, SQLite, and auth config.

#### [NEW] [config/urls.py](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/backend/config/urls.py)
Root URL conf including `/api/` routes.

#### [NEW] [config/asgi.py](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/backend/config/asgi.py)
ASGI application with HTTP + WebSocket routing for Django Channels.

#### [NEW] [api/models.py](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/backend/api/models.py)
Models: [StudyRoom](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/frontend/components/study-room-section.tsx#21-118) (name, subject, created_by, capacity, is_active), `ChatMessage` (room, user, content, is_ai, timestamp), `RoomMember` (room, user, role, joined_at).

#### [NEW] [api/serializers.py](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/backend/api/serializers.py)
DRF serializers for User registration/login, StudyRoom CRUD, ChatMessage list.

#### [NEW] [api/views.py](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/backend/api/views.py)
API views:
- `POST /api/auth/register/` — create user
- `POST /api/auth/login/` — token-based login (session auth)
- `POST /api/auth/logout/` — logout
- `GET /api/auth/me/` — current user
- `GET/POST /api/rooms/` — list/create rooms
- `GET /api/rooms/:id/` — room detail
- `GET /api/rooms/:id/messages/` — chat history
- `POST /api/rooms/:id/ai-ask/` — AI teacher endpoint (mock)
- `GET /api/admin/stats/` — admin stats

#### [NEW] [api/urls.py](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/backend/api/urls.py)
URL patterns for all API endpoints.

#### [NEW] [api/consumers.py](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/backend/api/consumers.py)
WebSocket consumer for room chat — handles connect/disconnect/receive/broadcast.

#### [NEW] [api/routing.py](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/backend/api/routing.py)
WebSocket URL routing: `ws/room/<room_id>/`.

---

### Frontend — Login Page

#### [MODIFY] [page.tsx](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/frontend/app/login/page.tsx)
Full login/signup page with tabbed form (Login / Register), form validation, API integration, and redirect on success.

---

### Frontend — Study Room

#### [MODIFY] [page.tsx](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/frontend/app/room/[id]/page.tsx)
Complete study room page with:
- Video grid (local camera via `getUserMedia`, participant placeholders)
- Real-time chat panel via WebSocket
- AI teacher "Ask AI" button that calls `/api/rooms/:id/ai-ask/`
- Media controls (mic, video, screen share, end call)
- Participant list sidebar

---

### Frontend — Admin Dashboard

#### [MODIFY] [page.tsx](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/frontend/app/admin/page.tsx)
Admin dashboard with:
- Stats overview (total rooms, active users, sessions, messages)
- Room management table (create/delete rooms)
- Recent activity feed

---

### Frontend — Shared

#### [MODIFY] [api.ts](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/frontend/lib/api.ts)
Add API helper functions for auth, rooms, messages, and AI endpoints. Add auth token handling.

#### [MODIFY] [layout.tsx](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/frontend/app/layout.tsx)
Wrap with [ThemeProvider](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/frontend/components/theme-provider.tsx#9-12) for dark mode support.

#### [MODIFY] [navbar.tsx](file:///c:/Users/Mallesh/Projects/Virtual_Study_Group/frontend/components/navbar.tsx)
Wire Login/Signup buttons to `/login`. Show logged-in user state.

---

## Verification Plan

### Automated Tests
1. **Backend API test**: Run `python manage.py test` from `backend/` directory (will add basic tests in `api/tests.py`)
2. **Backend server check**: Start server with `python manage.py runserver` and verify no errors

### Browser Verification
1. Open `http://localhost:3000` — verify landing page loads correctly
2. Navigate to `/login` — verify login/signup form renders, test signup + login flow
3. After login, navigate to `/admin` — verify stats and room list load
4. Create a room from admin, then navigate to `/room/<id>` — verify video grid, chat panel, and AI ask feature
5. Open a second browser tab to the same room to verify real-time WebSocket chat

### Manual Verification
- User should confirm the login → create room → join room → chat → ask AI flow works end-to-end
