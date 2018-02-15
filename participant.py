import http.client, urllib.parse
import json

"""
#GET 요청 -> 응답내용을 JSON객체로 변환
conn = http.client.HTTPConnection('127.0.0.1:5000')
conn.request("GET", "/nodes/list")

res = conn.getresponse()
nodes = json.loads(res.read().decode())
print(nodes[-1])
"""

"""
#POST 요청으로 노드 신규등록 요청 및 결과 수신

params = urllib.parse.urlencode({'address': '127.0.0.1:5002'})
headers = {"Content-type":"application/x-www-form-urlencoded"}
conn = http.client.HTTPConnection("127.0.0.1:5000")
conn.request("POST", "/nodes/register", params, headers)
response = conn.getresponse()

print(response.status, response.reason)

data = json.loads(response.read().decode())
print(data)

conn.close()
"""