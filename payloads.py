from test_blockchain import *
from creathash import *
import requests
from flask import Flask, jsonify, request

#초기 블록 생성
test_obj = TestBlocksAndTransactions()
test_obj.setUp()

app = Flask(__name__)

#새로운 거래발생 및 블록등록
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	values = request.form

	required = ['sender', 'recipient', 'amount']
	if not all(k in values.keys() for k in required):
		return 'Missing values', 400

	index = test_obj.test_create_transaction(values['sender'], values['recipient'], values['amount'])
	test_obj.test_block_creation()

	response = {'message': f'Transaction will be added to Block {index}'}
	return jsonify(response), 201

#체인에 연결된 블록리스트 출력
@app.route('/chains', methods=['GET'])
def chain():
	#print(json.dumps(test_obj.blockchain.chain, indent = 4))
	return jsonify(test_obj.blockchain.chain), 200

#체인에 연결된 모든 블록의 해시값 산출
@app.route('/chains/hash', methods=['GET'])
def get_hash_list():
	return jsonify(test_obj.get_hash_all())


#0.0.0.0:5000 포트로 리스닝
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=5000)
