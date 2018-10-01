#! /usr/bin/python3
from web3.auto import w3 as parity


# кошелек с деньками
BIG_WALLET = parity.toChecksumAddress("0x45f34852f89671D7aD143848B2ED252a726dD081")
BIG_WALLET_PASS = "XfirfNbcrbbJndthnrf1"
# ACCOUNTS = parity.personal.listAccounts


def check_connect(func):
    if parity.isConnected:
        return func
    else:
        raise ConnectionError("No connection to the blockchain node.")


@check_connect
def get_list_accounts():
    return parity.eth.accounts


@check_connect
def create_wallet(pass_wallet):
    return parity.personal.newAccount(pass_wallet)


@check_connect
def get_balance(address=None):
    return parity.eth.getBalance(address)


@check_connect
def transfer(from_address, to_address, value):
    data = {
        "from": from_address,
        "to": to_address,
        "value": value
    }
    return parity.eth.sendTransaction(data)


@check_connect
def get_transaction(transaction_hash):
    return parity.eth.getTransaction(transaction_hash)


@check_connect
def unlock_account(address, password):
    parity.personal.unlockAccount(address, password)


if __name__ == '__main__':

    end_transactions = []
    all_transactions = []
    accounts = get_list_accounts()

    for account in accounts:
        print("Account - {}.".format(account))

    if len(accounts) < 3:
        create_wallet(input("Enter password for new account >> "))

    for account in accounts:
        print(
            "Account balance {0} is equal to {1:>18} eth".format(
                account, get_balance(account)
            )
        )

    receivers = [account for account in accounts if account != BIG_WALLET]
    for receiver in receivers:
        unlock_account(BIG_WALLET, "XfirfNbcrbbJndthnrf1")
        tx_hach = transfer(BIG_WALLET, receiver, int(input("Enter count WEI >> ")))
        print(tx_hach)
        all_transactions.append(parity.toHex(tx_hach))

    for transaction in all_transactions:
        transaction_info = get_transaction(transaction)
        if transaction_info.blockNumber:
            end_transactions.append(transaction)

    not_end_transaction = set(all_transactions) ^ set(end_transactions)
    for transaction in not_end_transaction:
        print("Not end transaction - {}".format(transaction))
