const chatToken = localStorage.getItem('access_token');
const chatId = window.location.pathname.split('/')[2];
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

function addMessageToList(sender, text, timestamp) {
    const list = document.getElementById('messages');
    const li = document.createElement('li');
    const relativeTime = getRelativeTime(timestamp);
    li.textContent = `${sender}: ${text} (${relativeTime})`;
    list.appendChild(li);
}

async function loadMessages() {
    const res = await fetch(`/api/chat/${chatId}/message`, {
        headers: { 'Authorization': 'Bearer ' + chatToken }
    });
    const messages = await res.json();
    const list = document.getElementById('messages');
    list.innerHTML = '';
    messages.forEach(msg => {
        addMessageToList(msg.sender, msg.text, msg.timestamp);
    });
}

function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/chat/${chatId}/`;
    chatSocket = new WebSocket(wsUrl);

    chatSocket.onopen = function(e) {
        console.log('WebSocket connected');
    };

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const list = document.getElementById('messages');
        const li = document.createElement('li');
        li.textContent = `${data.sender}: ${data.message} (${data.timestamp})`;
        list.appendChild(li);
    };

    chatSocket.onclose = function(e) {
        console.log('WebSocket closed');
        // Optionally reconnect
    };

    chatSocket.onerror = function(e) {
        console.error('WebSocket error', e);
    };
}

document.getElementById('message-form').addEventListener('submit', async e => {
    e.preventDefault();
    const input = document.getElementById('message-input');
    const messageText = input.value.trim();
    if (!messageText) return;

    // Get current user (assuming stored in localStorage or from token)
    const currentUser = JSON.parse(atob(chatToken.split('.')[1])).username;

    if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
        chatSocket.send(JSON.stringify({ message: messageText }));
        // Add message immediately
        addMessageToList(currentUser, messageText, new Date().toISOString());
        input.value = '';
    } else {
        // Fallback to API if WebSocket not available
        const res = await fetch(`/api/chat/${chatId}/send`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + chatToken
            },
            body: JSON.stringify({ message: messageText })
        });
        if(res.ok){
            input.value = '';
            loadMessages();
        } else {
            const err = await res.json();
            alert(err.detail || 'Failed to send message');
        }
    }
});

loadMessages();
connectWebSocket();
