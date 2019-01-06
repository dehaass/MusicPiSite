#!/bin/python2
# Created: March 16, 2016
# Stuart de Haas
#
# Formats a list of artists into a HTML page

import subprocess

print("Content-type: text/html\n\n")
print("<html><body>")

subprocess.call("searchTunes -l led")

print("</body></html>")
