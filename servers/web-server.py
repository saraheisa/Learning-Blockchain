# needed because blockchain is in another directory
import sys
sys.path.insert(1, '../blockchain')
from blockchain import Blockchain

from flask import Flask, jsonify

# mining the blockchain
        
# create web app
app = Flask(__name__)

# create a blockchain
blockchain = Blockchain()

@app.route('/mineBlock', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    proof = blockchain.proof_of_work(prev_block['proof'])
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(proof, prev_hash)
    
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
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
            }
    return jsonify(response), 200

@app.route('/isValid', methods=['GET'])
def is_valid():
    response = {
            'is valid': blockchain.is_chain_valid(blockchain.chain)
            }
    return jsonify(response), 200

# running the app
app.run(host='0.0.0.0', port=5000, debug=True)
