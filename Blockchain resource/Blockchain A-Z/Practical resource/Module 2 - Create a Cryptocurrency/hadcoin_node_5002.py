# Module 1 - Create a Cryptocurrency

# To be installed:
# Flask and postman
# requests==2.18.4: pip install requests==2.18.4
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
# uuid4 function generates a random unique address


# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []  # list containing TRX before they are added to the block
        self.create_block(proof=1,
                          previous_hash='0')
        self.nodes = set()
        # initializing a (genesis block) blockhain (keep proof of 1 as standard practise , previous hash of string 0
        # in quotes because sha256 needs inside quotes.

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions,
                 }
        self.transactions = []  # Once TRX is added to the block, the list becomes empty
        self.chain.append(block)  # append the block to the self.chain list
        return block

    def get_previous_block(self):
        return self.chain[-1]  # -1 gives the last index of the chain.

        # problem should be hard to find(get)(not to lose its value), but easy to verify. End of function we return
        # proof of work previous proof is element of the problem that miners need to solve the problem we increment
        # new_proof by 1 , and the loop increments by 1 till find the right proof. once solution of problem is found,
        # we change check_proof to TRUE. try, fail , increment new proof ---> try, fail, increment new proof. more
        # leading 00000, harder it is to mine for miners.

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(
                new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            # str returns '5', encode returns b'5' (
            # adds b infront of 5 for format purpose for sha256 to accept this operation).
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):  # takes a block and returns the hash
        encoded_block = json.dumps(block,
                                   sort_keys=True).encode()
        # encoding block to the right format so get accepted by sha256
        return hashlib.sha256(encoded_block).hexdigest()

    # check previous hash of each block is equal to the hash of its 'previous block'
    # check proof of each work is valid according to our proof of work function.
    # chain : we gon take the chain and iterate on each of the block of the chain and make our 2 checks for each blocks.
    def is_chain_valid(self, chain):
        previous_block = chain[0]  # get first block of the chain
        block_index = 1  # looping variable, each block has index key as shown in Dictionary.
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(
                    previous_block):
                # if previous hash of our current block is different then the hash of our previous block
                return False
            previous_proof = previous_block['proof']  # get proof key of previous block
            proof = block['proof']  # get proof of current block
            hash_operation = hashlib.sha256(str(proof ** 2 - proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block  # Current block becomes the previous_block in the next iteration
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)  # get the netloc
        self.nodes.add(parsed_url.netloc)  # this gets just the url ('127.0.0.1:5000'), to help us find the longest node
        # any url in node = parsed_url.netloc

    def replace_chain(self):
        network = self.nodes    # network containing all the nodes
        longest_chain = None        # suppose to replace the node with the longest chain,
        max_length = len(self.chain)    # variable to find the longest chain, by comparing the length of all the chains
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:   # 200 means request was received and understood and is being processed
                length = response.json()['length']  # length = length of the chain
                chain = response.json()['chain']    # replace the chain if the length is not the largest one
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
            if longest_chain:  # if chain was replaced than replace the chain in the blockchain else return false
                self.chain = longest_chain
                return True
            return False


# Part 2 - Mining our Blockchain


# Creating a Flask based Web App
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-','')

# Creating a Blockchain
blockchain = Blockchain()  # instance of the class


# Mining a new Block
@app.route('/mine_block', methods=['GET'])  # decorator required to call the mineblock function to mine the block
def mine_block():  # no args, all params can be extracted from blockchain instance
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)  # Param: proof_of_work(self, previous_proof)
    previous_hash = blockchain.hash(previous_block)  # Param: Previous_hash extracted from "hash(self,block)"
    blockchain.add_transaction(sender=node_address, recevier='Kirill', amount=10)
    block = blockchain.create_block(proof, previous_hash)  # Param: create_block(self, proof, previous_hash)
    response = {'message': "Congrats, you just mined a block!",
                'index': block['index'],
                'timestamp': block["timestamp"],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']
                }
    return jsonify(response), 200  # jsonify & http status code.


# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)
                }  # Chain of our blockchain and length of chain
    return jsonify(response), 200


# Check if blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': "The blockchain is valid",
                    'length': len(blockchain.chain)
                    }
    else:
        response = {'message': "The blockchain is NOT valid",
                    'length': len(blockchain.chain)
                    }
    return jsonify(response), 200

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()  # get json file posted in postman
    transaction_keys = ['sender','receiver','amount']  # if a trx is missing any keys, warning will be issued
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

# Part 3 = Decentralizing our blockchain

# Connecting new nodes
@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No nodes", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': "All the nodes are now connected. The Hadcoin Blockchain now contains the following nodes",
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': "The nodes had different chains so the chain was replaced by the longest one",
                    'new_chain': blockchain.chain
                    }
    else:
        response = {'message': "All good, the chain is the largest one",
                    'actual_chain': blockchain.chain
                    }
    return jsonify(response), 200


# Running the app


app.run(host="0.0.0.0", port=5002)
