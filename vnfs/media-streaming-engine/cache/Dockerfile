FROM nginx:stable-alpine

EXPOSE 80

RUN apk update && apk add --no-cache \
    python3 \
    python3-dev

COPY ./requirements.txt /app/requirements.txt

RUN mkdir -p /opt/data

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR app/

COPY . app/

RUN mkdir /opt/data/hls && chmod 755 /opt/data/hls

# Add NGINX config.
ADD nginx.conf /etc/nginx/nginx.conf

ENTRYPOINT [ "/app/entrypoint.sh" ]
#CMD ["nginx", "-g", "daemon off;"]
