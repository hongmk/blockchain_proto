from blockchain import Blockchain
from creathash import *

class BlockchainTestCase:

    def __init(self):
        return None

    def setUp(self,address):
        #최초블록 생성
        self.blockchain = Blockchain(address)

    def create_transaction(self, sender='a', recipient='b', amount=1):
        #거래내역 생성
        index = self.blockchain.new_transaction(
            sender=sender,
            recipient=recipient,
            amount=amount
        )
        return index 

    def set_transaction(self, transaction):
        print('수신된인자: ', transaction)
        self.blockchain.set_transaction(transaction)

    def create_block(self, previous_hash='0'):
        #블록 생성 및 체인등록
        if len(self.blockchain.chain) == 0:
            previous_hash = '0'
        else:
            previous_hash = getHash(self.blockchain.chain[-1]['header'])

        return self.blockchain.new_block(previous_hash)

    def verify_of_chain(self):
        #이전 블록의 해시값 변조 확인
        result = self.blockchain.verify_of_chain()

        if result['result']:
            print("이전 해시 검증 완료")
        else:
            print("해시값 불일치!")
        
        return result

    def register_node(self, address):
        result = self.blockchain.register_node(address)
        return result

           
"""
class TestSingleNodeAndBlocks(BlockchainTestCase):

    def test_block_creation(self):
        self.create_block()

        latest_block = self.blockchain.last_block

        assert len(self.blockchain.chain) >= 2

    def test_create_transaction(self, sender, recipient, amount):

        index = self.create_transaction(sender, recipient, amount)

        transaction = self.blockchain.current_transactions[-1]

        return index
        """



