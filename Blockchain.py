from datetime import datetime
import json
import hashlib

class Blockchain:
  def __init__(self):
    self.chain = []
    self.current_transactions = []
    self.new_block(previous_hash=1, proof=100)
    
  def new_block(self, proof, previous_hash=None):
    block = {
      'index': len(self.chain) + 1,
      'timestamp': datetime.now(),
      'proof': proof,
      'previous_hash': previous_hash or self.hash(self.last_block),
    }

    self.current_transactions = []
    self.chain.append(block)

    return block
  
  def new_transaction(self, sender, receiver, amount):
    self.current_transactions.append({
      'sender': sender,
      'recipient': receiver,
      'amount': amount
    })

    self.last_block['index'] + 1

  @staticmethod
  def hash(block):
    block_string = json.dumps(block, sort_keys=True, default=str).encode()
    return hashlib.sha256(block_string).hexdigest()

  @property
  def last_block(self):
    return self.chain[-1]

  def proof_of_work(self, last_proof):
    proof = 0
    while self.valid_proof(last_proof, proof) is False:
      proof += 1
    return proof
  
  @staticmethod
  def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"