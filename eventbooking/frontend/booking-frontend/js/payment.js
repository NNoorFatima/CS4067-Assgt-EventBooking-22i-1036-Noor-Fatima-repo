document.addEventListener("DOMContentLoaded", function () {
    const eventId = localStorage.getItem("selectedEventId");
    const userId = localStorage.getItem("loggedInUserId");
    if (!userId) {
        alert("User ID is missing! Please log in again.");
        window.location.href = "login.html";
        return;
    }

    document.getElementById("confirm-booking").addEventListener("click", async () => {
        try {
            let response = await fetch("http://localhost:5001/bookings", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, event_id: eventId })
            });

            if (!response.ok) {
                let errorData = await response.json();
                console.error("Backend Error:", errorData);
                alert(`Booking failed! Server responded: ${errorData.error || "Unknown error"}`);
                return;
            }

            let data = await response.json();
            if (data.booking_id) {
                localStorage.setItem("bookingId", data.booking_id);
                alert("Booking confirmed! Redirecting...");
                setTimeout(() => {
                    window.location.href = "confirmation.html";
                }, 2000); // Add delay to ensure data is saved
            }
            

        } catch (error) {
            console.error("Error processing booking:", error);
            alert("Error processing booking. Please check your internet connection or server logs.");
        }
    });
});
