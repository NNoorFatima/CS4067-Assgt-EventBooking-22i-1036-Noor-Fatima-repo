document.addEventListener("DOMContentLoaded", function () {
    const bookingId = localStorage.getItem("bookingId");

    fetch("http://localhost:5001/payments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ booking_id: bookingId })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("payment-status").innerText = data.message;
    })
    .catch(error => console.error("Error processing payment:", error));
});
