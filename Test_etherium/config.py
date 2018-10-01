import os
import sys
PROGECT_ROOT = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])
if PROGECT_ROOT not in sys.path:
    sys.path.append(PROGECT_ROOT)
KEYS_ROOT = "/home/hacker/.local/share/io.parity.ethereum/keys/ethereum"
if not os.path.exists(KEYS_ROOT):
    os.makedirs(KEYS_ROOT, mode=0o755)
