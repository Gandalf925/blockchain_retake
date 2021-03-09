
import hashlib
import json
import logging
import sys
import time

import utils


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

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

def pprint(chains):
  for i, chain in enumerate(chains):
    print(f'{"="*25} Chain {i} {"="*25}')
    for k, v in chain.items():
      print(f'{k:25}{v}')
  print(f'{"*"*25}')

if __name__ == '__main__':
  block_chain = BlockChain()
  pprint(block_chain.chain)

  prevhash = block_chain.hash(block_chain.chain[-1])
  block_chain.create_block(9, prevhash)
  pprint(block_chain.chain)

  prevhash = block_chain.hash(block_chain.chain[-1])
  block_chain.create_block(2, prevhash)
  pprint(block_chain.chain)