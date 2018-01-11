from ecdsa import SECP256k1, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain
import hashlib
import sha3
import secrets

def make_key(seed):
  secexp = randrange_from_seed__trytryagain(seed, SECP256k1.order)
  return SigningKey.from_secret_exponent(secexp, curve=SECP256k1)

def toEthAddress(pk):
	keccak = sha3.keccak_256()
	keccak.update(pk.to_string())
	address = keccak.hexdigest()[24:]
	return address

desired_str = "dc"
found = False

while not found:
	seed = hashlib.sha256(secrets.token_bytes()).digest()
	priv = make_key(seed)
	pub = priv.get_verifying_key()
	
	if desired_str in priv.to_string().hex():
		print("Private: "+priv.to_string().hex())
		print("Public:  "+pub.to_string().hex())
		print("Address: "+toEthAddress(pub))

		found = True