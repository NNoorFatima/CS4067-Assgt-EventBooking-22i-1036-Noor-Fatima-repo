FROM openjdk:17-jdk-slim

WORKDIR /app

#Copy Maven build file (to leverage Docker caching)
COPY pom.xml .

COPY src ./src

RUN apt-get update && apt-get install -y maven && mvn clean package -DskipTests

# Copy the built JAR file
COPY target/event-service-0.0.1-SNAPSHOT.jar app.jar

#Expose the port (Spring Boot runs on 8080)
EXPOSE 8080

#  Command to run the application inside the container
CMD ["java", "-jar", "app.jar"]
