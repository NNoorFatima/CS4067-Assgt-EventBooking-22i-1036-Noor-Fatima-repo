FROM nginx:alpine
#inside the container
WORKDIR  /usr/share/nginx/html 
#remove default nginx static files
RUN rm -rf ./*

COPY . .

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
