package com.example.eventservice.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;
import com.mongodb.client.MongoClient;

@RestController
@RequestMapping("/api/test")
public class TestController {

    private final MongoClient mongoClient;
    public TestController(MongoClient mongoClient) {
        this.mongoClient = mongoClient;
    }
    @GetMapping("/mongo-status")
    public String checkMongoConnection() {
        try {
            mongoClient.listDatabaseNames(); // Query MongoDB to check the connection
            return "✅ Connected to MongoDB Atlas!";
        } catch (Exception e) {
            return "❌ MongoDB Connection Failed: " + e.getMessage();
        }
    }
}
