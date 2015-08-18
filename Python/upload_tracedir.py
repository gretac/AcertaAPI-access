import sys as SYSTEM
import os
import json
import requests
from requests_toolbelt.multipart import encoder

from config import AUTH, urlLogin, urlUpload, urlSys, urlTrace

### SETUP ###
# start a session
s = requests.Session()
# login user
r = s.post(urlLogin, params=AUTH)

if r.status_code != 200:
  print 'Cannot log in; check credentials.'
  SYSTEM.exit(1)

################################################################
# Input args and help

def printHelp():
  print "Default Usage: python upload_trace.py system_name dir_path [type]"

if len(SYSTEM.argv) > 1 and SYSTEM.argv[1] == "-h":
  printHelp()
  SYSTEM.exit(0)

if len(SYSTEM.argv) < 3:
  printHelp()
  SYSTEM.exit(1)

def report_progress(monitor):
  progress = float(monitor.bytes_read) / float(monitor.len) * 100
  print ("%.2f" % progress) + '% ...' ,
  SYSTEM.stdout.flush()

systemName = SYSTEM.argv[1]
sysPayload = {'systemName': systemName}

dir_path = SYSTEM.argv[2]

if not os.path.isdir(dir_path):
  print "Cannot locate the traces directory."
  SYSTEM.exit(1)

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
system = serverSys

################################################################
# Upload trace

traceNames = [
  trace for trace in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, trace))
]

for traceName in traceNames:
  tracePath = os.path.join(dir_path, traceName)

  # determine file type

  supportedTypes = ['QNX', 'CAN']

  if len(SYSTEM.argv) == 4 and SYSTEM.argv[3]:
    fileType = SYSTEM.argv[3]
    if fileType not in supportedTypes:
      print "Unrecognized file type."
      SYSTEM.exit(1)
  elif traceName.endswith('.kev') or traceName.endswith('.trace'):
    fileType = 'QNX'
  elif traceName.endswith('.asc'):
    fileType = 'CAN'
  else:
    print 'Cannot determine the type of the trace. Please specify type explicitly.'
    printHelp()
    SYSTEM.exit(1)

  ################################################################
  # Upload a trace

  try:
    traceFile = (traceName, open(tracePath, 'rb'))
  except IOError as e:
    print "Error while reading file"
    print "I/O error ({0}): {1}".format(e.errno, e.strerror)
    SYSTEM.exit(1)

  e = encoder.MultipartEncoder(
    fields={
      'traceFile': traceFile,
      'fileType': fileType,
      'system': json.dumps(system)
    })

  m = encoder.MultipartEncoderMonitor(e, report_progress)

  print 'UPLOADING...'
  r = s.post(urlUpload, data=m, headers={'Content-Type': e.content_type})

  if r.status_code != 200:
    print r.text
    SYSTEM.exit(1)

  fileInfo = r.json()['fileInfo']

  print 'DONE PROCESSING...'
  print 'File Uploaded Name: ' + fileInfo['traceName']

  ################################################################
  # Create a trace record

  payload = { 'name': fileInfo['traceName'], 'type': fileInfo['fileType'],
    'size': fileInfo['fileSize'], 'status': fileInfo['status'],
    'system': system
  }

  r = s.post(urlTrace, data=json.dumps(payload))

  if r.status_code != 200:
    print r.text
    SYSTEM.exit(1)

  trace = r.json()

  print 'Trace ID: ' + str(trace['traceId']) + ' Name: ' + traceName
  print ''
