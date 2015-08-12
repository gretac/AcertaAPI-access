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
  sysId = trace['system']['id']
  if sysId in systems:
    sys = systems[sysId]
  else:
    sys = systems[sysId] = []
  sys.append(trace)

for sys in systems:
  sysTraces = systems[sys]
  printedSyInfo = False

  for trace in sysTraces:
    if not printedSyInfo:
      sys = trace['system']
      print 'System ID: ' + str(sys['id']) + ' Name: ' + sys['name']
      print ""
      printedSyInfo = True

    print 'Trace ID: ' + str(trace['id']) + ' Name:  ' + trace['name'] + \
          ' Type: ' + trace['type']
  print ""
