from time import time
from creathash import *

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        # Create the genesis block
        self.new_block(previous_hash='0')

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

            print('Hash Set:' + prev_block_hash + ',' + cur_block_hash )

            if prev_block_hash == cur_block_hash:
                result = {'result': True, 'msg': '검증성공'}
            else: 
                result = {'result': False, 'msg': '검증실패'}

        return result

    @property
    def last_block(self):
        return self.chain[-1]

