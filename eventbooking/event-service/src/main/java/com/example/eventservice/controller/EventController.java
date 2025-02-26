package com.example.eventservice.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import java.time.LocalDateTime;
import com.example.eventservice.model.Event;
import com.example.eventservice.repository.EventRepository;

@RestController
@RequestMapping("/api/events")
public class EventController {

    @Autowired
    private EventRepository eventRepository;

    @PostMapping("/add-test")
    public String addTestEvent() {
        Event event = new Event();
        event.setTitle("Tech Conference 2025");
        event.setDescription("A conference about AI and ML");
        event.setDateTime(LocalDateTime.now().plusDays(10));
        event.setLocation("Dubai");
        event.setAvailableTickets(100);
        event.setPrice(49.99);

        eventRepository.save(event);
        return "✅ Test event added successfully!";
    }
}
