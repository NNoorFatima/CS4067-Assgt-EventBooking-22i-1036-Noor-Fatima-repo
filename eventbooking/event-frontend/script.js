const API_URL = "http://localhost:8080/api/events";

document.addEventListener("DOMContentLoaded",() =>{ //wait for the page to load
    loadEvents(); //fetch and display events
    
    document.getElementById("eventForm").addEventListener("submit",async (e) =>{ //listen for form submission event
        e.preventDefault();//prevents page from refershing 
        
        const name= document.getElementById("eventName").value;
        const dateTime = document.getElementById("eventDate").value;//takes the data entered by user
        const description = document.getElementById("eventDescription").value;
        const location = document.getElementById("eventLocation").value;
        const capacity = document.getElementById("eventCapacity").value;
        const price = document.getElementById("eventPrice").value;

        if(!name || !dateTime || !location ){
            alert("Plese enter event details!"); //show alert for empty field
            return;
        }
        
        const eventData= { name, description, dateTime, location, capacity, price }; //creates an object and send to the backend in JSON format
        try {
            const reponse= await fetch(API_URL,{
                method :"POST", //sends a POST request to add a new event.
                headers:{"Content-Type":"application/json"},//Tells the backend that we're sending JSON data.
                body: JSON.stringify(eventData),//Tells the backend that we're sending JSON data.
            });
            if (reponse.ok){ //if req succeeds
                alert("Successfully added event :)");
                document.getElementById("eventForm").reset(); //Clear the form fields 
                loadEvents();// reload the events 
            }
            else{
                alert("Failed to add event :(");
            }
        }
        catch (error)
        {
            console.error("Error:", error);
            alert(" Error connecting to the server.");
        }
    });
});
async function loadEvents() {
    const response = await fetch(API_URL);  //This fetches (GET) all events from the backend.
    const events = await response.json();//converts reponse to javascript array
    const eventList = document.getElementById("eventList");//find the element where events will be shown 
    eventList.innerHTML = "";//clear previous data before adding new one
    
    events.forEach(event => {
        const li = document.createElement("li");
        li.innerHTML = `
             ${event.name || "No Name"} - ${event.dateTime ? new Date(event.dateTime).toLocaleString() : "Invalid Date"}
            <br> Location: ${event.location || "No Location"}
            <br> Price: $${event.price || "0.00"}
            <br> Capacity: ${event.capacity || "0"} people
            <button onclick="deleteEvent('${event.id}')">Delete</button>
        `;
        eventList.appendChild(li);
    });

}
async function deleteEvent(id) {
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });// Sends a DELETE request to remove an event.
    loadEvents();//refresh events
}

/*
GET IS USED TO FETCH DATA FROM BACKEND 
fetch(API_URL) SENDS A GET REQUEST TO THE URL 
await response.json();CONVERS REPONSE INTO JAVASCRIPT ARRAY/OBJECT
 */

/* 
POST IS USED TO SEND/ADD NEW DATA TO THE BACKEND 
method: "POST" TELLS THE BACKEND WE ARE CREATING NEW EVENT 
headers: { "Content-Type": "application/json" }ENSURES THE REQUEST SENDS A JSON DATA
body: JSON.stringify(eventData)CONVERTS JS OBJ INTO JSON FORMAT BEFORE SENDING 

*/
/*
DELETE IS USED TO REMOVE DATA FROM BACKEND 
${API_URL}/${id} part means we are calling DELETE http://localhost:8080/api/events/{id}.
the backend finds the event with the matching id and removes it 

 */