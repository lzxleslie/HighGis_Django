#!/usr/bin/env python
"""tilestache-list.py will list your tiles.

This script is intended to be run directly. This example lists tiles in the area
around West Oakland (http://sta.mn/ck) in the "osm" layer, for zoom levels 12-15:

    tilestache-list.py -b 37.79 -122.35 37.83 -122.25 12 13 14 15

See `tilestache-list.py --help` for more information.
"""

from sys import stderr, path
from optparse import OptionParser

from TileStache.Core import KnownUnknown
from TileStache import MBTiles

from ModestMaps.Core import Coordinate
from ModestMaps.Geo import Location
from ModestMaps.OpenStreetMap import Provider
import os
from tempfile import mkstemp
import TileStache
import ModestMaps
import json
def generateCoordinates(ul, lr, zooms, padding):
    """ Generate a stream of coordinates for seeding.
    
        Flood-fill coordinates based on two corners, a list of zooms and padding.
    """
    # start with a simple total of all the coordinates we will need.
    count = 0
    
    for zoom in zooms:
        ul_ = ul.zoomTo(zoom).container().left(padding).up(padding)
        lr_ = lr.zoomTo(zoom).container().right(padding).down(padding)
        
        rows = lr_.row + 1 - ul_.row
        cols = lr_.column + 1 - ul_.column
        
        count += int(rows * cols)

    # now generate the actual coordinates.
    # offset starts at zero
    offset = 0
    
    for zoom in zooms:
        ul_ = ul.zoomTo(zoom).container().left(padding).up(padding)
        lr_ = lr.zoomTo(zoom).container().right(padding).down(padding)

        for row in range(int(ul_.row), int(lr_.row + 1)):
            for column in range(int(ul_.column), int(lr_.column + 1)):
                coord = Coordinate(row, column, zoom)
                
                yield coord
                offset += 1

def tilesetCoordinates(filename):
    """ Generate a stream of (offset, count, coordinate) tuples for seeding.
    
        Read coordinates from an MBTiles tileset filename.
    """
    coords = MBTiles.list_tiles(filename)
    count = len(coords)
    
    for (offset, coord) in enumerate(coords):
        yield coord
def getTile(layer,extension,x,y,z):
    coord=ModestMaps.Core.Coordinate(int(x), int(y), int(z))
    configFile=open('static/config/tile.cfg')
    config=json.load(configFile)    
    cfg = TileStache.Config.buildConfiguration(config)
    contenttype, content = TileStache.getTile(cfg.layers[layer], coord,extension)
    if not os.path.exists('static/map/'+layer):
            os.mkdir(r'static/map/'+layer)    
    if not os.path.exists('static/map/'+layer+'/'+z):
            os.mkdir(r'static/map/'+layer+'/'+z)
    if not os.path.exists('static/map/'+layer+'/'+z+'/'+y):
            os.mkdir(r'static/map/'+layer+'/'+z+'/'+y)
    #if not os.path.exists('static/map/'+layer+'/'+z+'/'+y+'/'+x):
      #      os.mkdir(r'static/map/'+layer+'/'+z+'/'+y+'/'+x)
    tilepath='static/map/'+layer+'/'+z+'/'+y+'/'+x+'.png'
    open(tilepath, 'w').write(content)
    return contenttype, content
def tilelist(data,zooms):   
        if (data["filetype"]):
            coordinates = MBTiles.list_tiles(data["filename"])
    
        else:
            lat1, lon1, lat2, lon2 = data["bbox"]
            south, west = min(lat1, lat2), min(lon1, lon2)
            north, east = max(lat1, lat2), max(lon1, lon2)
    
            northwest = Location(north, west)
            southeast = Location(south, east)
            
            osm = Provider()
    
            ul = osm.locationCoordinate(northwest)
            lr = osm.locationCoordinate(southeast)
    
            for (i, zoom) in enumerate(zooms):
                if not zoom.isdigit():
                    raise KnownUnknown('"%s" is not a valid numeric zoom level.' % zoom)
    
                zooms[i] = int(zoom)
            
            if data["padding"] < 0:
                raise KnownUnknown('A negative padding will not work.')
    
            coordinates = generateCoordinates(ul, lr, zooms, data["padding"])
            return coordinates
            #filenamelist=[]
            #for coord in coordinates:
                ## render
                #mimetype, content = getTile(data["layer"], coord, data["extension"])
        
                ## save
                #handle, filename = mkstemp(prefix='tile-', suffix='.'+data["extension"])
                #os.write(handle, content)
                #os.close(handle)
                ##
                #filenamelist.append(filename)
            #return coordinates
        

