from web3.auto import w3 as node
from .decorators import connection
# import ecdsa
# import os
# import sys
# PROGECT_ROOT = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])
# if PROGECT_ROOT not in sys.path:
    # sys.path.append(PROGECT_ROOT)

# import config
# import pickle


@connection(node)
def get_list_accounts(**kwargs):
    """
        Получить список аккаунтов на локальном хосте.
        Принимает именованные параметры:
        connection=w3 - объект подключения к хосту,
        является не обязательным параметром, по умолчанию
        используется подключение к локальному хосту.
        Бровает исключения:
        ValueError
    """
    try:
        return kwargs["connection"].eth.accounts
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection'.",
            "get_list_accounts(connection=w3).",
            "default use decorator.",
            "@connection(w3)",
            "get_list_accounts()"
        )


@connection(node)
def create_wallet(**kwargs):
    """
        Создание кошелька на текущей ноде.
        Принимает именованные параметры:
        password='You_new_password' - пароль для кощелька.
        connection=w3 - объект подключения к хосту,
        является не обязательным параметром, по умолчанию
        используется подключение к локальному хосту.
        Бровает исключения:
        ValueError
    """
    try:
        return kwargs["connection"].personal.newAccount(
            kwargs["password"]
        )
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection' and 'password'.",
            "create_wallet(connection=w3, password='Yor_new_password').",
            "default use decorator.",
            "@connection(w3)",
            "create_wallet(password='Yor_new_password')"
        )


@connection(node)
def get_balance(**kwargs):
    """
        Получить баланс на указанном адресе.
        Принимает именованные параметры:
        address=address - адрес аккаунта.
        connection=w3 - объект подключения к хосту,
        является не обязательным параметром, по умолчанию
        используется подключение к локальному хосту.
        Бровает исключения:
        ValueError
    """
    try:
        return kwargs["connection"].eth.getBalance(
            kwargs["connection"].toChecksumAddress(
                str(kwargs["address"])
            )
        )
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection' and 'address'.",
            "get_balance(connection=w3, address=<address_account>).",
            "default use decorator.",
            "@connection(w3)",
            "get_balance(address=<address_account>)"
        )
    except web3.exceptions.InvalidAddress:
        raise ValueError("Address '{}' not found.".format(kwargs["address"]))


@connection(node)
def get_number_last_block(**kwargs):
    """
        Получить номер последнего блока.
        Принимает именованные параметры:
        connection=w3 - объект подключения к хосту,
        является не обязательным параметром, по умолчанию
        используется подключение к локальному хосту.
        Бровает исключения:
        ValueError
    """
    try:
        return kwargs["connection"].eth.blockNumber
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection'.",
            "get_number_last_block(connection=w3).",
            "default use decorator.",
            "@connection(w3)",
            "get_number_last_block()"
        )


@connection(node)
def get_block_by_number(**kwargs):
    """
        Получит блок по его номеру.
        Принимает именованные параметры:
        number=number_block - номер запрашиваемого блока.
        connection=w3 - объект подключения к хосту,
        является не обязательным параметром, по умолчанию
        используется подключение к локальному хосту.
        Бровает исключения:
        ValueError
    """
    try:
        result = kwargs["connection"].eth.getBlock(
            kwargs["number"]
        )
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection' and 'number'.",
            "get_block_by_number(connection=w3, number=<number_block>).",
            "default use decorator.",
            "@connection(w3)",
            "get_block_by_number(number=<number_block>)"
        )
    else:
        if result:
            return result
        raise ValueError("Block with number {} not found.".format(kwargs["number"]))


@connection(node)
def get_block_by_hash(**kwargs):
    """
        Получит блок по его хешу.
        Принимает именованные параметры:
        hash=hash_block- хещ блока.
        connection=w3 - объект подключения к хосту,
        является не обязательным параметром, по умолчанию
        используется подключение к локальному хосту.
        Бровает исключения:
        ValueError
    """
    try:
        result = kwargs["connection"].eth.getBlock(
            kwargs["hash"]
        )
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection' and 'hash'.",
            "get_block_by_hash(connection=w3, hash=<hash_block>).",
            "default use decorator.",
            "@connection(w3)",
            "get_block_by_hash(hash=<hash_block>)"
        )
    else:
        if result:
            return result
        raise ValueError("Block with hash '{}' not found.".format(kwargs["hash"]))


@connection(node)
def get_transaction_by_index(**kwargs):
    """
        Получить транзакцию по известному индексу
        в указанном блоке.
        Принимает именованные параметы:
        number=number_block - номер блока.
        index=index_transaction - индекс транзакции
        (порядковый номер -1).
        connection=w3 - объект подключения к хосту,
        является не обязательным параметром, по умолчанию
        используется подключение к локальному хосту.
        Бровает исключения:
        ValueError
    """
    try:
        result = kwargs["connection"].eth.getTransactionFromBlock(
            kwargs["number"], kwargs["index"]
        )
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection' and 'hash'.",
            "get_transaction_by_index(connection=w3, number=<number_block>, index=<index_transaction>).",
            "default use decorator.",
            "@connection(w3)",
            "get_transaction_by_index(number=<number_block>, index=<index_transaction>)"
        )
    else:
        if result:
            return result
        raise ValueError(
            "Transaction with index {0} not found in block {1}.".format(
                kwargs["index"], kwargs["number"]
            )
        )


@connection(node)
def get_transaction_by_hash(**kwargs):
    """
        Получить транзакцию по ее хешу.
        Принимает именованные параметры:
        hash=hash_transaction - хеш транзакции.
        connection=w3 - объект подключения к хосту,
        является не обязательным параметром, по умолчанию
        используется подключение к локальному хосту.
        Бровает исключения:
        ValueError
    """
    try:
        result = kwargs["connection"].eth.getTransaction(
            kwargs["hash"]
        )
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection' and 'hash'.",
            "get_transaction_by_hash(connection=w3, hash=<hash_transaction>).",
            "default use decorator.",
            "@connection(w3)",
            "get_transaction_by_hash(hash=<hash_transaction>)"
        )
    else:
        if result:
            return result
        raise ValueError("Transaction with hash '{}' not found.".format(kwargs["hash"]))


@connection(node)
def get_private_key(**kwargs):
    """
        get private key
    """
    try:
        file = None
        for element in os.listdir(config.KEYS_ROOT):
            if os.path.isfile("{0}/{1}".format(config.KEYS_ROOT, element)):
                try:
                    file = open("{0}/{1}".format(config.KEYS_ROOT, element), "r").read()
                except Exception as e:
                    print(e)
                else:
                    if kwargs["name"] not in file:
                        break

        try:
            private_key = kwargs["connection"].eth.account.decrypt(file, kwargs["password"])
        except ValueError:
            raise ValueError("Error enter password.")
        else:
            return private_key
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection' and 'name' and 'password'.",
            "get_private_key(connection=w3, name=<name_account>, password=<password>).",
            "default use decorator.",
            "@connection(w3)",
            "get_private_key(name=<name_account>, password=<password>)"
        )


@connection(node)
def sign_transaction(**kwargs):
    try:
        return kwargs["connection"].eth.account.signTransaction(
            kwargs["transaction"], kwargs["key"]
        )
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection' and 'transaction' and 'key'.",
            "sign_transaction(connection=w3, transaction=<transaction>, key=<Your_key_key>).",
            "default use decorator.",
            "@connection(w3)",
            "sign_transaction(transaction=<hashtransaction>, key=<Your_key_key>)"
        )
    except TypeError:
        raise ValueError("Error enter private key.")


@connection(node)
def send_sign_transaction(**kwargs):
    try:
        return kwargs["connection"].eth.sendRawTransaction(kwargs["transaction"].rawTransaction)
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection' and 'transaction'.",
            "send_sign_transaction(connection=w3, transaction=<transaction>).",
            "default use decorator.",
            "@connection(w3)",
            "send_sign_transaction(transaction=<transaction>)"
        )
    except Exception as e:
        print(e)


@connection(node)
def send_transaction(**kwargs):
    try:
        result = kwargs["connection"].eth.sendTransaction(
            kwargs["transaction"]
        )
    except KeyError:
        raise ValueError(
            "Expected argument of 'connection' and 'transaction'.",
            "send_transaction(connection=w3, transaction=<transaction>).",
            "default use decorator.",
            "@connection(w3)",
            "send_transaction(transaction=<transaction>)"
        )
    else:
        if result:
            return result
        raise ValueError("Error send transaction {}.".format(kwargs["transaction"]))


# @connection(node)
# def sign_transaction(**kwargs):
#     """

#     """
#     try:
#         pass
#     except KeyError:
#         pass


# @connection(node)
# def sign_send_transaction(**kwargs):
#     pass


# @connection(node)
# def send_transaction(**kwargs):
#     try:
#         return kwargs["connection"].eth.sendTransaction(kwargs["transaction"])
#     except KeyError:
#         raise ValueError(
#             "Expected argument of 'connection' and 'transaction'.",
#             "send_transaction(connection=w3, transaction=<transaction>).",
#             "default use decorator.",
#             "@connection(w3)",
#             "send_transaction(transaction=<transaction>)"
#         )


# @connection(node)
# def send_signed_transaction(**kwargs):
#     try:
#         return kwargs["connection"].eth.sendRawTransaction(kwargs["transaction"])
#     except KeyError:
#         raise ValueError(
#             "Expected argument of 'connection' and 'transaction'.",
#             "send_signed_transaction(connection=w3, transaction=<sign_transaction>).",
#             "default use decorator.",
#             "@connection(w3)",
#             "send_signed_transaction(transaction=<sign_transaction>)"
#         )







# def generation_pp_key(name):
#     """
#         Generate private and public key,
#         and save in file.
#     """
#     private_path = "{0}/private".format(config.KEYS_ROOT)
#     public_path = "{0}/public".format(config.KEYS_ROOT)

#     if not os.path.exists(private_path):
#         os.mkdir(private_path, mode=0o700)
#     if not os.path.exists(public_path):
#         os.mkdir(public_path, mode=0o700)

#     private_name = "{0}/{1}".format(private_path, name)
#     public_name = "{0}/{1}".format(public_path, name)

#     private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
#     public_key = private_key.get_verifying_key()

#     private_file = open(private_name, "wb")
#     pickle.dump(private_key, private_file)
#     private_file.close()

#     public_file = open(public_name, "wb")
#     pickle.dump(public_key, public_file)
#     public_file.close()


# def get_private_key(name):
#     """
#         Get private key.
#     """
#     private_name = "{0}/private/{1}".format(config.KEYS_ROOT, name)
#     if not os.access(private_name, os.F_OK):
#         raise ValueError("Keys not found.")
#     private_file = open(private_name, "rb")
#     private_key = pickle.load(private_file)
#     return private_key


# def get_public_key(name):
#     """
#         Get public key.
#     """ 
#     public_name = "{0}/public/{1}".format(config.KEYS_ROOT, name)
#     if not os.access(public_name, os.F_OK):
#         raise ValueError("Keys not found.")
#     public_file = open(public_name, "rb")
#     public_key = pickle.load(public_file)
#     return public_key
