docker pull ignaciodomin/media-cpe:dev
docker run --rm -v cpe_vol:/tests ignaciodomin/media-cpe:dev ${workspace.absolutePath}/config.cfg
