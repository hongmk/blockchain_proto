#import http.client, urllib.parse
import json
#import requests
from httpquery import HttpQuery
from blockchain import Blockchain, Node
from test_blockchain.py

class ChainNodeTest(BlockchainTestCase):
	def __init__(self):
		self.other_nodes=[]
		self.http_req = HttpQuery()
		self.result = []
		self.my_address = '127.0.0.1:5003'

	def get_node_list(self, address):
		self.result = self.http_req.send_request('GET', address)

	def register_node(self, address, params):
		self.result = self.http_req.send_request('POST', address, params)

	def get_node_count(self, address):
		self.result = self.http_req.send_request('GET', address)

def test_node(type):
	obj = ChainNodeTest()
	address = 'http://127.0.0.1:5000'
	params = {'address':obj.my_address}
	result = []

	if type == 1: 	#GET Node List
		obj.get_node_list(address+'/nodes/list')

	elif type == 2: #POST register Node
		obj.register_node(address+'/nodes/register', params)
	elif type == 3:
		print(obj.get_node_count(address+'/nodes/count'))

	else:
		return {'result':False, 'data':'정당한 거래구분이 아닙니다'}

	print(obj.result)
	
	return True

if __name__ == "__main__":
	#test_node(1)
	test_node(2)
	#test_node(1)
	test_node(3)


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