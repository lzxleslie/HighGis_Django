#!/bin/sh
gnome-terminal -x bash -c "./django.sh"
echo "Django Server is opened"
echo "open TileStache Server"
uwsgi --http :8888 --workers 8 --eval 'import TileStache; application = TileStache.WSGITileServer("/home/whu/src/TileStache/tilestache.cfg")'


