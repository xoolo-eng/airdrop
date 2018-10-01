import sys
import os
from Crypto.PublicKey import RSA


def check_path(path=None):
    if not path:
        path = "."
    else:
        if not os.path.exists:
            os.makedirs(path, mode=0o700)


def generate_keys(path, name=None):
    key = RSA.generate(2048)
    encripted_key = key.exportKey(
        pkcs=8,
        protection="scryptAndAES128-CBC"
    )
    if not name:
        name = input("Enter file names >> ")
    private_file_name = "{0}/{1}".format(path, name)
    public_file_name = private_file_name + ".pub"
    with open(private_file_name, "wb") as private:
        private.write(encripted_key)
    with open(public_file_name, "wb") as public:
        public.write(key.publickey().exportKey())


if __name__ == '__main__':
    name = None
    try:
        name = sys.argv[2]
    except IndexError:
        pass
    try:
        check_path(sys.argv[1])
    except IndexError:
        generate_keys(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), name=name)
    else:
        generate_keys(sys.argv[1], name=name)
