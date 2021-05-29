from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import os



#build web3
w3 = Web3(Web3.WebsocketProvider('wss://bsc-ws-node.nariox.org:443'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


print(w3.isConnected())



#load account

dev = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(dev)


#load contracts
addresses = {
  "WBNB": '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c',
  "factory": '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73',
  "router": '0x10ED43C718714eb63d5aA57B78B54704E256024E',
  "recipient": 'recipient of the profit here'
}

import requests
abi = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
abi = json.loads(abi)

contract = w3.eth.contract(address=addresses["factory"], abi=abi)



#play with contract



event_filter = contract.events.PairCreated().createFilter(fromBlock="latest")
#print(event_filter.get_new_entries())

import time

def handle_event(event):
    print(event)
    decoded_event = Web3.toHex(event)
    decoded_to_json = Web3.toJSON(decoded_event)
    print(decoded_to_json)

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(5)

def main():
    block_filter = w3.eth.filter('latest')
    log_loop(block_filter, 2)

if __name__ == '__main__':
    main()
