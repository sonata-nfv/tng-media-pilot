FROM alfg/ffmpeg

ENV CMS ""
ENV AGGREGATOR ""
ENV VIDEO ""

RUN apk update && apk add \
    python3 \
    python3-dev

WORKDIR /app

COPY code/requirements.txt /app

#Python dependencies:
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY video/360_7M.mp4 /app/video
COPY code /app 

ENTRYPOINT [ "/app/entrypoint.sh" ]