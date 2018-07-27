FROM alpine:3.4

ENV NGINX_VERSION 1.13.9
ENV NGINX_RTMP_VERSION 1.2.1

EXPOSE 1935
EXPOSE 80

RUN mkdir -p /opt/data && mkdir /www

#Build dependencies:
#TODO: optimize this dependencies
RUN apk update && apk add \
  binutils \
  binutils-libs \
  build-base \
  ca-certificates \
  gcc \
  libc-dev \
  libgcc \
  make \
  musl-dev \
  openssl \
  openssl-dev \
  pcre \
  pcre-dev \
  pkgconf \
  pkgconfig \
  zlib-dev \
  python3 \
  python3-dev \
  inotify-tools

  

#Get the nginx source:
RUN cd /tmp && \
  wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && \
  tar zxf nginx-${NGINX_VERSION}.tar.gz && \
  rm nginx-${NGINX_VERSION}.tar.gz

#Get nginx-rtmp module:
RUN cd /tmp && \
  wget https://github.com/arut/nginx-rtmp-module/archive/v${NGINX_RTMP_VERSION}.tar.gz && \
  tar zxf v${NGINX_RTMP_VERSION}.tar.gz && rm v${NGINX_RTMP_VERSION}.tar.gz

#Compile nginx + module:
RUN cd /tmp/nginx-${NGINX_VERSION} && \
  ./configure \
  --prefix=/opt/nginx \
  --add-module=/tmp/nginx-rtmp-module-${NGINX_RTMP_VERSION} \
  --conf-path=/opt/nginx/nginx.conf \
  --error-log-path=/opt/nginx/logs/error.log \
  --http-log-path=/opt/nginx/logs/access.log \
  --with-debug && \
  cd /tmp/nginx-${NGINX_VERSION} && make && make install

#Cleanup:
RUN rm -rf /var/cache/* /tmp/*

#Modify the nginx.conf:
ADD nginx.conf /opt/nginx/nginx.conf
ADD static /www/static

#Install API dependencies:
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app 

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "/app/entrypoint.sh" ]
