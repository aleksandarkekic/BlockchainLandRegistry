import datetime
import hashlib
import json
import base64
import requests
import struct

import config
from rsaKey import Encrypt
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request
from uuid import uuid4


class Blockchain:
    def __init__(self):
        # Initialize a chain which will contain blocks

        self.chain = []  # a simple list containing blovks
        self.data = []  # Create a list which contains a list of data before they
        # are added to the block.
        self.create_block(proof=1,
                          previous_hash='0')
        self.nodes = set()  # Create a set of nodes

    def create_block(self, proof, previous_hash):
        # Define block as a dictionary
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'data': self.data
                 }
        # Now we need to empty the data list
        self.data = []
        self.chain.append(block)
        self.save_blockchain()

        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1  # nonce value
        check_proof = False
        while check_proof is False:
            # Problem to be solved (this makes the minig hard)
            # operation has to be non-symetrical!!!
            hash_operation = hashlib.sha256(
                str(config.BLOCKCHAIN_PROBLEM_OPERATION_LAMBDA(previous_proof, new_proof)).encode()).hexdigest()
            # Check if first 4 characters are zeros
            if hash_operation[:len(config.LEADING_ZEROS)] == config.LEADING_ZEROS:
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash_of_block(self, block):
        # Convert a dictionary to string (JSON)
        encoded_block = json.dumps(block, sort_keys=True, default=str).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def add_data(self, parcel_info):
        # we do encryption and then base64 encoding
        self.data.append({
            'surface_area': base64.b64encode(Encrypt.encryption(parcel_info['surface_area'])),
            'sale_price': base64.b64encode(Encrypt.encryption(parcel_info['sale_price'])),
            'previous_owner': base64.b64encode(Encrypt.encryption(parcel_info['previous_owner'])),
            'current_owner': base64.b64encode(Encrypt.encryption(parcel_info['current_owner'])),
            'contract_date': base64.b64encode(Encrypt.encryption(parcel_info['contract_date'])),
            'address': base64.b64encode(Encrypt.encryption(parcel_info['address']))})
        value = f"{self.data}"
        # self.data = value[2:len(value) - 1]
        self.data = value

    def save_blockchain(self, filename='blockchain.json'):
        # save blockchain into file 'blockchain.json'
        with open(filename, 'w') as file:
            json.dump({'chain': self.chain}, file, indent=2)


# ======================= FLASK APP ===========================================

app = Flask(__name__)

node_address = str(uuid4()).replace('-', '')
blockchain = Blockchain()


@app.route('/mine-block', methods=["POST"])
def mine_block():
    # Get the previous proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash_of_block(previous_block)
    json = request.get_json()
    data_keys = ['surface_area', 'sale_price', 'previous_owner', 'current_owner', 'contract_date', 'address']
    if not all(key in json for key in data_keys):
        return 'ERROR: Some elements of the transaction JSON are missing!', 400  # Bad Request code
    blockchain.add_data(json)
    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'Congratulations! You have just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'data': block['data']
                }
    podatak = 120.5
    cyph = Encrypt.encryption(podatak)
    return jsonify(response), 200

#Getting the full Blockchain
@app.route('/get-chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)
                }
    return jsonify(response), 200


app.run(host=config.HOST, port=5002)
