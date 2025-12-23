// Login
async function login(form, redirectUrl) {
    const formData = new FormData(form);
    const data = {
        email: formData.get('email'),
        username: formData.get('username'),
        password: formData.get('password')
    };
    const res = await fetch('/api/auth/login', {
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
}

// Signup
async function signup(form, redirectUrl) {
    const formData = new FormData(form);
    const data = {
        email: formData.get('email'),
        username: formData.get('username'),
        password: formData.get('password')
    };
    const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    const result = await res.json();
    if(res.ok){
        alert('Signup successful!');
        window.location.href = redirectUrl;
    } else {
        alert(result.detail || 'Signup failed');
    }
}

// Forgot Password
let userEmail = '';
async function requestCode() {
    userEmail = document.getElementById('email').value;
    if(!userEmail) return alert('Enter email');
    const res = await fetch('/api/forget-password/request', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: userEmail })
    });
    const result = await res.json();
    if(res.ok) {
        alert('Code sent to your email');
        document.getElementById('step1').style.display = 'none';
        document.getElementById('step2').style.display = 'block';
    } else {
        alert(result.detail || 'Failed to send code');
    }
}

async function verifyCode() {
    const code = document.getElementById('code').value;
    const res = await fetch('/api/forget-password/verify', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: userEmail, code })
    });
    const result = await res.json();
    if(res.ok) {
        alert('Code verified');
        document.getElementById('step2').style.display = 'none';
        document.getElementById('step3').style.display = 'block';
    } else {
        alert(result.detail || 'Invalid code');
    }
}

async function resetPassword() {
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;
    if(password !== confirm_password) return alert('Passwords do not match');
    const res = await fetch('/api/forget-password/reset/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: userEmail, code: document.getElementById('code').value, password, confirm_password })
    });
    const result = await res.json();
    if(res.ok) {
        alert('Password reset successfully');
        window.location.href = '/';
    } else {
        alert(result.detail || 'Failed to reset password');
    }
}
