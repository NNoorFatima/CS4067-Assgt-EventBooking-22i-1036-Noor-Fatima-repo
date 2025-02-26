package com.example.eventservice.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;


@Data
@NoArgsConstructor // Required for MongoDB deserialization
@Document(collection = "events")
public class Event {
    @Id
    private String id;
    private String name;
    private String description;
    private LocalDateTime dateTime;
    private String location;
    private int capacity;
    private double price;

    //constructor 
    public Event(String nm, String des, LocalDateTime dt, String loc,int cap,double p)
    {
        this.capacity=cap;
        this.dateTime=dt;
        this.description=des;
        this.location=loc;
        this.name=nm;
        this.price= p;
    }
   
}
