docker pull ignaciodomin/media-cpe:dev
docker run --rm -v tee:/workspace ignaciodomin/media-cpe:dev ${workspace.absolutePath}/config.cfg
