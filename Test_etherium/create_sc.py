#! /usr/bin/python3
import os
import sys
PROGECT_ROOT = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])
if PROGECT_ROOT not in sys.path:
    sys.path.append(PROGECT_ROOT)
import node
import solc
import jinja2
import web3
import pickle
import requests


def get_all_transactions():
    connect = requests.post(
        "http://localhost:8545",
        json={"method": "parity_allTransactions", "params": [], "id": 1, "jsonrpc": "2.0"}
    )
    if connect.status_code == 200:
        return connect.json()["result"]
    raise Exception("Error get transactions.")


TEMPLATES = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        "{}/{}/templates".format(PROGECT_ROOT, "Test_etherium")
    )
)
DEFAULT_ADDRESS = '0x03fdae379e05340B05D942793E1Ed5d0BF197c18'
gas_price = 200000000


def deploy_contract(contract_name, **data):
    eth_test = web3.Web3(web3.EthereumTesterProvider())
    eth_test.eth.defaultAccount = eth_test.eth.accounts[0]
    try:
        template = TEMPLATES.get_template(contract_name)
        contract_code = solc.compile_source(template.render(**data))
        # contract_interface = contract_code["<stdin>:{}".format(data["name"]["class"])]

        # new_contract = eth_test.eth.contract(
        #     abi=contract_interface["abi"],
        #     bytecode=contract_interface["bin"]
        # )
        # transaction = new_contract.constructor().buildTransaction()
        # tx_hash = eth_test.eth.sendTransaction(transaction)
        # tx_receipt = eth_test.eth.waitForTransactionReceipt(tx_hash)
        # test_contract = eth_test.eth.contract(
        #     address=tx_receipt.contractAddress,
        #     abi=contract_interface["abi"]
        # )

        # balance = test_contract.functions.balanceOf(eth_test.eth.defaultAccount).call()
        # if balance:
        return contract_code
        # raise Exception("Что то пошло не так!!!")
    except Exception as e:
        print(e)
        raise Exception("Все очень плохо!!!")


def cost_contract(contract_code, **data):
    contract_interface = contract_code["<stdin>:{}".format(data["name"]["class"])]
    new_contract = node.node.eth.contract(
        abi=contract_interface["abi"],
        bytecode=contract_interface["bin"]
    )
    return new_contract.constructor().estimateGas()


def send_contract(contract_code, **data):
    contract_interface = contract_code["<stdin>:{}".format(data["name"]["class"])]
    new_contract = node.node.eth.contract(
        abi=contract_interface["abi"],
        bytecode=contract_interface["bin"]
    )
    transaction = new_contract.constructor().buildTransaction({"gasPrice": gas_price})
    node.node.personal.unlockAccount(DEFAULT_ADDRESS, "XfirfNbcrbbJndthnrf1")
    tx_hash = node.send_transaction(transaction=transaction)
    print(node.node.toHex(tx_hash))
    tx_receipt = node.node.eth.waitForTransactionReceipt(tx_hash)
    file_name = "abi/{}".format(tx_receipt.contractAddress)
    abi_file = open(file_name, "wb")
    pickle.dump(contract_interface, abi_file)
    abi_file.close()
    return tx_receipt.contractAddress


def load_contract(address):
    file_name = "abi/{}".format(address)
    abi_file = open(file_name, "rb")
    contract_interface = pickle.load(abi_file)
    abi_file.close()
    return node.node.eth.contract(
        address=address,
        abi=contract_interface["abi"]
    )


def show_api_contract(contract):
    function_template = "{}({});"
    ret_function_template = "{}({}) returns ({});"
    for function in contract.all_functions():
        signature_input = ""
        signature_output = ""
        _output = False
        data_in = function.abi["inputs"]
        data_out = function.abi["outputs"]
        for element_in in data_in:
            signature_input += "{0} {1}, ".format(element_in["type"], element_in["name"])
        signature_input = signature_input[:-2].replace("  ", "")

        if data_out:
            for element_out in data_out:
                signature_output += "{0} {1}".format(element_out["type"], element_out["name"])
            signature_output = signature_output[:-2].replace("  ", "")
        if not _output:
            print(function_template.format(function.fn_name, signature_input))
        else:
            print(ret_function_template.format(
                function.fn_name,
                signature_input,
                signature_output
            ))


if __name__ == '__main__':
    # address = "0xC37932aD2582CBE1496Cf60DACD6A4c0Ffc5686c"
    address = ""
    # addresses = [
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",

    # ]

    token = "0x8d4906259879514F5c77DD0aEdAB4347b9dD972b"
    count_tokens = 100000000000000000
    all_tokens = count_tokens * len(addresses)
    args = {
        "contract": {
            "address": token,
            "count": count_tokens,
            "owner": DEFAULT_ADDRESS
        },
        "name": {
            "class": "RemoteICO",
        },
    }

    if not address:
        code = deploy_contract("RemoteICO.sol", **args)
        result = cost_contract(code, **args)
        print("стоимость контракта", result)
        result = send_contract(code, **args)
        print("адрес контракта", result)
        address = result
    else:
        contract = load_contract(address)
        balance_transact = {
            'to': token,
            'data': '0x70a08231000000000000000000000000{}'.format(address[2:])
        }
        balance = node.node.eth.call(balance_transact)
        print("баланс контракта", node.node.toInt(balance))

        if node.node.toInt(balance) < all_tokens:
            transaction = {
                'value': 0,
                'gasPrice': gas_price,
                'chainId': None,
                'to': token,
                'data': '0xa9059cbb000000000000000000000000{0}{1:0>64}'.format(
                    address[2:],
                    node.node.toHex(all_tokens)[2:]
                )
            }
            node.node.personal.unlockAccount(DEFAULT_ADDRESS, "XfirfNbcrbbJndthnrf1")
            result = node.node.eth.sendTransaction(transaction)
            print("перевод токенов на конракт", node.node.toHex(result))
        else:
            result = contract.functions.transferFor(
                addresses
            ).estimateGas({"gasPrice": gas_price})
            node.node.personal.unlockAccount(DEFAULT_ADDRESS, "XfirfNbcrbbJndthnrf1")
            result = contract.functions.transferFor(
                addresses
            ).transact({
                "gasPrice": gas_price,
                "gas": (13177+(64*(len(addresses)+3)))*len(addresses)+result
            })
            print("ICO!!!", node.node.toHex(result))

    # transaction = {
    #     'value': 0,
    #     'gasPrice': 2000000000,
    #     'chainId': None,
    #     'to': token,
    #     'data': '0xa9059cbb000000000000000000000000{}0000000000000000000000000000000000000000000000000de0b6b3a7640000'.format(address[2:])
    # }
    # # node.node.personal.unlockAccount(DEFAULT_ADDRESS, "XfirfNbcrbbJndthnrf1")
    # result = node.node.eth.estimateGas(transaction)
    # print(result)

    # contract = load_contract(token)
    # # # # show_api_contract(contract)

    # transaction = contract.functions.trans3(
    #     "0x8d4906259879514F5c77DD0aEdAB4347b9dD972b",
    #     "0xa9059cbb000000000000000000000000f4507eBD2a2F1c80563df941eA06997605943Fd000000000000000000000000000000000000000000000000000005af3107a4000"
    # ).buildTransaction({"gas": 120000})

    # # transaction = contract.functions.trans1(
    # #     "0x8d4906259879514F5c77DD0aEdAB4347b9dD972b",
    # #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    # #     14800000
    # # ).buildTransaction({"gas": 120000})

    # # # # transaction = contract.functions.transfer(
    # # # #     "0x8d4906259879514F5c77DD0aEdAB4347b9dD972b",
    # # # #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    # # # #     14800000
    # # # # ).buildTransaction({"gas": 120000})

    # # # # transaction = contract.functions.transferFor(
    # # # #     "0x8d4906259879514F5c77DD0aEdAB4347b9dD972b",
    # # # #     ["0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    # # # #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0",
    # # # #     "0xf4507eBD2a2F1c80563df941eA06997605943Fd0"],
    # # # #     14800000
    # # # # ).buildTransaction({"gas": 520000})

    # node.node.personal.unlockAccount(DEFAULT_ADDRESS, "XfirfNbcrbbJndthnrf1")
    # result = contract.functions.transfer(
    #     address,
    #     1000000000000000000
    # ).estimateGas()
    # print("перевод токенов", result)
    # result = contract.functions.transfer(
    #     address,
    #     1000000000000000000
    # ).transact()
    # result = node.node.eth.sendTransaction(transaction)
    # print(node.node.toHex(result))

    # node.node.personal.unlockAccount(DEFAULT_ADDRESS, "XfirfNbcrbbJndthnrf1")
    # transaction2 = contract.functions.transferFrom(
    # "0x5d687875D5bed985F9131d88629681C1A28A0069",
    # "0x084a83508Ce04d844512bDDAca50C69ACce9124b",
    # 2044440
    # ).buildTransaction()
    # print(transaction2)
    # from web3.gas_strategies.time_based import glacial_gas_price_strategy
    # import pickle

    # node.node.eth.setGasPriceStrategy(glacial_gas_price_strategy)
    # print(node.node.eth.generateGasPrice())

    # transaction = contract.functions.transfer(
    # "0x084a83508Ce04d844512bDDAca50C69ACce9124b",
    # 2044440
    # ).buildTransaction({"gasPrice": 20000000000})
    # print(node.node.eth.estimateGas(transaction))
    # print(transaction)
    # print(pickle.dumps(transaction))
    # transaction['data'] = '0xa9059cbb000000000000000000000000084a83508ce04d844512bddaca50c69acce9124b'
    # node.node.personal.unlockAccount(DEFAULT_ADDRESS, "XfirfNbcrbbJndthnrf1")
    # tx_hash = node.send_transaction(transaction=transaction)
    # print(tx_hash)

    # transaction = {'value': 0, 'gas': 50859, 'chainId': None, 'gasPrice': 20000000000, 'to': '0x5d687875D5bed985F9131d88629681C1A28A0069', 'data': '0xa9059cbb000000000000000000000000084a83508ce04d844512bddaca50c69acce9124b00000000000000000000000000000000000000000000000000000000001f3218'}
    # node.node.personal.unlockAccount(DEFAULT_ADDRESS, "XfirfNbcrbbJndthnrf1")
    # tx_hash = node.send_transaction(transaction=transaction)
    # print(tx_hash)

    # node.node.personal.unlockAccount(DEFAULT_ADDRESS, "XfirfNbcrbbJndthnrf1")
    # tx_hash = contract.functions.transfer(
    #     "0x084a83508Ce04d844512bDDAca50C69ACce9124b",
    #     1000000
    # ).transact({"data": "0xce3f865f0000000000000000000000000000000000000000000000004563918244f40000"})
    # print(node.node.toHex(tx_hash))

    # balance = contract.functions.balanceOf(DEFAULT_ADDRESS).call()
    # print(balance)
    # balance = contract.functions.balanceOf("0x084a83508Ce04d844512bDDAca50C69ACce9124b").call()
    # print(balance)
    # print(get_all_transactions())
