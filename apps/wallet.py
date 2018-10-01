import json
import socket
from libs.log import Log
from select import select
import fcntl
import hashlib
import os
from Crypto.PublicKey import RSA
# from Crypto.Random import get_random_bytes
# from Crypto.Cipher import AES, PKCS1_OAEP
import sha3
import ecdsa
import pickle
from libs import node
import web3
import solc
import threading
import jinja2
# import Process, Queue
# from datetime import datetime.


log = Log(path_file="wallet.log")


class Config():

    _data = {}

    def __init__(self, **kwargs):
        """
            Can take the initialization path to the configuration file
            and/or the dictionary with the default settings
        """
        if kwargs.get("file"):
            with open(kwargs["file"], "r") as file:
                try:
                    self._data = json.loads(file.read())
                except json.decoder.JSONDecodeError:
                    log.err("Error in config file: {}".format(kwargs["file"]))
        if kwargs.get("default"):
            for key in kwargs["default"]:
                self._data[key] = kwargs["default"][key]
        # print(self._data)

    def __getattr__(self, name):
        return self._data[name]

    def __call__(self, name, value):
        self._data[name] = value

    def __str__(self):
        return "{}".format(self._data)


def load_contract(address, config):
    """
    загрузка смартконтракта используя abi контракта
    """
    contract_interface = None
    with open("{}/{}".format(config.abi, address), "rb") as abi_file:
        contract_interface = pickle.load(abi_file)
    return config.parity.eth.contract(
        address=address,
        abi=contract_interface["abi"]
    )


def get_key(name):
    with open("{}/{}".fomrat(kwargs["config"].wallet_keys, name), "rb") as key_file:
        key = pickle.load(key_file)
        return key.hexdigest()
    log.err("get_key() -> {}".format("Error open key file"))
    return None


def create(**kwargs):
    keccak = sha3.keccak_256()
    priv = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    keccak.update(priv.get_verifying_key().to_string())
    address = keccak.hexdigest()[24:]
    key_file = open("{}/{}.key".format(kwargs["config"].wallet_keys, kwargs["order"]), "wb")
    pickle.dump(priv, key_file)
    key_file.close()
    address = kwargs["config"].parity.toChecksumAddress("0x{}".format(address))[:-41:-1][::-1]
    return {"status": "OK", "address": address}


def balance(**kwargs):
    kwargs["address"] = kwargs["config"].parity.toChecksumAddress(
        "0x{}".format(kwargs["address"][:-41:-1][::-1])
    )
    try:
        result = node.get_balance(
            connection=kwargs["config"].parity,
            address=kwargs["address"]
        )
    except ValueError as err:
        return {"status": "ERR", "description": err}
    else:
        return {"status": "OK", "balance": result}


def token(**kwargs):

    def token_balance(address, inspect, result, parity):
        transaction = {
            "to": inspect,
            "data": "0x70a08231000000000000000000000000{0}".format(address[:-41:-1][::-1])
        }
        try:
            result.append(
                parity.toInt(parity.eth.call(transaction))
            )
        except ValueError:
            pass

    kwargs["address"] = kwargs["config"].parity.toChecksumAddress(
        "0x{}".format(kwargs["address"][:-41:-1][::-1])
    )
    kwargs["contract"] = kwargs["config"].parity.toChecksumAddress(
        "0x{}".format(kwargs["contract"][:-41:-1][::-1])
    )
    # balance_contract = load_contract(
    #     kwargs["config"].balance_contract,
    #     kwargs["config"]
    # )
    result = []
    thread = threading.Thread(
        target=token_balance,
        args=[kwargs["address"],
              kwargs["contract"], result, kwargs["config"].parity]
    )
    thread.start()
    thread.join(3)
    if thread.is_alive():
        thread.terminate()
    if result:
        return {"status": "OK", "balance": result[0]}
    else:
        return {
            "status": "ERR",
            "description": "Request to be completed. \
            A smart contract must comply with the ERCS20 standard"
        }


def cost(**kwargs):
    """
    стоимость услуги, расчитывается с разбивкой заказа на несколько итераций
    kwargs["config"] - конфигурация
    kwargs["count"][0] - общее количество адресов
    kwargs["count"][1] - количество адресов за одну транзакцию (задается в настройках сайта)
    kwargs["call"] - стоимость вызова метода массового перевода (задается в настройках сайта)
    """
    conf = kwargs["config"]
    iterations = kwargs["count"][0] // kwargs["count"][1]
    sizes_arrays = kwargs["count"][1] * iterations
    staff = (kwargs["count"][0] - (kwargs["count"][1] * iterations))
    if staff:
        sizes_arrays.append(staff)
    costs_remote_call = [conf.remote_transfer * (64 * (size_array+3))
                         for size_array in sizes_arrays]
    result = (
        conf.transfer +
        (sum(costs_remote_call)) *
        kwargs["count"][0] + kwargs["call"]
    ) * conf.gas_price
    if not kwargs.get("work_contract"):
        result += conf.deploy * conf.gas_price
    return {"status": "OK", "cost": result}


def contract(**kwargs):
    """
    проверка адреса на наличие контракта
    """
    kwargs["contract"] = kwargs["config"].parity.toChecksumAddress(
        "0x{}".format(kwargs["contract"][:-41:-1][::-1])
    )
    try:
        kwargs["config"].parity.eth.getCode(kwargs["contract"])
    except web3.exceptions.InvalidAddress:
        return {"status": "OK", "contract": False}
    else:
        return {"status": "OK", "contract": True}


def deploy(**kwargs):
    """
    размещение контракта
    """
    args = {
        "name": kwargs.get("name") or "RemoteICO",
        "contract": {
            "address": "0x{}".format(kwargs["address"])[:-41:-1][::-1],
            "contract": "0x{}".format(kwargs["contract"])[:-41:-1][::-1],
            "amount": kwargs["amount"]
        }
    }
    try:
        work_contract = kwargs["config"].templates.get_template(
            "{}.sol".format(args["name"])
        )
    except Exception as err:
        return {
            "status": "ERR",
            "description": "{}: {}".format(
                "Open templates",
                str(err)
            )
        }
    try:
        code_contract = solc.compile_source(work_contract.render(**args))
    except Exception as err:
        return {
            "status": "ERR",
            "description": "{}: {}".format(
                "Compile contract",
                str(err)
            )
        }
    interface_contract = code_contract["<stdin>:{}".format(args["name"])]
    abi_file = open(
        "{}/{}.abi".format(
            kwargs["config"].abi,
            kwargs["order"]
        ), "wb"
    )
    pickle.dump(interface_contract, abi_file)
    abi_file.close()
    new_contract = kwargs["parity"].eth.contract(
        abi=interface_contract["abi"],
        bytecode=interface_contract["bin"]
    )
    transaction = new_contract.conctructor().buildTransaction(
        {"gasPrice": kwargs.get("gasPrice") or kwargs["config"].gasPrice}
    )
    key = get_key(kwargs["order"])
    if key:
        pass
    else:
        return {
            "status": "ERR",
            "description": "{} {}".format(
                "Not open key file for order",
                kwargs["order"]
            )
        }
    try:
        s_transaction = node.sign_transaction(
            connection=kwargs["config"].parity,
            key=key,
            transaction=transaction
        )
    except ValueError as err:
        return {
            "status": "ERR",
            "description": "{} {}".format(
                err,
                kwargs["order"]
            )
        }
    try:
        tx_hash = node.send_sign_transaction(
            connection=kwargs["config"].parity,
            transaction=s_transaction
        )
    except ValueError as err:
        return {
            "status": "ERR",
            "description": "{} {}".format(
                err,
                kwargs["order"]
            )
        }
    """
    олжидание поподания кранзакции в блок.
    переделать в асинхронном режиме для снятия блокироваки
    """
    tx_receipt = None
    while not tx_receipt:
        tx_receipt = kwargs["config"].parity.eth.getTransactionReceipt(tx_hash)
    return {"staus": "OK", "tx_receipt": tx_receipt}


def task(**kwargs):
    pass


def crypt(data, key):
    # client_public_key = RSA.import_key(key)
    # session_key = get_random_bytes(16)
    # cipher_rsa = PKCS1_OAEP.new(client_public_key)
    # result = cipher_rsa.encrypt(session_key)
    # cipher_aes = AES.new(session_key, AES.MODE_EAX)
    # ciphtext, MAC = cipher_aes.encrypt_and_digest(data)
    # result += cipher_aes.nonce + MAC + ciphtext
    # return result
    return data


def decrypt(data, private_key):
    # enc_seccion_key = data[:private_key.size_in_bytes()]
    # nonce = data[len(enc_seccion_key):16]
    # MAC = data[len(enc_seccion_key)+16:16]
    # ciphtext = data[len(enc_seccion_key)+16+16:]
    # cipher_rsa = PKCS1_OAEP.new(private_key)
    # session_key = cipher_rsa.decrypt(enc_seccion_key)
    # cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    # return cipher_aes.decrypt_and_verify(ciphtext, MAC)
    return data


def authorization(data, config):
    """
        user authorization, key and password verification
    """
    result = {"key": None, "data": None}
    keys = os.listdir(config.client_keys)
    try:
        for key in keys:
            with open("{0}/{1}".format(config.client_keys, key), "rb") as key_file:
                data_key = key_file.read()
                hash_key = hashlib.sha512()
                hash_key.update("{}{}".format(data_key, config.password).encode("utf-8"))
                if data == hash_key.hexdigest():
                    result["key"] = data_key
                    result["data"] = str(crypt(data_key, open(
                        config.public_key, "rb").read()))  # tmp (str)
                    break
    except Exception as err:
        log.err("def authorization(): {}".format(err))
    return result


def process_request(data, key, config):
    """
        message decryption, processing, response generation
    """
    commands = [
        "create",
        "balance",
        "token",
        "cost",
        "contract"
    ]

    private_key = RSA.import_key(open(config.private_key, "rb").read())
    decrypt_data = decrypt(data, private_key)
    request = json.loads(decrypt_data)
    response = {}
    if request.get("command"):
        if request["command"] in commands:
            response = eval(
                "{0}(**{1}, config=config)".format(request["command"], request)
            )
        else:
            response["starus"] = "ERR"
            response["description"] = "Command not found"
    else:
        response["starus"] = "ERR"
        response["description"] = "No command specified"
    response = json.dumps(response)
    return crypt(response, key)


def wallet(config_file=None, default_config=None):
    config = Config(file=config_file, default=default_config)
    templates = jinja2.Environment(
        loader=jinja2.FileSystemLoader(config.templates_path)
    )
    config("templates", templates)
    config(
        "parity",  web3.Web3(
            web3.HTTPProvider(
                "http://{}:{}".format(
                    config.parity_host,
                    config.parity_port
                )
            )
        )
    )
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((config.address, config.port))
    server_socket.listen(config.queue_size or 200)
    fcntl.fcntl(server_socket, fcntl.F_SETFL, os.O_NONBLOCK)
    sockets = set()
    clients = {}
    sockets.add(server_socket)
    stop = False
    while not stop:
        try:
            read_fd, write_fd, error_fd = select(sockets, sockets, sockets)
            for sock in read_fd:
                if sock is server_socket:
                    client, address = server_socket.accept()
                    fcntl.fcntl(client, fcntl.F_SETFL, os.O_NONBLOCK)
                    sockets.add(client)
                    log.info("Connect client with address {}".format(address))
                else:
                    if sock.fileno() in clients:
                        if not clients[sock.fileno()]["data"]:
                            clients[sock.fileno()]["data"] = process_request(
                                sock.recv(4096).decode("utf-8"),
                                clients[sock.fileno()]["key"], config
                            )
                            clients[sock.fileno()]["connect"] = "END"
                    else:
                        result = authorization(sock.recv(4096).decode("utf-8"), config)
                        if result:
                            clients[sock.fileno()] = result
            for sock in write_fd:
                if sock.fileno() in clients:
                    if clients[sock.fileno()]["data"]:
                        result = sock.send(clients[sock.fileno()]["data"].encode("utf-8"))
                        clients[sock.fileno()]["data"] = None
                        if not result:
                            log.err("Size sender data = 0")
                    if clients[sock.fileno()].get("connect") == "END":
                        del clients[sock.fileno()]
                        sockets.remove(sock)
                        sock.close()
            for sock in error_fd:
                del client[sock.fileno()]
                sockets.remove(sock)
                sock.close()
        except Exception as e:
            log.err("{}".format(e))


if __name__ == '__main__':
    wallet(config_file="/home/hacker/Projects/Python/airdrop-saas/apps/wallet.conf")
