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
  print "Default Usage: python delete_system.py system_name"

if len(SYSTEM.argv) > 1 and SYSTEM.argv[1] == "-h":
  printHelp()
  SYSTEM.exit(0)

if len(SYSTEM.argv) < 2:
  printHelp()
  SYSTEM.exit(1)

systemName = SYSTEM.argv[1]
sysPayload = {'systemName': systemName}

################################################################
# Check for system existence on server

r = s.get(urlSys, params=sysPayload)

if r.status_code != 200:
  print r.text
  SYSTEM.exit(1)

serverSys = r.json()

if not serverSys:
  print 'System ' + systemName + ' is NOT found'
  SYSTEM.exit(1)

sysPayload = {'system': json.dumps(serverSys)}

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

print 'System ' + systemName + ' deleted.'
