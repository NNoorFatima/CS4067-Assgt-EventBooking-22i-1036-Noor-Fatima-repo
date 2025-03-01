package com.example.eventservice.controller;

import com.example.eventservice.service.EventService;
import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import java.time.LocalDateTime;
import com.example.eventservice.model.Event;
import com.example.eventservice.repository.EventRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.http.ResponseEntity;
import java.util.Map;
import java.util.Collections;  


import java.util.HashMap;
import org.springframework.http.HttpStatus;



@CrossOrigin(origins = "*") // Adjust port if needed
@RestController
@RequestMapping("/api/events")
public class EventController {

    private final EventRepository eventRepository;

    @Autowired
    private EventService eventService;
    @Autowired
    public EventController(EventRepository eventRepository, EventService eventService) {
        this.eventRepository = eventRepository;
        this.eventService = eventService;
    }

    // Get all events
    @GetMapping
    public List<Event> getAllEvents() {
        return eventService.getAllEvents();
    }

    // Get a single event by ID
    @GetMapping("/{id}")
    public ResponseEntity<Event> getEventById(@PathVariable String id) {
        Optional<Event> event = eventService.getEventById(id);
        return event.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    // Create a new event
    @PostMapping
    public ResponseEntity<Event> createEvent(@RequestBody Event event) {
        return ResponseEntity.ok(eventService.createEvent(event));
    }

    // Update an existing event
    @PutMapping("/{id}")
    public ResponseEntity<Event> updateEvent(@PathVariable String id, @RequestBody Event updatedEvent) {
        try {
            return ResponseEntity.ok(eventService.updateEvent(id, updatedEvent));
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }

    // Delete an event
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteEvent(@PathVariable String id) {
        eventService.deleteEvent(id);
        return ResponseEntity.noContent().build();
    }

    //Decrease Event Capacity
    @PutMapping("/{eventId}/decrease_capacity")
    public ResponseEntity<Map<String, String>> decreaseCapacity(@PathVariable String eventId) {
        Optional<Event> eventOptional = eventRepository.findById(eventId);

        if (!eventOptional.isPresent()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(Collections.singletonMap("error", "Event not found"));
        }

        Event event = eventOptional.get();
        if (event.getCapacity() <= 0) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(Collections.singletonMap("error", "Event is fully booked"));
        }

        // ✅ Reduce capacity
        event.setCapacity(event.getCapacity() - 1);
        eventRepository.save(event);

        return ResponseEntity.ok(Collections.singletonMap("message", "Event capacity updated"));
    }



}
