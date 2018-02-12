import hashlib
import json
from unittest import TestCase

from blockchain import Blockchain
from creathash import *

class BlockchainTestCase(TestCase):

    def setUp(self):
        self.blockchain = Blockchain()

    def create_block(self, proof=1, previous_hash='1'):
        previous_hash = getHash(self.blockchain.chain[-1])
        self.blockchain.new_block(proof, previous_hash)

    def create_transaction(self, sender='a', recipient='b', amount=1):
        index = self.blockchain.new_transaction(
            sender=sender,
            recipient=recipient,
            amount=amount
        )

        return index 

    def get_hash_all(self):
        #체인에 등록된 모든 블록의 해시값 json list로 반환

        hash_list = []
        cur_hash_dict = {}

        for chain_obj in self.blockchain.chain:
            cur_hash = getHash(chain_obj)
            cur_hash_dict = {'index':chain_obj['index'], 'cur_hash':cur_hash}
            hash_list.append(cur_hash_dict)

        print(hash_list)
        return hash_list

    def proof_prev_hash(self):
        cur_index = 0
        cur_hash = '1'

        for chain_obj in self.blockchain.chain:
            
            prev_hash = cur_hash
            cur_hash = getHash(chain_obj)
            if cur_index > 0:
                print("start of proof")
                if chain_obj['previous_hash'] == prev_hash:
                    print("hash check result: True")
                else:
                    print("hash check result: False")
                    return False
            cur_index = cur_index + 1

        return True


class TestBlocksAndTransactions(BlockchainTestCase):

    def test_block_creation(self):
        self.create_block()

        latest_block = self.blockchain.last_block

        assert len(self.blockchain.chain) >= 2

    def test_create_transaction(self, sender, recipient, amount):

        index = self.create_transaction(sender, recipient, amount)

        transaction = self.blockchain.current_transactions[-1]

        return index

    def test_return_last_block(self):
        self.create_block()

        created_block = self.blockchain.last_block

        #assert len(self.blockchain.chain) == 2
        assert created_block is self.blockchain.chain[-1]
        return created_block


