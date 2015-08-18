import sys as SYSTEM
import requests

from config import AUTH, urlLogin, urlTrace

### SETUP ###
# start a session
s = requests.Session()
# login user
r = s.post(urlLogin, params=AUTH)

################################################################
# Input args and help

if len(SYSTEM.argv) > 1 and SYSTEM.argv[1] == "-h":
  print "Default Usage: python list_traces.py"
  SYSTEM.exit(0)

################################################################
# List of available (uploaded) traces for all systems

r = s.get(urlTrace)

if r.status_code != 200:
  print r.text
  SYSTEM.exit(1)

traces = r.json()

systems = {}
for trace in traces:
  sysName = trace['system']['name']
  if sysName in systems:
    sys = systems[sysName]
  else:
    sys = systems[sysName] = []
  sys.append(trace)

for sys in systems:
  print 'System ' + sys
  print ""

  sysTraces = systems[sys]
  for trace in sysTraces:
    print 'Trace ID: ' + str(trace['id']) + ' Name:  ' + trace['name'] + \
          ' Type: ' + trace['type']

  print ""
