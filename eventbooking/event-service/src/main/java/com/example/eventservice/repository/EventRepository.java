package com.example.eventservice.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import com.example.eventservice.model.Event;
import java.util.List;

public interface EventRepository extends MongoRepository<Event, String> {
    List<Event> findByTitleContaining(String title);
}
    