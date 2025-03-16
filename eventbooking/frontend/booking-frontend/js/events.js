const EVENT_SERVICE_URL = "http://localhost:8080/api/events"; // URL for Event Service


document.addEventListener("DOMContentLoaded", function () {
    const eventList = document.getElementById("event-list");
   // let events = JSON.parse(localStorage.getItem("eventsData"));  // Get stored events
    let events; //bhai fetch regardless 
    if (!events || events.length === 0) {
        console.warn("No events found in localStorage. Fetching from Event Service...");
        fetch(EVENT_SERVICE_URL)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Fetched events:", data);
                localStorage.setItem("eventsData", JSON.stringify(data));
                displayEvents(data);
            })
            .catch(error => console.error("Error fetching events:", error));
    } else {
        displayEvents(events); // If events are in localStorage, display them
    }

});

// Function to display events
function displayEvents(events) {
    const eventList = document.getElementById("event-list");
    eventList.innerHTML = ""; // Clear previous data

    if (events.length === 0) {
        eventList.innerHTML = "<tr><td colspan='7'>No events available.</td></tr>";
        return;
    }

    events.forEach(event => {
        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${event.name}</td>
            <td>${event.description}</td>
            <td>${event.dateTime}</td>
            <td>${event.location}</td>
            <td>${event.capacity}</td>
            <td>${event.price}</td>
            <td><button onclick="bookEvent('${event.id}')">Book</button></td>
        `;
        eventList.appendChild(row);
    });
}




// Function to handle booking
function bookEvent(eventId) {
    localStorage.setItem("selectedEventId", eventId); //  Store selected event ID
    window.location.href = "payment.html"; //  Redirect to payment page
}