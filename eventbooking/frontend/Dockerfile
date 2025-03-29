# Use official NGINX image as base image
FROM nginx:alpine

# Copy the NGINX configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Copy each frontend module to appropriate directory
COPY ./booking-frontend /usr/share/nginx/html/booking-frontend
COPY ./event-frontend /usr/share/nginx/html/event-frontend
COPY ./notification-frontend /usr/share/nginx/html/notification-frontend
COPY ./user-frontend /usr/share/nginx/html/user-frontend

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start NGINX when the container runs
CMD ["nginx", "-g", "daemon off;"]
