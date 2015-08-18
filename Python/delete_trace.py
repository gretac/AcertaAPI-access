import sys as SYSTEM
import json
import requests

from config import AUTH, urlLogin, urlSys, urlTrace, urlFiles

### SETUP ###
# start a session
s = requests.Session()
# login user
r = s.post(urlLogin, params=AUTH)

################################################################
# Input args and help

def printHelp():
  print "Default Usage: python delete_trace.py system_name trace_id"

if len(SYSTEM.argv) > 1 and SYSTEM.argv[1] == "-h":
  printHelp()
  SYSTEM.exit(0)

if len(SYSTEM.argv) < 3:
  printHelp()
  SYSTEM.exit(1)

systemName = SYSTEM.argv[1]
sysPayload = {'systemName': systemName}

traceId = SYSTEM.argv[2]

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
# List of available (uploaded) traces for a specified system

r = s.get(urlTrace, params=sysPayload)

if r.status_code != 200:
  print r.text
  SYSTEM.exit(1)

sysTraces = r.json()

for t in sysTraces:
  if int(t['id']) == int(traceId): trace = t

trace['system'] = serverSys
tracePayload = {'trace': json.dumps(trace)}

################################################################
# Delete trace file and file record

r = s.delete(urlFiles, params=tracePayload)

if r.status_code != 200:
  print r.text
  SYSTEM.exit(1)

################################################################
# Delete an existing trace record

r = s.delete(urlTrace, params=tracePayload)

if r.status_code != 200:
  print r.text
  SYSTEM.exit(1)

print 'Trace ' + traceId + ' from system ' + systemName + ' deleted.'
