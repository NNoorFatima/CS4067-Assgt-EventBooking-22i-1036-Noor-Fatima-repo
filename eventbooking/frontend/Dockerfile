# Use the official Nginx image
FROM nginx:alpine

# Set the working directory inside the container
WORKDIR /usr/share/nginx/html

# Remove the default Nginx static files
RUN rm -rf ./*

# Copy the contents of the frontend directories into the Nginx HTML folder
COPY ./user-frontend/ /usr/share/nginx/html/user-frontend/
COPY ./notification-frontend/ /usr/share/nginx/html/notification-frontend/
COPY ./event-frontend/ /usr/share/nginx/html/event-frontend/
COPY ./booking-frontend/ /usr/share/nginx/html/booking-frontend/

# Copy the custom Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf


# Expose port 80 (default HTTP port)
EXPOSE 80

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
