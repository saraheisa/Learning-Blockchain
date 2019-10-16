# needed because blockchain is in another directory
import sys
sys.path.insert(1, '../cryptocurrency')
from cellcoin import CellCoin

import requests

from uuid import uuid4 # generate random address
from flask import Flask, jsonify

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
    block = cellcoin.create_block(proof, prev_hash)
    
    response = {
            'message': 'congrats, you just mined the block',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'prrof': block['proof'],
            'previous hash': block['prev_hash']
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

# running the app
app.run(host='0.0.0.0', port=5000, debug=True)
