from ecdsa import SECP256k1, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain
import hashlib
import sha3

def make_key(seed):
  secexp = randrange_from_seed__trytryagain(seed, SECP256k1.order)
  return SigningKey.from_secret_exponent(secexp, curve=SECP256k1)

def toEthAddress(pk):
	keccak = sha3.keccak_256()
	keccak.update(pk.to_string())
	address = keccak.hexdigest()[24:]
	return address

seed = hashlib.sha256("ABCDEF12".encode('utf-8')).digest()
priv = make_key(seed)
pub = priv.get_verifying_key()

print("Private: "+priv.to_string().hex())
print("Public:  "+pub.to_string().hex())
print("Address: "+toEthAddress(pub))