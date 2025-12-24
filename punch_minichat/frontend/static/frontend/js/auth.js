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
                alert('Code sent to your email');
                document.getElementById('step1').style.display = 'none';
                document.getElementById('step2').style.display = 'block';
            } else {
                alert(result.detail || 'Failed to send code');
            }
        } catch(err) {
            console.error(err);
            alert('Network error');
        }
    }

    async function verifyCode() {
        const codeEl = document.getElementById('code');
        if(!codeEl) return;
        const code = codeEl.value.trim();
        if(!code) return alert('Enter the code');

        try {
            const res = await fetch(`${window.location.origin}/api/forget-password/verify`, {
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
        } catch(err) {
            console.error(err);
            alert('Network error');
        }
    }

    async function resetPassword() {
        const passwordEl = document.getElementById('password');
        const confirmEl = document.getElementById('confirm_password');
        const codeEl = document.getElementById('code');
        if(!passwordEl || !confirmEl || !codeEl) return;

        const password = passwordEl.value.trim();
        const confirm_password = confirmEl.value.trim();
        const code = codeEl.value.trim();

        if(!password || !confirm_password) return alert('Fill all fields');
        if(password !== confirm_password) return alert('Passwords do not match');

        try {
            const res = await fetch(`${window.location.origin}/api/forget-password/reset/`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ email: userEmail, code, password, confirm_password })
            });
            const result = await res.json();
            if(res.ok) {
                alert('Password reset successfully');
                window.location.href = `${window.location.origin}/login`;
            } else {
                alert(result.detail || 'Failed to reset password');
            }
        } catch(err) {
            console.error(err);
            alert('Network error');
        }
    }

    // Attach event listeners
    const requestBtn = document.getElementById('request-code-btn');
    if (requestBtn) requestBtn.addEventListener('click', requestCode);

    const verifyBtn = document.getElementById('verify-code-btn');
    if (verifyBtn) verifyBtn.addEventListener('click', verifyCode);

    const resetBtn = document.getElementById('reset-password-btn');
    if (resetBtn) resetBtn.addEventListener('click', resetPassword);

    // Expose functions globally if needed in templates
    window.login = login;
    window.signup = signup;
    window.requestCode = requestCode;
    window.verifyCode = verifyCode;
    window.resetPassword = resetPassword;
});
