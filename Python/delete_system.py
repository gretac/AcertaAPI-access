import sys as SYSTEM
import json
import requests

from config import AUTH, urlLogin, urlSys, urlSysFiles

### SETUP ###
# start a session
s = requests.Session()
# login user
r = s.post(urlLogin, params=AUTH)

################################################################
# Input args and help

def printHelp():
  print "Default Usage: python delete_system.py system_id system_name"

if len(SYSTEM.argv) > 1 and SYSTEM.argv[1] == "-h":
  printHelp()
  SYSTEM.exit(0)

if len(SYSTEM.argv) < 3:
  printHelp()
  SYSTEM.exit(1)

system = { 'id': SYSTEM.argv[1] ,'name': SYSTEM.argv[2] }
sysPayload = { 'system': json.dumps(system) }

################################################################
# Check for system existence on server

r = s.get(urlSys, params=sysPayload)

if r.status_code != 200:
  print r.text
  SYSTEM.exit(1)

serverSys = r.json()

if not serverSys:
  print 'System ID: ' + str(system['id']) + ' Name: ' + system['name'] + ' is NOT found'
  SYSTEM.exit(1)

################################################################
# Delete all system files (i.e. trace files and db file) and file records

r = s.delete(urlSysFiles, params=sysPayload)

if r.status_code != 200:
  print r.text
  SYSTEM.exit(1)

################################################################
# Delete an existng system record

r = s.delete(urlSys, params=sysPayload)

if r.status_code != 200:
  print r.text
  SYSTEM.exit(1)

print 'System ' + system['name'] + ' deleted.'
