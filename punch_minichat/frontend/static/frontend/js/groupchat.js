const groupToken = localStorage.getItem('access_token');
const groupId = window.location.pathname.split('/')[2];
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
    const li = document.createElement('li');
    li.textContent = `${sender}: ${content} (${getRelativeTime(timestamp)})`;
    list.appendChild(li);
}

/* ---------- Load Messages ---------- */
async function loadGroupMessages() {
    const res = await fetch(`/api/groupchat/${groupId}/message`, {
        headers: {
            'Authorization': 'Bearer ' + groupToken
        }
    });

    const messages = await res.json();
    const list = document.getElementById('messages');
    list.innerHTML = '';

    messages.forEach(msg => {
        addMessageToList(msg.sender, msg.content, msg.timestamp);
    });
}

/* ---------- WebSocket ---------- */
function connectGroupSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/groupchat/${groupId}/`;

    groupSocket = new WebSocket(wsUrl);

    groupSocket.onopen = () => {
        console.log('Group WebSocket connected');
    };

    groupSocket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        addMessageToList(data.user, data.message, data.timestamp);
    };

    groupSocket.onclose = () => {
        console.log('Group WebSocket closed');
    };

    groupSocket.onerror = (e) => {
        console.error('Group WebSocket error', e);
    };
}

/* ---------- Send Message ---------- */
document.getElementById('message-form').addEventListener('submit', e => {
    e.preventDefault();
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    if (!message) return;

    if (groupSocket && groupSocket.readyState === WebSocket.OPEN) {
        groupSocket.send(JSON.stringify({ message }));
        input.value = '';
    }
});

/* ---------- Init ---------- */
loadGroupMessages();
connectGroupSocket();
