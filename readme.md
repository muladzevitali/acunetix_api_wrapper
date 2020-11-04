# Acunetix Api flask wrapper 


# Run
```bash
docker-compose build
docker-compose up
```

# Usage

### 1. Authentication (**/auth/login**)
```python
import requests

url = 'http://127.0.0.1:6009/auth/login'
data = dict(username='dastpython', password='f5T#/WfY^p~bsx')
response = requests.post(url, data=data)

auth_token = response.json().get('auth_token')
```
**Return Codes**:
* 400 - No credentials provided (_you must send it with data parameter_)
* 401 - Invalid username or password
*  200 - Successful login, comes with auth_token

**Notice**: _Token doesn't expire for 1 day after it you will get token expired message on protected endpoints, so you need to get new token_

### 2. Admin (**/admin**) 

You can access users **list**, **modify** and **add** them

### 3. Add scan (**/scans**)
With this request you create a scan and start scanning automatically. There is option also for scheduling, but currently not implemented here. 
```python
import requests
auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjIwMzU5NTk4ODMsImlhdCI6MTYwMzk1OTg4MywidXNlcm5hbWUiOiJkYXN0cHl0aG9uIn0.TEjRvv76hwttraDGZinZbEifxWvw0TAtzlklh7rZh9k'
headers = {'Authorization': auth_token}
url = 'http://127.0.0.1:6009/scans'
data = dict(address='http://google.com')
response = requests.post(url, json=data, headers=headers)
scan_id = response.json().get('scan_id')
```
You can add some parameters to data:
* target_type - one of default, demo, network
* target_criticality - one of critical, high, normal, low
* profile - one of full_scan, high_risk_vulnerabilities, cross_site_scripting_vulnerabilities, sql_injection_vulnerabilities, weak_passwords, crawl_only
* authentication - dict object with two parameters: username and password. i.e {"username": "test", "password": "test"}
* login - dict object with two parameters: username and password. i.e {"username": "test", "password": "test"}
* user_agent - user agent string. i.e "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
* custom_headers - list of custom headers. i.e ["Accept: */*","Connection: Keep-alive"]
* custom_cookies - list of odict objects like [{"url": "http://test.vulnweb.com/", "cookie":"UM_distinctid=15da1bb9287f05-022f43184eb5d5-30667808-fa000-15da1bb9288ba9; PHPSESSID=dj9vq5fso96hpbgkdd7ok9gc83"}]
* scan_speed - one of fast, moderate, slow, sequential

So the final request with all parameters in it would be like:
```python
import requests

url = "http://127.0.0.1:6009/scans"

data = {"address": "http://test.vulnweb.com/",
        "description": "Test custom scan speed",
        "target_type": "default",
        "target_criticality": "low",
        "profile": "full_scan",
        "authentication": {"username": "test", "password": "test"},
        "login": {"username": "test", "password": "test"},
        "user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "custom_headers":["Accept: */*","Connection: Keep-alive"],
        "custom_cookies":[{"url": "http://test.vulnweb.com/", "cookie":"UM_distinctid=15da1bb9287f05-022f43184eb5d5-30667808-fa000-15da1bb9288ba9; PHPSESSID=dj9vq5fso96hpbgkdd7ok9gc83"}],
        "scan_speed": "slow"
}
headers = {
  'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjIwMzU5NTk4ODMsImlhdCI6MTYwMzk1OTg4MywidXNlcm5hbWUiOiJkYXN0cHl0aG9uIn0.TEjRvv76hwttraDGZinZbEifxWvw0TAtzlklh7rZh9k',
  'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, json=data)
scan_id = response.json().get('scan_id')
```

**Return Codes:**
* 200 - Operation done successfully
* 400 - Some error occurred. Error comes in response.json
**Notice:** _Default values for each meta parameters are: description='', target_type='default', target_criticality='normal', profile='full_scan'_
So with full indication of parameters in above code data parameter will be:
```python
data = dict(address='http://google.com', description='Google homepage', target_type='default', target_criticality='normal', profile='full_scan')
```


### 4. Pause, Resume, Abort scan (**/scans/<scan_id>/pause**, **/scans/<scan_id>/resume**, **/scans/<scan_id>/abort**)

```python
import requests
auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjIwMzU5NTk4ODMsImlhdCI6MTYwMzk1OTg4MywidXNlcm5hbWUiOiJkYXN0cHl0aG9uIn0.TEjRvv76hwttraDGZinZbEifxWvw0TAtzlklh7rZh9k'
headers = {'Authorization': auth_token}
scan_id = 'a23bbcc1-4b48-4d23-8ede-8f1d9c6f4ea9'
url = 'http://127.0.0.1:6009/scans/%s/pause' % scan_id
response = requests.get(url, headers=headers)
scan_id = response
```

*Return codes:*
* 201 - Operation done successfully
* 400 - Invalid scan status i.e already paused, resumed or aborted

### 5. Results meta data (**/scans/<scan_id>/results**)
```python
import requests
auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjIwMzU5NTk4ODMsImlhdCI6MTYwMzk1OTg4MywidXNlcm5hbWUiOiJkYXN0cHl0aG9uIn0.TEjRvv76hwttraDGZinZbEifxWvw0TAtzlklh7rZh9k'
headers = {'Authorization': auth_token}
scan_id = 'a23bbcc1-4b48-4d23-8ede-8f1d9c6f4ea9'
url = 'http://127.0.0.1:6009/scans/%s/results' % scan_id
response = requests.get(url, headers=headers)
results = response.json()
```

**Result codes:**
* 200 - Operation done successfully
* 404 - Invalid scan id

### 6. Vulnerabilities (**/scans/<scan_id>/vulnerabilities**)
```python
import requests
auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjIwMzU5NTk4ODMsImlhdCI6MTYwMzk1OTg4MywidXNlcm5hbWUiOiJkYXN0cHl0aG9uIn0.TEjRvv76hwttraDGZinZbEifxWvw0TAtzlklh7rZh9k'
headers = {'Authorization': auth_token}
scan_id = 'a23bbcc1-4b48-4d23-8ede-8f1d9c6f4ea9'
url = 'http://127.0.0.1:6009/scans/%s/vulnerabilities' % scan_id
response = requests.get(url, headers=headers)
results = response.json()
```

**Result codes:**
* 200 - Operation done successfully
* 404 - Invalid scan id

### 7. Statistics (**/scan/<scan_id>/statistics**)
```python
import requests
auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjIwMzU5NTk4ODMsImlhdCI6MTYwMzk1OTg4MywidXNlcm5hbWUiOiJkYXN0cHl0aG9uIn0.TEjRvv76hwttraDGZinZbEifxWvw0TAtzlklh7rZh9k'
headers = {'Authorization': auth_token}
scan_id = 'a23bbcc1-4b48-4d23-8ede-8f1d9c6f4ea9'
url = 'http://127.0.0.1:6009/scans/%s/statistics' % scan_id
response = requests.get(url, headers=headers)
results = response.json()
```

**Result codes:**
* 200 - Operation done successfully
* 404 - Invalid scan id

### 8. Register report request (**/reports**)
```python
import requests

auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjIwMzU5NTk4ODMsImlhdCI6MTYwMzk1OTg4MywidXNlcm5hbWUiOiJkYXN0cHl0aG9uIn0.TEjRvv76hwttraDGZinZbEifxWvw0TAtzlklh7rZh9k'
headers = {'Authorization': auth_token}
data = {'scan_id': '771fc67d-9892-40fd-81a6-9f75bdfa227d'}

url = "http://127.0.0.1:6009/reports"
response = requests.post(url, headers=headers, json=data,)
report_id = response.json().get('report_id')
```
**Result codes:**
* 200 - Operation done successfully
* 404 - scan not found with given id


### 9. Check report status (**/reports/<report_id>**)
```python
import requests

auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjIwMzU5NTk4ODMsImlhdCI6MTYwMzk1OTg4MywidXNlcm5hbWUiOiJkYXN0cHl0aG9uIn0.TEjRvv76hwttraDGZinZbEifxWvw0TAtzlklh7rZh9k'
headers = {'Authorization': auth_token}

url = "http://127.0.0.1:6009/reports/<report_id>"
response = requests.get(url, headers=headers)
response_data = response.json()
status = response_data.get('status')
if status == 'completed':
    file_path = response_data.get('download')
```

**Result codes:**
* 200 - Operation done successfully i.e gives the report meta data.
* 400 - report getting error. Comes with error message

### 10. Download report in xml (**/reports/download/<file_name>**)
```python
import requests

auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjIwMzU5NTk4ODMsImlhdCI6MTYwMzk1OTg4MywidXNlcm5hbWUiOiJkYXN0cHl0aG9uIn0.TEjRvv76hwttraDGZinZbEifxWvw0TAtzlklh7rZh9k'
headers = {'Authorization': auth_token}

url = "http://localhost:6009/reports/download/<file_name>"
response = requests.get(url, headers=headers)
file = response.content
```

**Result codes:**
* 200 - Operation done successfully i.e gives the report meta data.
* 400 - report getting error. Comes with error message

