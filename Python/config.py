HTTP = 'http://'
HTTPS = 'https://'
HOST = "test.acerta.ca"
PORT = ""

## LOGIN Credentials ##

AUTH = { 'username':'', 'password':'' }

## API endpoints ##

urlLogin = HTTPS + HOST + ":" + PORT + "/login"
urlUpload = HTTPS + HOST + ":" + PORT + "/api/upload"

urlTrace = HTTPS + HOST + ":" + PORT + "/api/traces"
urlSys = HTTPS + HOST + ":" + PORT + "/api/systems"

urlFiles = HTTPS + HOST + ":" + PORT + "/api/files"
urlSysFiles = HTTPS + HOST + ":" + PORT + "/api/files/sys"
urlReport = HTTP + HOST + ":" + PORT + "/api/reports/summary"
