document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("signupForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission

        let phoneInput = document.getElementById("phoneNumber").value.trim().replace(/\D/g, ""); // Remove non-numeric characters

        if (phoneInput.length === 10) {
            phoneInput = "+1" + phoneInput;
        } else {
            alert("Please enter a valid 10-digit phone number.");
            return;
        }

        // ✅ Store success flag in localStorage BEFORE redirecting
        localStorage.setItem("signupSuccess", "true");

        // ✅ Redirect to index.html (No waiting for fetch to complete)
        window.location.href = "thankyou.html";

        // ✅ Send data to the server (runs in background, no error checks)
        fetch("https://textmarley-one-21309214523.us-central1.run.app/create_conversation", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ phone: phoneInput }).toString(),
        });
    });
});