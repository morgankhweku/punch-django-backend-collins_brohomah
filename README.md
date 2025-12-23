# Punch MiniChat – Realtime Chat Application

Punch MiniChat is a real-time chat application built with **Django**, **Django Rest Framework**, **JWT authentication**, and **Django Channels (WebSockets)**.  
It supports **one-to-one chat**, **group chat**, **password reset via email**, and a **minimal frontend** for testing functionality.

This project was built as an **engineering interview test** with emphasis on:
- Clean architecture
- Authentication
- Realtime communication
- Readable and maintainable code

---

##  Features

###  Authentication
- User registration
- Login with **email + username + password**
- JWT authentication (Access & Refresh tokens)
- Check session
- Logout
- Forgot password (email verification code + reset)

###  Chat
- One-to-one chat
- Realtime messaging using WebSockets
- Messages stored in database
- Message metadata (sender, timestamp)

###  Group Chat
- Create group chat
- Add multiple users
- Realtime group messaging
- Group message persistence

###  Frontend
- Minimal HTML/CSS/JS
- Login, signup, forgot password flow
- Dashboard
- Chat list & chat room
- Group chat list & group room

---

##  Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | Django 5.x |
| API | Django Rest Framework |
| Auth | SimpleJWT |
| Realtime | Django Channels |
| WebSocket Server | Daphne |
| Frontend | HTML, CSS, Vanilla JS |
| Database | SQLite (can be replaced later) |

---

## Project Structure


punch_minichat/
│
├── auth/                 # Authentication & JWT
├── chat/                 # One-to-one chat
├── groupchat/            # Group chat
├── forgot_password/      # Password reset flow
├── frontend/             # HTML/CSS/JS frontend
│
├── punch_minichat/
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
│
├── manage.py
├── README.md
└── requirements.txt
