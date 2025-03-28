FROM openjdk:17-jdk-slim

WORKDIR /app

COPY pom.xml .
COPY src ./src

# Install Maven and build the JAR inside the container
RUN apt-get update && apt-get install -y maven && mvn clean package -DskipTests

# Copy the built JAR file from inside the container
COPY target/event-service-0.0.1-SNAPSHOT.jar app.jar

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
