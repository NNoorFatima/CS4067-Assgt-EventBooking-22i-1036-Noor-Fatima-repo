# Use official NGINX image
FROM nginx:alpine

# Delete default nginx config to avoid conflicts
# Remove default html and config
RUN rm -rf /usr/share/nginx/html/* \
    && rm /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf


# Copy static frontend files
COPY ./booking-frontend /usr/share/nginx/html/booking
COPY ./event-frontend /usr/share/nginx/html/event
COPY ./notification-frontend /usr/share/nginx/html/notification
COPY user-frontend /usr/share/nginx/html/user

# Expose port 80
EXPOSE 80

# Run NGINX
CMD ["nginx", "-g", "daemon off;"]
