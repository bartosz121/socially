FROM nginx:1.21-alpine

# for debugging
RUN apk add curl

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
