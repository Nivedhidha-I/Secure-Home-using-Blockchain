# libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
# creating a Blockcain
class Blockchain:
  def __init__(self):
    self.chain = []
    self.data = []
    self.createBlock(proof = 1, prevHash = '0')
    self.nodes = set()
    
  def createBlock(self, proof, prevHash):
    # block contains - index, data, timestamp, proof, previousHash
    block = {
      'index': len(self.chain) + 1,
      'timestamp': str(datetime.datetime.now()),
      'proof': proof,
      'prevHash': prevHash,
      'data': self.data
    }
    self.data = []
    self.chain.append(block)
    return block
    
  def getPrevBlock(self):
    # returns the last mined block
    return self.chain[-1]
  
  def proofOfWork(self, prevProof):
    # 4 leading 0s should be present
    newProof = 1
    check = False
    while check == False:
      hashOperations = hashlib.sha256(str(newProof**2 - prevProof**2).encode()).hexdigest()
      if hashOperations[:4] == '0000':
        check = True
      else:
        newProof += 1
    return newProof
    
  def hash(self, block):
    # function that returns the hash of a given block
    encodedBlock = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(encodedBlock).hexdigest()
    
  def isChainValid(self, chain):
    prevBlock = chain[0]
    blockIndex = 1
    while blockIndex < len(chain):
      # previousHash equal to hash value of previous block
      block = chain[blockIndex]
      if block['prevHash'] != self.hash(prevBlock):
        return False
      # if proofOfWork is valid for each block
      prevProof = prevBlock['proof']
      proof = block['proof']
      hashOperations = hashlib.sha256(str(proof**2 - prevProof**2).encode()).hexdigest()
      if hashOperations[:4] != '0000':
        return False
      prevBlock = block
      blockIndex += 1
    return True
    
  def addData(self, deviceID, deviceType, deviceName, location, data):
    # when each data made it gets added to the datas list
    self.data.append({
      'deviceID':deviceID,
      'deviceType':deviceType,
      'deviceName': deviceName,
      'location':location,
      'data': data
    })
    return self.getPrevBlock()['index'] + 1
    
  def addNode(self, address):
    # adding a node into the blockchain
    parsedURL = urlparse(address)
    self.nodes.add(parsedURL.netloc)
    
  def replaceChain(self):
    # checking for longest chain and replacing current node chain if it isnt the longest chain
    network = self.nodes
    longestChain = None
    longestChainLength = len(self.chain)
    for node in network:
      response = requests.get(f'http://{node}/getChain')
      if response.status_code == 200:
        length = response.json()['length']
        chain = response.json()['chain']
        if length > longestChainLength and self.isChainValid(chain):
          longestChainLength = length
          longestChain = chain
    if longestChain:
      self.chain = longestChain
      return True
    return False

# creating a flask application for the blockchain
app = Flask(__name__)

# creating an address a node in port 5000
node_address = str(uuid4()).replace('-', '')

# mining the cryptocurrency
blockchain = Blockchain()
@app.route('/mineBlock', methods = ['GET'])
def mineBlock():
  prevBlock = blockchain.getPrevBlock()
  prevProof = prevBlock['proof']
  proof = blockchain.proofOfWork(prevProof)
  prevHash = blockchain.hash(prevBlock)
  block = blockchain.createBlock(proof, prevHash)
  response = {
    'message': 'congrats you have mined a block!',
    'index': block['index'],
    'timestamp': block['timestamp'],
    'proof': block['proof'],
    'prevHash': block['prevHash'],
    'data': block['data']
  }
  return jsonify(response), 200
  
# displaying the whole cryptocurrency in a website
@app.route('/getChain', methods = ['GET'])
def getChain():
  response = {
    'chain': blockchain.chain,
    'length': len(blockchain.chain)
  }
  return jsonify(response), 200
  
# checking if the cryptocurrency is valid
@app.route('/isValid', methods = ['GET'])
def isValid():
  if blockchain.isChainValid(blockchain.chain):
    response = {'message': "The blockchain is valid."}
  else:
    response = {'message': "The blockchain is invalid."}
  return jsonify(response), 200
  
# adding a new data into the blockchain
@app.route('/addData', methods = ['POST'])
def addData():
  json = request.get_json()
  dataKeys = ['deviceID', 'deviceType', 'deviceName', 'location', 'data']
  if not all (key in json for key in dataKeys):
    return 'not all data are available', 400
  index = blockchain.addData(json['deviceID'], json['deviceType'],
  json['deviceName'], json['location'], json['data'])
  response = {'message': f'This data will be added to the Block {index}.'}
  return jsonify(response), 201
  
# adding new nodes
@app.route('/connectNode', methods = ['POST'])
def connectNode():
  json = request.get_json()
  nodes = json.get('nodes')
  if nodes is None:
    return "No node", 400
  for node in nodes:
    blockchain.addNode(node)\
  response = {
    'message': 'All the nodes are now connected. The Blockchain now contains the following nodes: ',
    'totalNodes': list(blockchain.nodes)
  }
  return jsonify(response), 201
    
# replacing by longest chain if needed
@app.route('/replaceChain', methods = ['GET'])
def replaceChain():
  if blockchain.replaceChain():
    response = {
      'message': "The nodes had different chains so the chain was replaced by the longest one.",
      'newChain': blockchain.chain
    }
  else:
    response = {
      'message': "All good, the chain is the longest one.",
      'actualChain': blockchain.chain
    }
  return jsonify(response), 200
app.run(host='0.0.0.0', port=5000)
