from hashlib import sha256
import json
from time import time
import datetime

from flask import Flask, request
import requests

import socket 

app = Flask(__name__)

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.details = details
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
        
class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.client_details = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
       
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
         
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash
    
    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block
			
    def new_details(self, username, password, host_name, ip, city, location, latitude, longitude, timezone):
        username = request.form['username']
        password = request.form['password']
        host_name = socket.gethostname()
        ip = socket.gethostbyname(host_name) 
        res = requests.get('https://ipinfo.io/')
	data = res.json()

	city = data['city']

	location = data['loc'].split(',')
	latitude = location[0]
	longitude = location[1]
	timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        self.clients_details.append({
            'username': username,
            'password': password,
            'host_name':host_name,
            'ip': ip,
            'city': city,
            'location': location
            'latitude': latitude
            'longitude': longitude
            'timezone': timezone 
        })
        return self.last_block['index'] + 1
        
        
@app.route('/',methods=['GET', 'POST'])
@app.route('/login', methods=['GET','POST'])

blockchain = Blockchain()


# In[41]:



def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['username', 'password', 'host_name', 'ip', 'city', 'location', 'latitude', 'longitude', 'timezone']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['username'], values['password'], values['host_name'],values['ip'],values['city'],values['location'],values['latitude'],values['longitude'],values['timezone'])

    response = {'message': f'Details will be added to Block {index}'}
    return jsonify(response), 201


# In[45]:



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)


