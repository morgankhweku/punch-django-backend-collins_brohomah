console.log("Chat JS LOADED");

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        alert('You are not logged in!');
        return;
    }

    const chatListEl = document.getElementById('chat-list');
    const messagesEl = document.getElementById('messages');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const createChatBtn = document.getElementById('create-chat-btn');

    const pathParts = window.location.pathname.split('/');
    const chatId = pathParts.includes('chat') ? pathParts[2] : null;
    let chatSocket = null;

    function getRelativeTime(timestamp) {
        const now = new Date();
        const messageTime = new Date(timestamp);
        const diffInSeconds = Math.floor((now - messageTime) / 1000);
        if (diffInSeconds < 60) return `${diffInSeconds} seconds ago`;
        const diffInMinutes = Math.floor(diffInSeconds / 60);
        if (diffInMinutes < 60) return `${diffInMinutes} mins ago`;
        const diffInHours = Math.floor(diffInMinutes / 60);
        if (diffInHours < 24) return `${diffInHours} hours ago`;
        const diffInDays = Math.floor(diffInHours / 24);
        if (diffInDays < 30) return `${diffInDays} days ago`;
        const diffInMonths = Math.floor(diffInDays / 30);
        if (diffInMonths < 12) return `${diffInMonths} months ago`;
        const diffInYears = Math.floor(diffInMonths / 12);
        return `${diffInYears} years ago`;
    }

    function addMessage(sender, text, timestamp) {
        if (!messagesEl) return;
        const li = document.createElement('li');
        li.textContent = `${sender}: ${text} (${getRelativeTime(timestamp)})`;
        messagesEl.appendChild(li);
    }

    async function loadChats() {
        if (!chatListEl) return;
        const res = await fetch(`${window.location.origin}/api/chat/list`, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        const chats = await res.json();
        chatListEl.innerHTML = '';
        if (chats.length === 0) {
            chatListEl.innerHTML = '<li>No chats yet</li>';
        } else {
            chats.forEach(chat => {
                const li = document.createElement('li');
                li.textContent = chat.display_name;
                li.onclick = () => window.location.href = `${window.location.origin}/chat/${chat.id}/`;
                chatListEl.appendChild(li);
            });
        }
    }

    async function createChat() {
        if (!createChatBtn) return;
        const username = prompt('Enter username to chat with:');
        if (!username) return;
        const res = await fetch(`${window.location.origin}/api/chat/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ username })
        });
        if (res.ok) {
            alert('Chat created!');
            loadChats();
        } else {
            const err = await res.json();
            alert(err.detail || 'Failed to create chat');
        }
    }

    async function loadMessages() {
        if (!chatId || !messagesEl) return;
        const res = await fetch(`${window.location.origin}/api/chat/${chatId}/message`, {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        if (!res.ok) return;
        const messages = await res.json();
        messagesEl.innerHTML = '';
        messages.forEach(msg => addMessage(msg.sender, msg.text, msg.timestamp));
    }

    function connectWebSocket() {
        if (!chatId || !messagesEl) return;
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/chat/${chatId}/?token=${token}`;
        chatSocket = new WebSocket(wsUrl);

        chatSocket.onopen = () => console.log('WebSocket connected');
        chatSocket.onmessage = e => {
            const data = JSON.parse(e.data);
            addMessage(data.sender, data.message, data.timestamp);
        };
        chatSocket.onclose = () => console.log('WebSocket closed');
        chatSocket.onerror = e => console.error('WebSocket error', e);
    }

    if (chatListEl) {
        loadChats();
        if (createChatBtn) createChatBtn.addEventListener('click', createChat);
    }

    if (messagesEl) {
        loadMessages();
        connectWebSocket();
        if (messageForm) {
            messageForm.addEventListener('submit', async e => {
                e.preventDefault();
                const messageText = messageInput.value.trim();
                if (!messageText) return;
                let currentUser = 'You';
                try { currentUser = JSON.parse(atob(token.split('.')[1])).username; } catch {}
                if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
                    chatSocket.send(JSON.stringify({ message: messageText }));
                    addMessage(currentUser, messageText, new Date().toISOString());
                    messageInput.value = '';
                } else {
                    const res = await fetch(`${window.location.origin}/api/chat/${chatId}/send`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + token
                        },
                        body: JSON.stringify({ message: messageText })
                    });
                    if(res.ok){
                        messageInput.value = '';
                        loadMessages();
                    } else {
                        const err = await res.json();
                        alert(err.detail || 'Failed to send message');
                    }
                }
            });
        }
    }
});
