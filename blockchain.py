
import hashlib
import json
import logging
import sys
import time

import utils


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

MINING_DIFFICULTY = 3

class BlockChain(object):

  def __init__(self):
    self.transaction_pool = []
    self.chain = []
    self.create_block(0, self.hash({}))

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
      'recipient_blockcahin_address': recipient_blockchain_address,
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



if __name__ == '__main__':
  block_chain = BlockChain()
  utils.pprint(block_chain.chain)

  block_chain.add_transaction('A', 'B', 1.0)
  prevhash = block_chain.hash(block_chain.chain[-1])
  nonce = block_chain.ploof_of_work()
  block_chain.create_block(nonce, prevhash)
  utils.pprint(block_chain.chain)

  block_chain.add_transaction('C', 'D', 3.0)
  prevhash = block_chain.hash(block_chain.chain[-1])
  nonce = block_chain.ploof_of_work()
  block_chain.create_block(nonce, prevhash)
  utils.pprint(block_chain.chain)