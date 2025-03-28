# ---------- STAGE 1: Build ----------
    FROM maven:3.9.6-eclipse-temurin-17-alpine AS build
    WORKDIR /app
    COPY pom.xml .
    COPY src ./src
    RUN mvn clean package -DskipTests
    
    # ---------- STAGE 2: Run ----------
    FROM openjdk:17-jdk-alpine
    WORKDIR /app
    COPY --from=build /app/target/event-service-0.0.1-SNAPSHOT.jar app.jar
    EXPOSE 8080
    CMD ["java", "-jar", "app.jar"]
    