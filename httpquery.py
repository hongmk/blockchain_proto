import json
import requests

class HttpQuery:

	def __init__(self):
		self.response = []
		self.req = None

	def send_request(self, method, address, params={}):
		
		if method == 'GET':
			try:
				self.req = requests.get(address)
			except:
				return {'result': False, 'data':'GET 오류발생'}

		elif method == 'POST':
			try:
				self.req = requests.post(address, data=params)
			except:
				return {'result': False, 'data':'POST 오류발생'}

		else:
			return {'result': False, 'data':'잘 못된 Http Method 사용입니다.'}

		return {'result':True, 'data': self.req.json()}