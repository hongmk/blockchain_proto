from time import time
from creathash import *
import json
from httpquery import HttpQuery

class Blockchain:

    def __init__(self, address):
        self.current_transactions = []
        self.chain = []
        self.nodes = []   
        self.node_type = 0
        self.http_req = HttpQuery()
        self.address = address
        #최초 생성시 자신을 노드리스트에 추가하며, 최초 노드가 마스터가됨
        try:
            if address == '127.0.0.1:5000':
                self.node_type = 1
                #self.register_node(address, True, self.node_type)
                self.new_block(previous_hash='0')
            else:
                self.node_type = 2
                self.register_node('127.0.0.1:5000', True, 1) #노드 생성 시 마스터노드는 디폴트로 등록함
                #self.register_node(address, True, self.node_type)
        except: 
            return None

    def new_block(self, previous_hash):
        #새로운 블록을 생성 후 체인에 등록한다
        #블록 구조: 블록해시(거래내역의해시정보) + 블록헤더 + 거래정보 + nonce
        #현재 nonce 값은 미사용 (PoW 구현 시 사용예정)

        blockheader = {
            'version': len(self.chain) + 1,
            'timestamp': time(),
            'previous_hash': previous_hash or getHash(self.chain[-1]['header']),
            'transactions_hash': getHash(self.current_transactions)
        }

        block = {
            'block_hash': getHash(blockheader),
            'header': blockheader,
            'transactions': self.current_transactions,
            'nonce': 0
        }

        #생성된 거래내역을 다른 노드에 전송
        #self.spread_transaction(self.current_transactions[-1])

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        #새로운 거래발생 시 현재 거래리스트에 추가하며, 등록될 블록 인덱스를 반환함
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        if len(self.chain) == 0:
            return 1
        else:
            return self.last_block['header']['version'] + 1

    def verify_of_chain(self):
        result = {}
        error_bit = 0

        #최초블록만 존재하는 경우는 검증하지 않음
        try:
            assert len(self.chain) > 1
        except:
            result = {'result': False, 'msg':'거래블록 생성 전입니다.'}
            error_bit = 1

        if error_bit == 0:
            prev_block_hash = self.chain[-2]['block_hash']
            cur_block_hash = self.chain[-1]['header']['previous_hash']

            if prev_block_hash == cur_block_hash:
                result = {'result': True, 'msg': '검증성공'}
            else: 
                result = {'result': False, 'msg': '검증실패'}

        return result

    def register_node(self, address, status=True, node_type=2):
        #노드중복체크 -> 노드생성 -> 노드등록 프로세스임 

        dup_check = 0
        if len(self.nodes) > 0:
            dup_check = self.check_node_dup(address)
        else:
            dup_check = 1

        if dup_check != 0:
            if dup_check == 1:
                self.node = Node()
                self.node_info = self.node.set_node_info(address, status, node_type)
                self.nodes.append(self.node_info)
                #print(json.dumps(self.nodes))
                result =  {'result':True , 'msg':'노드 등록 성공'}
            elif dup_check == 2:
                result =  {'result':True , 'msg':'비활성 노드를 활성화합니다.'}

            #새로 생성되거나 상태가 변경된 노드를 참가자 노드에 전송함
            if self.node_type == 1:
                self.spread_node_list(address)

        else:
            result = {'result':False , 'msg':'이미 활성상태인 노드가 존재합니다.'}

        return result

    def check_node_dup(self, address):
        #노드 중복체크 프로세스이며, 이미 존재하는 노드의 상태가 False 였을 경우 True로만 변경함
        result = 0

        for node in self.nodes:
            result = 1

            if node['address'] == address:
                result = 0
                if node['status'] == False:
                    node['status'] = True
                    result = 2
                return result
            else:
                print('중복없음')
        
        result = 1

        return result       

    def spread_node_list(self, register_address):
        #활성상태인 모든 모드에 새로등록되거나 상태가 변경된 노드를 전송함
        #print('전송대상 노드:', json.dumps(self.nodes[-1], indent = 4, sort_keys=True))
        if len(self.nodes) > 1:

            for node in self.nodes:
                address = ''
                params = {}
                nodes_size = len(self.nodes)
                #마지막(현재추가된) 노드는 전송 대상에서 제외함
                if node['status'] == True and node['address'] != register_address:
                    address = 'http://'+node['address']+'/nodes/register'
                    params = {'address': register_address}
                    print('address:', node['address'], 'params:', params)
                    result = self.http_req.send_request('POST', address, params)

                    #if node['address'] != register_address:
                    #새로추가된 노드에는 활성화된 노드를 모두 전송해줌
                    address = 'http://'+register_address+'/nodes/register'
                    params = {'address': node['address']}
                    print('마지막 노드에 전송 address:', node['address'], 'params:', params)
                    result = self.http_req.send_request('POST', address, params)
        return True

    def get_node_count(self):
        #노드 총 개수 전달
        return {'result': True, 'data':len(self.nodes)}

    #내부용
    def spread_transaction(self, transaction):
        print('거래전송', transaction)
        result = ''
        index = 0
        for node in self.nodes:
            if self.address != node['address']: #현재 노드가 아닌 노드에만 전송
                print('대상노드:', node, index)

                address = 'http://'+node['address']+'/transactions/set'
                params = {'transaction':transaction}

                print('address:', address, 'params:', params)
                self.http_req.send_request('POST', address, params)    
            index = index + 1
        return True

    def set_transaction(self, transaction):
        print('다른 노드로부터 전송된 거래수신', transaction)
        self.current_transactions.append(transaction)
        #previous_hash = '0'
        #self.new_block(getHash(self.chain[-1]['header']))
        #return self.last_block['header']['version'] + 1
        return True


    @property
    def last_block(self):
        return self.chain[-1]

class Node:
    def __init__(self):
        self.node_info = {}

    def set_node_info(self, address, status, node_type):
        self.node_info = {
            'address': address,         #추가되는 노드의 IP:PORT
            'status': status,           #노드의 상태 True: 활성상태 , False:비활성상태
            'node_type': node_type      #노드의 타입 1: 마스터 , 2: 참가자
        }

        return self.node_info


