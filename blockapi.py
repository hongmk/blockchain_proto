from blocktestcase import *
from creathash import *
#import requests
from flask import Flask, jsonify, request

#초기 블록 생성
default_ip = '127.0.0.1'
default_port = '5001'

test_obj = BlockchainTestCase()
test_obj.setUp(default_ip+':'+ default_port)

app = Flask(__name__)

#새로운 거래발생 및 블록등록
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	#신규 거래 및 블록 생성

	values = request.form

	available_arg_list = ['sender', 'recipient', 'amount']
	if not all(k in values.keys() for k in available_arg_list):
		return '정당한 파라미터가 아닙니다.', 400

	index = test_obj.create_transaction(values['sender'], values['recipient'], values['amount'])
	test_obj.create_block()

	response = {'message': f'이번 거래는 {index} 블록에 등록됩니다.'}

	return jsonify(response), 201

#다른노드에서 전송되는 거래를 수신함
@app.route('/transactions/set', methods=['POST'])
def set_transaction():
	values = request.form
	test_obj.set_transaction(values['transaction'])

#체인에 연결된 블록리스트 출력
@app.route('/chains', methods=['GET'])
def chain():
	#print(json.dumps(test_obj.blockchain.chain, indent = 4))
	return jsonify(test_obj.blockchain.chain), 200

#블록 변조 검증(이전 해시값 확인)
@app.route('/chains/verify', methods=['GET'])
def verify_block():
	return jsonify(test_obj.verify_of_chain())

@app.route('/nodes/register', methods=['POST'])	
def register_node():
	values = request.form
	result = test_obj.register_node(values['address'])

	return jsonify(result), 201

@app.route('/nodes/list', methods=['GET'])
def all_node_list():
	return jsonify(test_obj.blockchain.nodes), 200

@app.route('/nodes/count', methods=['GET'])
def node_count():
	result = test_obj.get_node_count()
	return jsonify(result), 200


#0.0.0.0:5000 포트로 리스닝
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=default_port)
