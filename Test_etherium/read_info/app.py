#!/usr/bin/python3
from web3.auto import w3 as parity
import time


def check_connect(func):
    if parity.isConnected:
        return func
    raise ConnectionError("No connection to the blockchain node.")


@check_connect
def get_number_last_block():
    return parity.eth.blockNumber


@check_connect
def get_block_by_number(number_block):
    result = parity.eth.getBlock(number_block)
    if result:
        return result
    raise ValueError("Block with number {} not found.".format(number_block))


@check_connect
def get_block_by_hash(hash_block):
    result = parity.eth.getBlock(hash_block)
    if result:
        return result
    raise ValueError("Block with hash '{}' not found.".format(hash_block))


@check_connect
def get_transaction_by_index(number_block, index_transction):
    result = parity.eth.getTransactionFromBlock(number_block, index_transction)
    if result:
        return result
    raise ValueError(
        "Transaction with index {0} not found in block {1}.".format(
            index_transction, number_block
        )
    )


@check_connect
def get_transaction_by_hash(hash_transaction):
    result = parity.eth.getTransaction(hash_transaction)
    if result:
        return result
    raise ValueError("Transaction with hach '{}' not found.".format(hash_transaction))


def show_transaction(hash_transaction):
    transaction = get_transaction_by_hash(hash_transaction)
    isContract = False
    isCreated = False
    try:
        if parity.eth.getCode(str(transaction.get("to"))):
            isContract = True
    except Exception:
        isCreated = True
        isContract = True
    transaction_template = """
        _____________________________________________
        Hash: ......... {0}
        Block Number: . {1}
        From: ......... {2}
        To: ........... {3} {9}
        Value: ........ {4}
        Gas Limit: .... {5}
        Gas Used: ..... {6}
        Gas Prise: .... {7}
        Input Data: ... {8}
        _____________________________________________
    """.format(
        parity.toHex(transaction.get("hash")),
        transaction.get("blockNumber"),
        transaction.get("from"),
        transaction.get("to") if not isCreated else "Created {} ".format(transaction.get("to")),
        transaction.get("value"),
        transaction.get("gasLimit"),
        transaction.get("gas"),
        transaction.get("gasPrice"),
        transaction.get("input"),
        "Contract" if isContract else ""
    )
    return transaction_template


def show_block(block):
    transactions = block.get("transactions")
    transactions_template = ""
    for transaction_hash in transactions:
        transactions_template += show_transaction(transaction_hash)
    block_template = """
        \r#############  Block {0} ####################
        \rTime Stamp: . {1}
        \rHash: ....... {2}
        \rAuthor: ..... {3}
        \rSize: ....... {4}
        \rGas Limit: .. {5}
        \rGas Used: ... {6}
        \rTransactions:
            {7}
        \r##############  End {0}   ###################
    """.format(
        block.get("number"),
        time.ctime(block.get("timestamp")),
        parity.toHex(block.get("hash")),
        block.get("author"),
        block.get("size"),
        block.get("gasLimit"),
        block.get("gasUsed"),
        transactions_template
    )
    print(block_template)



if __name__ == '__main__':
    count_blocks = int(input("Enter count of blocks to read >> "))
    last_block = get_number_last_block()
    blocks = [get_block_by_number(i) for i in range(last_block, last_block-count_blocks, -1)]
    for block in blocks:
        show_block(block)


# AttributeDict(
#     {
#         'author': '0x00a0a24b9f0e5ec7aa4c7389b8302fd0123194de',
#         'difficulty': 340282366920938463463374607431768211452,
#         'extraData': HexBytes('0xd583010a068650617269747986312e32362e31826c69'),
#         'gasLimit': 7999992,
#         'gasUsed': 269562,
#         'hash': HexBytes('0x1ca032a97fa846a2ee8239d5bcc0b39eb830eed2a0c1a59efe00d146ad250491'),
#         'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080001000000000020000000000000000000000000000000000000000000'),
#         'miner': '0x00A0A24b9f0E5EC7Aa4c7389b8302fd0123194dE',
#         'number': 7635967,
#         'parentHash': HexBytes('0x2f938ced7727837bf3f0443a788d02a8f8b839c7f8feefad32685c2c6384e32c'),
#         'receiptsRoot': HexBytes('0xa9fe4d9683f16d2d10f9d50222e5d746bc4371c040c34df77599d406f4d82d0a'),
#         'sealFields': ['0x8416c79ee5', '0xb841c10a51af706cd67bb846a266b6d04c4e78111dd4f16509d0022dc00071b214ad2b29728da4c6b1523f72f1b6deb183a41ff5627f1dad1459725a84a6b811616101'],
#         'sha3Uncles': HexBytes('0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347'),
#         'signature': 'c10a51af706cd67bb846a266b6d04c4e78111dd4f16509d0022dc00071b214ad2b29728da4c6b1523f72f1b6deb183a41ff5627f1dad1459725a84a6b811616101',
#         'size': 1784,
#         'stateRoot': HexBytes('0xc6c2c481702c463dbf094cb10dc23689d4fc7cdd5ed79d3432996fb007d3fa5c'),
#         'step': '382181093',
#         'timestamp': 1528724372,
#         'totalDifficulty': 2547941806700184719151687022555858945842007621,
#         'transactions': [HexBytes('0x29bcaeb002fc0ee1a90d2dad2a693013f63f5aafd22fa3a92f4f99754549a7e2')],
#         'transactionsRoot': HexBytes('0xaf54a99847ab91aa49eff1cdcc5f511d7723c01f98afe958a32b2ec5aaa5e052'),
#         'uncles': []
#     }
# )
