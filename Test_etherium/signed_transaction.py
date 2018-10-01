import os
import sys
PROGECT_ROOT = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])
if PROGECT_ROOT not in sys.path:
    sys.path.append(PROGECT_ROOT)
KEYS_ROOT = "{}/keys".format(PROGECT_ROOT)
if not os.path.exists(KEYS_ROOT):
    os.makedirs(KEYS_ROOT, mode=0o755)

import node
import pickle


CLEAR_TERMINAL = "clear"


class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CLEAR = '\033[0m'
    BOLDWHITE = '\033[1m'
    UNDERLINE = '\033[4m'


def show_accounts(exclude=0):
    accounts_template = ""
    i = 1
    for account in node.get_list_accounts():
        if i != exclude:
            accounts_template += "Account #{3}{0}{4}: {1} | Balance: {2}.\n".format(
                i,
                account,
                node.get_balance(address=account),
                bcolors.YELLOW,
                bcolors.CLEAR
            )
        else:
            accounts_template += "\n"
        i += 1
    template = """
        \r######## Accounts list ########\n
        \r{}
        \r###############################
    """.format(accounts_template)
    print(template)


def show_enter_data(data):
    for key in data:
        print("{0}: {1}".format(key.replace("_", " "), transaction[key]))


if __name__ == '__main__':
    # check_path_key()
    transaction = {}
    """
        from
    """
    os.system(CLEAR_TERMINAL)
    show_accounts()
    show_enter_data(transaction)
    number_from = 0
    while not (0 < number_from <= len(node.get_list_accounts())):
        try:
            number_from = int(input("Enter number account 'FROM' >> "))
        except ValueError:
            print("Error enter number account 'FROM'.")
            show_accounts()
    transaction["from"] = node.get_list_accounts()[number_from-1]
    balance = node.get_balance(address=transaction.get("from"))
    """
        to
    """
    os.system(CLEAR_TERMINAL)
    show_accounts(exclude=number_from)
    show_enter_data(transaction)
    number_to = 0
    while not (0 < number_to <= len(node.get_list_accounts()) and
               number_to != number_from):
        try:
            number_to = int(input("Enter number account 'TO' >> "))
        except ValueError:
            print("Error enter number account 'TO'.")
            show_accounts(exclude=number_from)
    transaction["to"] = node.get_list_accounts()[number_to-1]
    """
        money
    """
    correct = False
    while not correct:
        """
            gas price
        """
        os.system(CLEAR_TERMINAL)
        show_accounts()
        show_enter_data(transaction)
        while not transaction.get("gasPrice"):
            try:
                cost = int(input("Enter cost GAS >> "))
            except ValueError:
                print("Error enter cost GAS.")
            else:
                if (cost < balance):
                    transaction["gasPrice"] = cost
                else:
                    print("Error enter cost GAS, there is not enough money to make a transaction")
                    key = input("Re-enter? [Y/n] >> ")
                    if not key or key.lower() == "y":
                        continue
                    else:
                        exit(-1)
        if not transaction.get("gasPrice"):
            continue
        """
            count gas
        """
        os.system(CLEAR_TERMINAL)
        show_accounts()
        show_enter_data(transaction)
        while not transaction.get("gas"):
            try:
                count = int(input("Enter count GAS for transaction >> "))
            except ValueError:
                print("Error enter count GAS for transaction.")
            else:
                if (count * transaction["gasPrice"]) < balance:
                    transaction["gas"] = count
                else:
                    print("Error enter coutn GAS, there is not enough money to make a transaction")
                    key = input("Re-enter? [Y/n] >> ")
                    if not key or key.lower() == "y":
                        continue
                    else:
                        exit(-1)
        if not transaction.get("gas"):
            continue
        """
            count wer
        """
        os.system(CLEAR_TERMINAL)
        show_accounts()
        show_enter_data(transaction)
        while not transaction.get("value"):
            try:
                count = int(input("Enter count WEI for transfer >> "))
            except Exception:
                print("Error enter count WEI for transfer.")
            else:
                if (count + transaction["gas"] * transaction["gasPrice"]) <= balance:
                    transaction["value"] = count
                    correct = True
                else:
                    print("Error enter count WEI, there is not enough money to make a transaction")
                    key = input("Re-enter? [Y/n] >> ")
                    if not key or key.lower() == "y":
                        continue
                    else:
                        exit(-1)
        if not transaction.get("value"):
            continue
        os.system(CLEAR_TERMINAL)
    show_accounts()
    show_enter_data(transaction)

    transaction["nonce"] = 12
    transaction["chainId"] = '0x2a'
    """
        keys
    """
    key = node.get_private_key(name=transaction["from"][2:], password="LbvfbDbnz2Xfirb")
    s_transaction = node.sign_transaction(key=key, transaction=transaction)
    # node.node.personal.unlockAccount(transaction["from"], "XfirfNbcrbbJndthnrf1")
    result = node.send_sign_transaction(transaction=s_transaction)
    print(result)



    if PROGECT_ROOT in sys.path:
        sys.path.remove(PROGECT_ROOT)
