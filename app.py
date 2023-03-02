from Blockchain import Blockchain
from flask import Flask, jsonify
from uuid import uuid4
import requests

# Creating the app node
app = Flask(__name__)

node_identifier = str(uuid4()).replace('-','')

# Initializing blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
  last_block = blockchain.last_block
  last_proof = last_block['proof']
  proof = blockchain.proof_of_work(last_proof)
  blockchain.new_transaction(
    sender="0",
    recipient = node_identifier,
    amount = 1,
  )
  previous_hash = blockchain.hash(last_block)
  block = blockchain.new_block(proof, previous_hash)
  response = {
    'message': 'The new block has been forged',
    'index': block['index'],
    'proof': block['proof'],
    'previous_hash' : block['previous_hash']
  }
  return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
  values = requests.get_json()
  index = blockchain.new_transaction(values['sender'], values['recipient', values['amount']])
  response = {'message': f'Transaction is scheduled to be added to Block No. {index}'}
  return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
  response = {
    'chain': blockchain.chain,
    'length': len(blockchain.chain)
  }
  return jsonify(response), 200

if __name__ == '__main__':
    app.run(host="localhost", port=3131)