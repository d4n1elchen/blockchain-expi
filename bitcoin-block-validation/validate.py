from hashlib import sha256
import codecs

def toHexStr(byte):
    return codecs.encode(byte, 'hex_codec').decode('utf-8')

with open('block.raw', 'r') as file:
    header = file.read()
    file.close()
print()

if len(header) < 160:
    raise ValueError("Invalid length of block!")
elif len(header) > 160:
    header = header[0:160]
    print("Automatic trim header: "+header)
    print()

header = codecs.getdecoder('hex_codec')(header)[0]

version = header[0:4]
hashPrevBlock = header[4:36]
hashMerkleRoot = header[36:68]
time = header[68:72]
bits = header[72:76]
nonce = header[76:80]

print("=== Header fields ===")
print("Version: 0x"+toHexStr(version[::-1]))
print("HashPrevBlock:  0x"+toHexStr(hashPrevBlock[::-1]))
print("HashMerkleRoot: 0x"+toHexStr(hashMerkleRoot[::-1]))
print("Time:  0x"+toHexStr(time[::-1]))
print("nBits: 0x"+toHexStr(bits[::-1]))
print("Nonce: 0x"+toHexStr(nonce[::-1]))
print()

hash = sha256(sha256(header).digest()).digest()
hash_int = int.from_bytes(hash, byteorder="little")
target = int.from_bytes(bits[0:3], byteorder="little") * 256**(bits[3] - 3)

print("=== Block validation ===")
print("BlockHash: 0x"+toHexStr(hash[::-1]))
print("Target:    "+"{0:#0{1}x}".format(target, 66))
print("Validate (hash < target): "+str(hash_int < target))
