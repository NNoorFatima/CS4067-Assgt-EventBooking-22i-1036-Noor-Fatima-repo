document.addEventListener("DOMContentLoaded", function () {
    const bookingId = localStorage.getItem("bookingId");

    //fetch("http://localhost:5001/payments", {
    //fetch("/api/booking/payments", {
    fetch("/api/booking/payments", {  // Use NGINX routing path for payment service

        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ booking_id: bookingId })
    })
    .then(response => response.json())
    .then(data => {
        console.log("✅ Payment response:", data);

        document.getElementById("payment-status").innerText = data.message;
    })
    .catch(error => console.error("Error processing payment:", error));
});
