import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

from creathash import *

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash):
        #새로운 블록을 생성 후 체인에 등록한다

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or getHash(self.chain[-1]),
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

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        #creathash.py로 모듈화 할 수 도 있고, 이 메소드를 사용해도 무방함
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

