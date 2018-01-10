import threading
from pybitcoin import BitcoinPrivateKey

threads = []
found = False

def get_addr():
    priv = BitcoinPrivateKey()
    pub = priv.public_key()
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
            if(i % 10 == 0):
                with self.output_lock:
                    print("[Worker %s] i = %s" % (self.num, i))
                    print(priv.to_hex())
                    print(pub.address())

# Found the target
            if(pub.address()[1:5] == "CCNS"):
                with self.output_lock:
                    print("[Worker %s] i = %s, FIND!!" % (self.num, i))
                    print(priv.to_hex())
                    print(pub.address())
                found = True
            i = i + 1

if __name__ == "__main__":
    for k in range(5):
        t = Finder(k)
        threads.append(t)
        t.start()
