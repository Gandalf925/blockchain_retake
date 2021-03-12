
import hashlib
import json
import logging
import sys
import time

import utils


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

MINING_DIFFICULTY = 3
MINING_SENDER = 'THE BLOCKCHAIN'
MINING_REWARD = 12.5

class BlockChain(object):

  def __init__(self, blockchain_address=None):
    self.transaction_pool = []
    self.chain = []
    self.create_block(0, self.hash({}))
    self.blockchain_address = blockchain_address

  def create_block(self, nonce, prevhash):
    block = utils.sorted_dict_by_key({
      'timestamp': time.time(),
      'transactions': self.transaction_pool,
      'nonce': nonce,
      'prevhash': prevhash
    })
    self.chain.append(block)
    self.transaction_pool = []
    return block

  def hash(self, block):
    sorted_block = json.dumps(block, sort_keys=True)
    return hashlib.sha256(sorted_block.encode()).hexdigest()

  def add_transaction(self, sender_blockchain_address, recipient_blockchain_address, value):
    transaction = {
      'sender_blockchain_address':sender_blockchain_address,
      'recipient_blockchain_address': recipient_blockchain_address,
      'value': float(value)
    }
    self.transaction_pool.append(transaction)
    return True

  def valid_proof(self, transactions, prevhash, nonce, difficulty=MINING_DIFFICULTY):
    guess_block = utils.sorted_dict_by_key({
      'transactions': transactions,
      'prevhash': prevhash,
      'nonce': nonce
    })
    guess_hash = self.hash(guess_block)
    return guess_hash[:difficulty] == '0'*difficulty

  def ploof_of_work(self):
    transactions = self.transaction_pool.copy()
    prevhash = self.hash(self.chain[-1])
    nonce = 0
    while self.valid_proof(transactions, prevhash, nonce) is False:
      nonce += 1
    return nonce

  def mining(self):
    self.add_transaction(
      sender_blockchain_address=MINING_SENDER, recipient_blockchain_address=self.blockchain_address, value=MINING_REWARD
    )
    nonce = self.ploof_of_work()
    prevhash = self.hash(self.chain[-1])
    self.create_block(nonce, prevhash)
    logger.info({'action': 'mining', 'status': 'success'})
    return True

  def calculate_total_ammount(self, blockchain_address):
    total_amount = 0.0
    for block in self.chain:
      for transaction in block['transactions']:
        value = float(transaction['value'])
        if blockchain_address == transaction['recipient_blockchain_address']:
          total_amount += value
        if blockchain_address == transaction['sender_blockchain_address']:
          total_amount -= value
    return total_amount

if __name__ == '__main__':
  my_address = 'my_address'
  block_chain = BlockChain(blockchain_address=my_address)
  utils.pprint(block_chain.chain)

  block_chain.add_transaction('A', 'B', 1.0)
  block_chain.mining()
  utils.pprint(block_chain.chain)

  block_chain.add_transaction('C', 'D', 3.0)
  block_chain.mining()
  utils.pprint(block_chain.chain)

  print(block_chain.calculate_total_ammount(my_address))
  print('C:', block_chain.calculate_total_ammount('B'))
  print('D:', block_chain.calculate_total_ammount('D'))
