from ecdsa import SECP256k1, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain
import threading
import hashlib
import sha3
import secrets

threads = []
found = False

def make_key(seed):
    secexp = randrange_from_seed__trytryagain(seed, SECP256k1.order)
    return SigningKey.from_secret_exponent(secexp, curve=SECP256k1)

def toEthAddress(pk):
    keccak = sha3.keccak_256()
    keccak.update(pk.to_string())
    address = keccak.hexdigest()[24:]
    return address

def get_addr():
    seed = hashlib.sha256(secrets.token_bytes()).digest()
    priv = make_key(seed)
    pub = priv.get_verifying_key()
    return priv, pub

class Finder(threading.Thread):
    output_lock = threading.Lock()

    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        i = 0
        global found
        while(True and not found):
            priv, pub = get_addr()

# Print result every 10 generation
            if(i % 1000 == 0):
                with self.output_lock:
                    print("[Worker %s] i = %s" % (self.num, i))
                    print("Private: "+priv.to_string().hex())
                    print("Public:  "+pub.to_string().hex())
                    print("Address: "+toEthAddress(pub))

# Found the target
            if(toEthAddress(pub)[0:4] == "cc15"):
                with self.output_lock:
                    print("[Worker %s] i = %s, FIND!!" % (self.num, i))
                    print("Private: "+priv.to_string().hex())
                    print("Public:  "+pub.to_string().hex())
                    print("Address: "+toEthAddress(pub))
                found = True
            i = i + 1

if __name__ == "__main__":
    for k in range(4):
        t = Finder(k)
        threads.append(t)
        t.start()
