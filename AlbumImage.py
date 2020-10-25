from PIL import Image
from time import sleep
import json
import urllib.request
from urllib.parse import* #from urllib import*
from urllib.parse import urlparse
from urllib.parse import urlencode
import ssl
from string import Template
import re
import fnmatch
import os
import sys
from threading import Thread
from socketIO_client import SocketIO

volumio_host = 'localhost'
volumio_port = 3000
volumioIO = SocketIO(volumio_host, volumio_port)

ROWSIZE = 20
data = ()
Song = ''
Artist = ''
Album = ''
Format = ''
Status = ''
albumart = ''
FullJPGPath = ''
activeSong = ''
activeArtist = ''
activeAlbum = ''
activeAlbumart = ''

def JPGPathfinder(String):
    print('JPGPathfinder')
    albumstring = String
    p1 = 'path=(.+?)&metadata'
    result = re.search(p1, albumstring)
    URL = result.group(1)
    URLPath = "/mnt" + URL + '/'
    accepted_extensions = ['jpg', 'jpeg', 'gif', 'png', 'bmp']
    global FullJPGPath
    try:
        filenames = [fn for fn in os.listdir(URLPath) if fn.split(".")[-1] in accepted_extensions]
        JPGName = filenames[0]
        
        FullJPGPath = URLPath + JPGName
    except:
        
        FullJPGPath = '/home/volumio/Album-Art-Tool/NoCover.bmp'
    #global FullJPGPath
    JPGSave(FullJPGPath)
    print('FullJPGPath: ', FullJPGPath)

def JPGSave(Path):
    print('JPGSave')
    FullJPGPath = Path
    img = Image.open(FullJPGPath)     # puts our image to the buffer of the PIL.Image object
    width, height = img.size
    asp_rat = width/height
    new_width = 90
    new_height = 90
    new_rat = new_width/new_height
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    img.save('/home/volumio/album.bmp') 

def JPGSaveURL(link):
    print('JPGSaveURL')
    httpLink = urllib.parse.quote(link).replace('%3A',':')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(httpLink, context=ctx) as url:
        with open('temp.jpg', 'wb') as f:
            f.write(url.read())
    img = Image.open('temp.jpg')
    width, height = img.size
    asp_rat = width/height
    new_width = 90
    new_height = 90
    new_rat = new_width/new_height
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    img.save('/home/volumio/album.bmp') 
    
def onPushState(data):
    #data = json.loads(data)
    print('onPushState') 
    print(data)
    data = data
    global albumart
    global Artist
    global Song
    global Format
    global Status
    global Album
    global activeSong
    global activeArtist
    global activeAlbum
    if 'title' in data:
        Song = data['title']
    else:
        Song = ''
    if Song is None:
        Song = ''
    if Song == 'HiFiBerry ADC':
        Song = 'Bluetooth-Audio'
        
    if 'artist' in data:
        Artist = data['artist']
    else:
        Artist = ''
    if Artist is None and Song != 'HiFiBerry ADC':   #volumio can push NoneType
        Artist = ''
    if Artist == '' and Song == 'HiFiBerry ADC':
        Artist = 'Line-Input:'

    if 'trackType' in data:
        Format = data['trackType']
        activeFormat = Format
        if Format == True and Song != 'HiFiBerry ADC':
            Format = 'WebRadio'
            activeFormat = Format
        if Format == True and Song == 'HiFiBerry ADC':
            Format = 'Live-Stream'
            activeFormat = Format
        
    if 'status' in data:
        Status = data['status']

    if 'albumart' in data:
        albumart = data['albumart']
    if albumart is None:
        albumart = 'nothing'
    AlbumArtHTTP = albumart.startswith('http')
    print('Starts with HTTP: ', AlbumArtHTTP)
    print('Format', Format)

    if 'album' in data:
        Album = data['album']
    
    if 'uri' in data:
        URI = data['uri']
    
    #print(Artist)
    #print(Song)

    if albumart != activeAlbumart:
        activeArtist = Artist
        activeAlbum = Album
        activeSong = Song
        sleep(0.2)
        if AlbumArtHTTP is True and Format == 'webradio':
            JPGSaveURL(albumart)
        else:
            if Artist != '' and Song != '':
                albumdecode = urllib.parse.unquote(albumart, encoding='utf-8', errors='replace')
                print('albumdecode: ', albumdecode)        
                JPGPathfinder(albumdecode)

def _receive_thread():
    volumioIO.wait()

receive_thread = Thread(target=_receive_thread)
receive_thread.daemon = True
receive_thread.start()

volumioIO.on('pushState', onPushState)

volumioIO.emit('getState')

while True:
    #DataReadFunction()
    #print('while')
    sleep(1.0)

