document.addEventListener('DOMContentLoaded', () => {
    console.log("AUTH JS LOADED");

    // ------------------ Login ------------------
    async function login(form, redirectUrl) {
        const formData = new FormData(form);
        const data = {
            email: formData.get('email'),
            username: formData.get('username'),
            password: formData.get('password')
        };
        try {
            const res = await fetch(`${window.location.origin}/api/auth/login`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            if(res.ok){
                localStorage.setItem('access_token', result.access);
                window.location.href = redirectUrl;
            } else {
                alert(result.detail || 'Login failed');
            }
        } catch(err) {
            console.error(err);
            alert('Network error');
        }
    }

    // ------------------ Signup ------------------
    async function signup(form, redirectUrl) {
        const formData = new FormData(form);
        const data = {
            email: formData.get('email'),
            username: formData.get('username'),
            password: formData.get('password')
        };
        try {
            const res = await fetch(`${window.location.origin}/api/auth/register`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            if(res.ok){
                alert('User account created successfully');
                window.location.href = redirectUrl;
            } else {
                alert(result.detail || 'Signup failed');
            }
        } catch(err) {
            console.error(err);
            alert('Network error');
        }
    }

    // ------------------ Forgot Password ------------------
    let userEmail = '';

    async function requestCode() {
        const emailEl = document.getElementById('email');
        if(!emailEl) return;
        userEmail = emailEl.value.trim();
        if(!userEmail) return alert('Enter your email');

        try {
            const res = await fetch(`${window.location.origin}/api/forget-password/request`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ email: userEmail })
            });
            const result = await res.json();
            if(res.ok) {
                localStorage.setItem('reset_email', userEmail);
                document.getElementById('code-display').textContent = result.code;
                document.getElementById('code-popup').style.display = 'block';
            } else {
                alert(result.detail || 'Failed to send code');
            }
        } catch(err) {
            console.error(err);
            alert('Network error');
        }
    }

    function handleOk() {
        document.getElementById('code-popup').style.display = 'none';
        window.location.href = `${window.location.origin}/verify-code`;
    }

    // Attach event listeners
    const requestBtn = document.getElementById('request-code-btn');
    if (requestBtn) requestBtn.addEventListener('click', requestCode);

    const okBtn = document.getElementById('ok-btn');
    if (okBtn) okBtn.addEventListener('click', handleOk);

    // Expose functions globally if needed in templates
    window.login = login;
    window.signup = signup;
    window.requestCode = requestCode;
    window.handleOk = handleOk;
});
