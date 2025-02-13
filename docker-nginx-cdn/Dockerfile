FROM nginx:alpine

RUN apk add --no-cache \
    nginx-mod-http-dav-ext \
    apache2-utils

COPY ./models /usr/share/nginx/html/models
COPY nginx.conf /etc/nginx/nginx.conf
COPY .htpasswd /etc/nginx/.htpasswd

RUN chown -R nginx:nginx /usr/share/nginx/html/models

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]