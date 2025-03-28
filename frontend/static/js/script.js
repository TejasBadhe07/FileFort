document.addEventListener("DOMContentLoaded", function () {
    const formTitle = document.getElementById("form-title");
    const authForm = document.getElementById("auth-form");
    const nameField = document.getElementById("name-field");
    const toggleForm = document.getElementById("toggle-form");

    let isRegistering = false;

    // Toggle between Login & Register
    toggleForm.addEventListener("click", function (e) {
        e.preventDefault();
        isRegistering = !isRegistering;

        formTitle.innerText = isRegistering ? "Register" : "Login";
        nameField.classList.toggle("hidden", !isRegistering);
        authForm.querySelector("button").innerText = isRegistering ? "Register" : "Login";
        toggleForm.innerHTML = isRegistering
            ? "Already have an account? <a href='#'>Login here</a>"
            : "Don't have an account? <a href='#'>Register here</a>";
    });

    // Handle Form Submission
    authForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const endpoint = isRegistering ? "/register" : "/login";
        const requestBody = isRegistering ? { name, email, password } : { email, password };

        try {
            const response = await fetch(`http://127.0.0.1:5000${endpoint}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(requestBody),
            });

            const data = await response.json();

            if (response.ok) {
                alert(data.message);
                if (!isRegistering) {
                    localStorage.setItem("token", data.token);
                    window.location.href = "dashboard.html"; // Redirect on successful login
                }
            } else {
                alert(data.error);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Something went wrong!");
        }
    });
});
