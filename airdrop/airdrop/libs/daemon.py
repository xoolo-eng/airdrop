# import sha3
import json
# import ecdsa
# import pickle
import socket
import hashlib
from django.conf import settings
# from Crypto.PublicKey import RSA
# from Crypto.Random import get_random_bytes
# from Crypto.Cipher import AES, PKCS1_OAEP


TIMEOUT = 300


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


def decrypt(data, key):
    # private_key = RSA.import_key(key)
    # enc_session_key = data[:private_key.size_in_bytes()]
    # nonce = data[len(enc_session_key):len(enc_session_key)+16]
    # MAC = data[len(enc_session_key)+16:len(enc_session_key)+32]
    # ciphtext = data[private_key.size_in_bytes()+32:]
    # cipher_rsa = PKCS1_OAEP.new(private_key)
    # session_key = cipher_rsa.decrypt(enc_session_key)
    # cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    # return cipher_aes.decrypt_and_verify(ciphtext, MAC)
    return data


def connection():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect((settings.WALLET_DAEMON["ADDRESS"], settings.WALLET_DAEMON["PORT"]))
    return client_socket


def get_pivate_key():
    with open("{}/{}".format(settings.RSA_KEYS_ROOT, settings.RSA_KEYS_NAME), "rb") as priv_file:
        return priv_file.read()


def auth_server(client_socket, private_key):
    with open(
        "{}/{}.pub".format(
            settings.RSA_KEYS_ROOT,
            settings.RSA_KEYS_NAME
        ), "rb"
    ) as pub_file:
        key_data = pub_file.read()
        hash_publick_key = hashlib.sha512()
        hash_publick_key.update(
            "{}{}".format(
                key_data, settings.WALLET_DAEMON["PASSWORD"]
            ).encode("utf-8")
        )
    try:
        result = client_socket.send(
            str(hash_publick_key.hexdigest()).encode("utf-8")
        )
    except Exception:
        print("ERROR CONNECT!!!! address.py")
        print(result)
        return None
    else:
        try:
            auth_data = client_socket.recv(4096).decode("utf-8")
        except Exception as err:
            print(err)
        else:
            decrypt_data = decrypt(auth_data, private_key)
    # временный костыль, после написания функций шифрования удалить и раскоментить стрку ниже
    return decrypt_data[2:-2].encode("utf-8")
    # return decrypt_data


def get_result(**kwargs):
    # временный костыль, после написания функций шифрования удалить и раскоментить блок ниже
    kwargs["client_socket"].send(
        crypt(
            json.dumps(kwargs["request"]),
            kwargs["server_key"]
        ).encode("utf-8")
    )
    # kwargs["client_socket"].send(
    #     crypt(
    #         json.dumps(kwargs["request"]),
    #         kwargs["server_key"]
    #     )
    # )
    # временный костыль, после написания функций шифрования удалить и раскоментить блок ниже
    response = decrypt(
        kwargs["client_socket"].recv(4096).decode("utf-8"),
        kwargs["private_key"]
    )
    # response = decrypt(
    #     kwargs["client_socket"].recv(4096),
    #     kwargs["private_key"]
    # )
    return json.loads(response)


def get_data(data, name):
    client_socket = connection()
    private_key = get_pivate_key()
    server_key = auth_server(client_socket, private_key)
    args = {
        "client_socket": client_socket,
        "private_key": private_key,
        "server_key": server_key,
        "request": data
    }
    result = get_result(**args)

    if result.get("status") == "OK":
        return result.get(name)
    else:
        settings.LOG.err(
            "daemon.py -> get_data() -> {} | {}".format(
                result.get("decription"),
                data
            )
        )
        return None
