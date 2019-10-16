# needed because blockchain is in another directory
import sys
sys.path.insert(1, '../cryptocurrency')
from cellcoin import CellCoin

import requests
import json

from uuid import uuid4 # generate random address
from flask import Flask, jsonify, request

# mining the blockchain
        
# create web app
app = Flask(__name__)

# creating an address for the node on port 5000
node_address = str(uuid4()).replace('-', '')

# create a blockchain
cellcoin = CellCoin()

@app.route('/mineBlock', methods=['GET'])
def mine_block():
    prev_block = cellcoin.get_prev_block()
    proof = cellcoin.proof_of_work(prev_block['proof'])
    prev_hash = cellcoin.hash(prev_block)
    # reward the miner by some cellcoin
    cellcoin.add_transaction(sender=node_address, receiver='celestial', amount=1)
    block = cellcoin.create_block(proof, prev_hash)
    
    response = {
            'message': 'congrats, you just mined the block',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'prrof': block['proof'],
            'previous hash': block['prev_hash'],
            'transactions': block['transactions']
            }
    return jsonify(response), 200
    
@app.route('/getChain', methods=['GET'])
def get_chain():
    response = {
            'chain': cellcoin.chain,
            'length': len(cellcoin.chain)
            }
    return jsonify(response), 200

@app.route('/isValid', methods=['GET'])
def is_valid():
    response = {
            'is valid': cellcoin.is_chain_valid(cellcoin.chain)
            }
    return jsonify(response), 200

@app.route('/transactions', methods=['POST'])
def add_transaction():
    json = request.get_json()
    # validate request body
    transactions_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transactions_keys):
        return 'Some data is missing', 400
    
    index = cellcoin.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {
            'message': f'This transaction will be added to block {index}'}
    return jsonify(response), 201

# decentralize the blockchain
@app.route('/nodes', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'no nodes!', 400
    for node in nodes:
        cellcoin.add_node(node)
    response = {
                'message': f'All the nodes are connecting',
                'total_nodes': list(cellcoin.nodes)}
    return jsonify(response), 201

@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    if cellcoin.replace_chain():
        response = {
                'message': 'The node has different chains so the chain was replaced by the longest one',
                'new_chain': cellcoin.chain
                }
    else:
        response = {
                'message': 'All Good! the chain is the longest one',
                'actual_chain': cellcoin.chain
                }
        
    return jsonify(response), 200

# running the app
app.run(host='0.0.0.0', port=5000, debug=True)
