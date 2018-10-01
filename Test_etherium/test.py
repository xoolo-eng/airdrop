# import json
# import web3

# from web3 import Web3
import web3
from solc import compile_source
from web3.contract import ConciseContract


w3 = web3.Web3(web3.Web3.HTTPProvider('http://192.168.1.107:8545'))
contract_code = open("CryptoFund.sol", "r").read()

w3.personal.unlockAccount(
    "0x03fdae379e05340B05D942793E1Ed5d0BF197c18", "XfirfNbcrbbJndthnrf1")

compled_sol = compile_source(contract_code)
contract_interface = compled_sol["<stdin>:CryptoFundToken"]
print(contract_interface['abi'])
Contract=w3.eth.contract(
    abi=contract_interface["abi"],
    bytecode=contract_interface["bin"]
)
tx_hash = Contract.constructor(7955555).transact()
print("################################################33")
print(w3.toHex(tx_hash))
print("################################################33")
tx_receipt=w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)

# abi = [{'constant': True, 'inputs': [], 'name': 'get_value1', 'outputs': [{'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'get_value2', 'outputs': [{'name': '', 'type': 'uint256'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'a', 'type': 'uint256'}], 'name': 'add_value', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}]
# greeter = w3.eth.contract(
#     address='0x9b6A55Cc3EaC9cA01Bc604f344a45DC1fe892652',
#     abi=abi
# )
# # greeter.functions.add_value(2).call()
# # tx_hash = greeter.functions.add_value(2).transact()
# # print(w3.toHex(tx_hash))
# result = greeter.functions.get_value1().call()
# print(result)
# result = greeter.functions.get_value2().call()
# print(result)

# for function in greeter.all_functions():
#     print(function.fn_name)
#     print(function.factory)
#     print(function.contract_abi)
# print(greeter.all_functions())
# count_gas = greeter.functions.greet().estimateGas()
# print(count_gas)
# print(
#     "Default contract grreting: {}".format(
#         greeter.functions.greet().call()
#     )
# )
# count_gas = greeter.functions.setGreeting("Nihao").estimateGas()
# print(count_gas)
# print("Setting the greeting to Hihao...")
# print("################################################33")
# balance = greeter.functions.balance("0x5d687875D5bed985F9131d88629681C1A28A0069", "0x45f34852f89671D7aD143848B2ED252a726dD081").call()
# print(balance)
# tx_receipt_new = w3.eth.waitForTransactionReceipt(tx_hash)
# print(tx_hash)
# count_gas = greeter.functions.greet().estimateGas()
# print(count_gas)
# print(
#     "Update contract greeting: {}".format(
#         greeter.functions.greet().call()
#     )
# )
# reader = ConciseContract(greeter)
# assert reader.greet() == "Nihao"


# ['__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_encode_transaction_data', '_return_data_normalizers', '_set_function_info', 'abi', 'address', 'arguments', 'buildTransaction', 'call', 'contract_abi', 'estimateGas', 'factory', 'fn_name', 'function_identifier', 'transact', 'transaction', 'web3']
