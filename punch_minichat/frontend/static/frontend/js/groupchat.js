console.log("GROUPCHAT JS LOADED");

document.addEventListener('DOMContentLoaded', () => {
    const groupToken = localStorage.getItem('access_token');
    const pathParts = window.location.pathname.split('/');
    const groupId = pathParts[2];
    if (!groupId || !groupToken) return console.error('Missing groupId or token');

    let groupSocket = null;

    /* ---------- Relative Time ---------- */
    function getRelativeTime(timestamp) {
        const now = new Date();
        const time = new Date(timestamp);
        const diff = Math.floor((now - time) / 1000);

        if (diff < 60) return `${diff}s ago`;
        if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
        if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
        if (diff < 2592000) return `${Math.floor(diff / 86400)}d ago`;
        if (diff < 31536000) return `${Math.floor(diff / 2592000)}mo ago`;
        return `${Math.floor(diff / 31536000)}y ago`;
    }

    /* ---------- UI ---------- */
    function addMessageToList(sender, content, timestamp) {
        const list = document.getElementById('messages');
        if (!list) return;
        const li = document.createElement('li');
        li.textContent = `${sender}: ${content} (${getRelativeTime(timestamp)})`;
        list.appendChild(li);
    }

    /* ---------- Load Messages ---------- */
    async function loadGroupMessages() {
        try {
            const res = await fetch(`/api/groupchat/${groupId}/message`, {
                headers: { 'Authorization': 'Bearer ' + groupToken }
            });
            const messages = await res.json();
            const list = document.getElementById('messages');
            if (!list) return;
            list.innerHTML = '';
            if (!res.ok) {
                list.innerHTML = `<li>Failed to load messages: ${res.status}</li>`;
                return;
            }
            if (messages.length === 0) {
                list.innerHTML = '<li>No messages yet</li>';
            } else {
                messages.forEach(msg => addMessageToList(msg.sender, msg.content, msg.timestamp));
            }
        } catch (err) {
            console.error('Error loading messages:', err);
            const list = document.getElementById('messages');
            if (list) list.innerHTML = '<li>Error loading messages. Refresh page.</li>';
        }
    }

    /* ---------- WebSocket ---------- */
    function connectGroupSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/groupchat/${groupId}/?token=${groupToken}`;
        groupSocket = new WebSocket(wsUrl);

        groupSocket.onopen = () => console.log('Group WebSocket connected');

        groupSocket.onmessage = e => {
            const data = JSON.parse(e.data);
            addMessageToList(data.sender, data.message, data.timestamp);
        };

        groupSocket.onclose = () => console.log('Group WebSocket closed');

        groupSocket.onerror = e => console.error('Group WebSocket error', e);
    }

    /* ---------- Send Message ---------- */
    const form = document.getElementById('message-form');
    if (form) {
        form.addEventListener('submit', async e => {
            e.preventDefault();
            const input = document.getElementById('message-input');
            if (!input) return;
            const message = input.value.trim();
            if (!message) return;

            // Optimistically add message
            addMessageToList('You', message, new Date().toISOString());
            input.value = '';

            if (groupSocket && groupSocket.readyState === WebSocket.OPEN) {
                groupSocket.send(JSON.stringify({ message }));
            } else {
                // Fallback API send if WS not connected
                try {
                    const res = await fetch(`/api/groupchat/${groupId}/send`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + groupToken
                        },
                        body: JSON.stringify({ content: message })
                    });
                    if (!res.ok) {
                        const err = await res.json();
                        alert(err.detail || 'Failed to send message');
                    }
                } catch (err) {
                    console.error(err);
                    alert('Network error. Failed to send message.');
                }
            }
        });
    }

    /* ---------- Init ---------- */
    loadGroupMessages();
    connectGroupSocket();
});
