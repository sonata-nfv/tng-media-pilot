FROM alfg/ffmpeg

ENV CMS ""
ENV AGGREGATOR ""
ARG video
ENV VIDEO=$video

RUN apk update && apk add \
    python3 \
    python3-dev

WORKDIR /app

COPY . /app

#Python dependencies:
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN chmod +x /app/send-video.sh

CMD [ "python3", "/app/cpe.py" ]