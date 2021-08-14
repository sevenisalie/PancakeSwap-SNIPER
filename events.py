import json
from web3 import Web3
import asyncio

from ABIs import *
from ETHABIs import *

# add your blockchain connection information // Websocks dont work with infura sometimes be warned
infura_url = 'https://mainnet.infura.io/v3/e1f6b5dd7b14451484517e51f13a4674'
infura_websocket_url = "wss://mainnet.infura.io/ws/v3/e1f6b5dd7b14451484517e51f13a4674"
w3 = Web3(Web3.HTTPProvider(infura_url))

print(w3.isConnected())



#load contracts
addresses={}
addresses["WETHDAI"] = "0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11"
addresses["uniswap_router"] = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
addresses["uniswap_factory"] = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
addresses["LENDINGPOOL"] = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"


WETHDAIcontract = w3.eth.contract(address=addresses["WETHDAI"], abi=univ2PairAbi)
LENDINGPOOLcontract = w3.eth.contract(address=addresses["LENDINGPOOL"], abi=lendingPoolAbi)


# define function to handle events and print to the console
def handle_event(event):
    print(Web3.toJSON(event))
    # and whatever


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for Swap in event_filter.get_new_entries():
            handle_event(Swap)
        await asyncio.sleep(poll_interval)

async def log_loop2(tx_filter, poll_interval):
    while True:
        for txs in tx_filter.get_new_entries():
            handle_event(txs)
        await asyncio.sleep(poll_interval)

async def log_loop3():
    with websockets.connect(infura_wss) as websocket_client:
        request_data = {"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}
        await websocket_client.send(json.dumps(request_data))
    result = await websocket_client.recv()


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = LENDINGPOOLcontract.events.Deposit.createFilter(fromBlock='latest')
    #block_filter = w3.eth.filter('latest')
    #tx_filter = w3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
                # log_loop(block_filter, 2),
                #log_loop(tx_filter, 2)))
                #log_loop3()
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()