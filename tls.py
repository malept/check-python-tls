#!/usr/bin/env python2

from __future__ import print_function
import json
import os
import ssl
import subprocess
import sys
try:
  from urllib2 import urlopen
except ImportError:
  # For Python 3, from urllib.request import urlopen
  print('Please make sure Python 2 is installed.')
  if sys.platform == 'win32':
    print('Download the latest Python 2 version from https://www.python.org/downloads/windows/')
  elif sys.platform == 'darwin':
    print('Run "brew install python@2" and make sure "python" points to python2')
  sys.exit(1)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def check_tls(verbose):
  process = subprocess.Popen(
    'node server',
    cwd=os.path.dirname(os.path.realpath(__file__)),
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
  )

  port = process.stdout.readline()
  localhost_url = 'https://localhost:' + port

  response = json.load(urlopen(localhost_url, context=ctx))
  tls = response['protocol']
  process.wait()

  if sys.platform in ["linux", "linux2"]:
    tutorial = "/docs/development/build-instructions-linux.md"
  elif sys.platform == "darwin":
    tutorial = "/docs/development/build-instructions-macos.md"
  elif sys.platform == "win32":
    tutorial = "/docs/development/build-instructions-windows.md"
  else:
    tutorial = "build instructions for your operating system" \
      + "in ./docs/development/"

  if tls == "TLSv1" or tls == "TLSv1.1":
    print("Your system/python combination is using an outdated security " +
      "protocol and will not be able to compile Electron.\n\nPlease see " +
      "https://github.com/electron/electron/blob/master" + tutorial + " " +
      "for instructions on how to update Python.")
    sys.exit(1)
  else:
    if verbose:
      print("Your Python is using " + tls + ", which is sufficient for " +
        "building Electron.")

if __name__ == '__main__':
  check_tls(True)
  sys.exit(0)
