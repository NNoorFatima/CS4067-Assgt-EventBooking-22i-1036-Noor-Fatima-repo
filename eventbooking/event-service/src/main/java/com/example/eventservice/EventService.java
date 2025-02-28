package com.example.eventservice.service;

import com.example.eventservice.model.Event;
import com.example.eventservice.repository.EventRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;
@Service
public class EventService {
    @Autowired
    private EventRepository eventRepository;

    public List<Event> getAllEvents() {
        return eventRepository.findAll();
    }

    public Optional<Event> getEventById(String id) {
        return eventRepository.findById(id);
    }

    public Event createEvent(Event event) {
        if (event.getName() == null || event.getDateTime() == null) {
            throw new RuntimeException("Missing required fields");
        }
        return eventRepository.save(event);
    }
    public Event updateEvent(String id, Event updatedEvent) {
        return eventRepository.findById(id)
                .map(event -> {
                    event.setName(updatedEvent.getName());
                    event.setDescription(updatedEvent.getDescription());
                    event.setDateTime(updatedEvent.getDateTime());
                    event.setLocation(updatedEvent.getLocation());
                    event.setCapacity(updatedEvent.getCapacity());
                    return eventRepository.save(event);
                })
                .orElseThrow(() -> new RuntimeException("Event not found with id: " + id));
    }

    public void deleteEvent(String id) {
        eventRepository.deleteById(id);
    }

}
