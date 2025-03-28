package com.EventBookingService.eventservice;
import com.example.eventservice.EventServiceApplication; // Import the main class

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest(classes = EventServiceApplication.class) // ✅ Add this line
class EventServiceApplicationTests {

	@Test
	void contextLoads() {
	}

}
