#!/usr/bin/python2

# Possibly a daemon to run a webserver and arduino
# Created March 4, 2016
# Author: Stuart de Haas

import web
import subprocess
import string
import RGBpi

ser = RGBpi.connectPi()

render = web.template.render('templates/')

urls = (
# URL '/' i.e. front page to be handled by the class 'index'
        '/', 'index',
        '/changeColour_(.*)', 'changeColour',
        '/tracks', 'tracks',
        '/artists', 'artists',
        '/play', 'play',
        '/songs', 'songs',
        '/party', 'party',
        '/control', 'control'
        )

backgroundCol = 'white'
currArtist = ""
artistList = ""
trackList = ""
location = ""

class index:
    def GET(self):
        global artistList
        playing = subprocess.check_output(['rhythmbox-client --print-playing'], shell=True)
        return render.index(backgroundCol, currArtist, artistList, trackList, location, playing)

def allArtists():
    global trackList
    global artistList
    trackList = ""
    artistList = ""

    shit = subprocess.check_output(["./searchTunes -l"], shell=True)
    shit = string.split(shit, '\n')
    for line in shit:
        artistList = artistList + '<option>' + line + '</option>\n'

class artists:
    """ Find artists based on search or output all of them """
    def POST(self):
        search = web.input()
        if search.search == "Reset":
            allArtists()
        else:
            shit = subprocess.check_output(['./searchTunes -a "' + search.search + '"'], shell=True)
            shit = string.split(shit, '\n')
            global artistList
            artistList = ""
            for line in shit:
                artistList = artistList + '<option>' + line + '</option>\n'
        raise web.seeother('/')

class tracks:
    """ Find all songs associated with a Artist """
    def POST(self):
        form = web.input()
        global currArtist
        currArtist = form.artist
        shit = subprocess.check_output(['./searchTunes -s "' + currArtist + '"'], shell=True)
        shit = string.split(shit, '\n')
        global trackList
        trackList = ""
        for line in shit:
            if '%' not in line:
                continue
            poop = string.split(line, '%')
            trackList = trackList + '<option value="' + poop[0] + '">' + poop[1] + '</option>\n'
        raise web.seeother('/')
class songs:
    """ Find all songs containing the search term """
    def POST(self):
        form = web.input()
        search = form.search
        shit = subprocess.check_output(['./searchTunes -t "' + search + '"'], shell=True)
        shit = string.split(shit, '\n')
        global trackList
        trackList = ""
        for line in shit:
            if '%' not in line:
                continue
            poop = string.split(line, '%')
            trackList = trackList + '<option value="' + poop[0] + '">' + poop[1] + '</option>\n'
        raise web.seeother('/')
class play:
    def POST(self):
        form = web.input()
        global currTrack
        global location
        location = form.track
        subprocess.call('rhythmbox-client --enqueue ' + location, shell=True)
        raise web.seeother('/')

class party:
    def POST(self):
        subprocess.call('PARTY', shell=True)
        raise web.seeother('/')
class control:
    def POST(self):
        form = web.input()
        subprocess.call('rhythmbox-client --' + form.cmd, shell=True)
        raise web.seeother('/')


class changeColour:
    def GET(self):
        raise web.seeother('/')
    def POST(self, colour):
        if RGBpi.isAlive(ser):
            RGBpi.changeCol(ser, colour)
            global backgroundCol
            backgroundCol = colour
        raise web.seeother('/')


allArtists()
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
