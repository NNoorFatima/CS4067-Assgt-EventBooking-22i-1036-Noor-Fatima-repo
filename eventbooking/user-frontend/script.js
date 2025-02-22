const API_BASE_URL = "http://127.0.0.1:8000";  // FastAPI Backend URL

//Register User
document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", async function (event) {
            event.preventDefault();
            const username = document.getElementById("username").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            
            try {
            const response = await fetch(`${API_BASE_URL}/users/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email, password })
            });



            const result = await response.json();
            if (response.ok) {
                alert("Registration successful! Redirecting to login...");
                window.location.href = "login.html"; // Redirects to login page
            } else {
                document.getElementById("registerMessage").innerText = result.detail || "Registration failed!";
            }
            document.getElementById("registerMessage").innerText = result.message;
        } catch(error) {
            nsole.error("Registration failed:", error);
            alert("Error registering. Check console for details.");
        }
        });
    }
});

// Login User
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();
            const username = document.getElementById("loginUsername").value;
            const password = document.getElementById("loginPassword").value;

            const response = await fetch(`${API_BASE_URL}/users/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            const result = await response.json();
            if (response.ok) {
                localStorage.setItem("token", result.access_token);
                alert("Login successful! Redirecting to dashboard...");
                window.location.href = "dashboard.html";
            } else {
                document.getElementById("loginMessage").innerText = "Invalid credentials!";
            }
        });
    }
});

// Fetch User Info (Dashboard)
document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname.includes("dashboard.html")) {
        const token = localStorage.getItem("token");
        if (!token) {
            window.location.href = "login.html";
        } else {
            fetch(`${API_BASE_URL}/users/me`, {
                method: "GET",
                headers: { "Authorization": `Bearer ${token}` }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("userInfo").innerText = `Welcome, ${data.username}!`;
            })
            .catch(() => {
                alert("Unauthorized access!");
                window.location.href = "login.html";
            });
        }
    }
});

//logout Function
function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}
