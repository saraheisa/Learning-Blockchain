import datetime  # used to store the creation date of each block
import hashlib
import json
import requests

from urllib.parse import urlparse

# building a blockchain
class CellCoin:
    
    def __init__ (self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.create_block(proof=1, prev_hash='0') # create the genesis block
        
    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash,
                 'transactions': self.transactions}
        self.transactions = []
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
                check_proof = True
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
                return False
            
            prev_block = block
            block_index += 1
            
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                'receiver': receiver,
                'amount': amount})
        # getting the block index for this transaction
        block_index = self.get_prev_block()['index'] + 1
        return block_index
    
    def add_node(self, address):
        # parse the address first
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        return parsed_url
    
    def replace_chain(self):
        longest_chain = self.get_longest_chain()
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
        
    def get_longest_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/getChain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
                    
        return longest_chain
        