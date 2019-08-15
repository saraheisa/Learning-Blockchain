import datetime  # used to store the creation date of each block
import hashlib
import json
from flask import Flask, jsonify

# building a blockchain
class Blockchain:
    
    def __init__ (self):
        self.chain = []
        self.create_block(proof=1, prev_hash='0') # create the genesis block
        
    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash}
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = true
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        # convert dict to str and encode it
        # didn't use str() because the block will be stored as json later
        encoded_block = json.dumps(block, sort_keys=True).encode() 
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            
            # 1st check: checks if the previous hash is correct
            if block['prev_hash'] != self.hash(prev_block):
                return False
            
            # 2nd check: if the hash starts with 4 zeros
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return false
            
            prev_block = block
            block_index += 1
            
        return true
    