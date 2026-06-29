document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("contactForm");
    const submitBtn = document.getElementById("fsub");

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        const data = {
            name: document.getElementById("name").value.trim(),
            company: document.getElementById("company").value.trim(),
            email: document.getElementById("email").value.trim(),
            phone: document.getElementById("phone").value.trim(),
            service: document.getElementById("service").value,
            message: document.getElementById("message").value.trim()
        };

        // Required field validation
        if (
            !data.name ||
            !data.company ||
            !data.email ||
            !data.phone ||
            !data.service ||
            !data.message
        ) {
            alert("Please fill all fields.");
            return;
        }

        // Email validation
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(data.email)) {
            alert("Please enter a valid email address.");
            return;
        }

        // Phone validation (10 digits)
        const phonePattern = /^[0-9]{10}$/;

        if (!phonePattern.test(data.phone)) {
            alert("Please enter a valid 10-digit phone number.");
            return;
        }

        try {

            // Disable button while sending
            submitBtn.disabled = true;
            submitBtn.textContent = "Sending...";
            submitBtn.style.opacity = "0.7";

            const response = await fetch(
                "/contact",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                }
            );

            const result = await response.json();

            if (response.ok) {

                submitBtn.textContent = "✓ Message Sent Successfully";
                submitBtn.style.background =
                    "linear-gradient(135deg,#0F6A2A,#0D5C24)";
                submitBtn.style.opacity = "1";

                form.reset();

                setTimeout(() => {
                    submitBtn.textContent = "Send Message →";
                    submitBtn.style.background = "";
                }, 5000);

            } else {

                alert(
                    result.error ||
                    "Something went wrong."
                );
            }

        } catch (error) {

            console.error("Error:", error);

            alert(
                "Unable to connect to backend server."
            );

        } finally {

            submitBtn.disabled = false;

            if (
                submitBtn.textContent !==
                "✓ Message Sent Successfully"
            ) {
                submitBtn.textContent = "Send Message →";
                submitBtn.style.opacity = "1";
            }
        }
    });
});