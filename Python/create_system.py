import sys as SYSTEM
import json
import requests

from config import AUTH, urlLogin, urlSys

### SETUP ###
# start a session
s = requests.Session()
# login user
r = s.post(urlLogin, params=AUTH)

################################################################
# Input args and help

def printHelp():
  print "Default Usage: python create_system.py system_name"

if len(SYSTEM.argv) > 1 and SYSTEM.argv[1] == "-h":
  printHelp()
  SYSTEM.exit(0)

if len(SYSTEM.argv) < 2:
  printHelp()
  SYSTEM.exit(1)

sysPayload = { 'name': SYSTEM.argv[1] }

################################################################
# Create a new system

r = s.post(urlSys, data=json.dumps(sysPayload))

if r.status_code != 200:
  print r.text
  SYSTEM.exit(1)

systems = r.json()

for sys in systems:
  print 'System ID: ' + str(sys['id']) + ' Name: ' + sys['name']
