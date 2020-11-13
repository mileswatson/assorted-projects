import zlib, os
from hashlib import sha256
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key): 
        self.bs = 32
        self.key = sha256(key).digest()
        
    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = os.urandom(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    def decrypt(self, enc):
        enc = enc
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + bytes([self.bs - len(s) % self.bs for i in range(self.bs - len(s) % self.bs)])

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


def package(plainbytes, key):
    compressed = zlib.compress(plainbytes,9)
    crypter = AESCipher(key)
    encrypted = crypter.encrypt(compressed)
    return encrypted

def unpackage(encrypted, key):
    crypter = AESCipher(key)
    compressed = crypter.decrypt(encrypted)
    plainbytes = zlib.decompress(compressed)
    return plainbytes

def key():
    return os.urandom(32)

class Client:

    def __init__(self):
        self.table = dict()

    def send(filename, provider):
        f = open(filename, "rb")
        plainbytes = f.read()
        f.close()
        key = os.urandom(32)
        packaged = package(plainbytes, key)
        ID = sha256(packaged).digest()
        provider.request()

class Provider:
    def __init__(self):
        pass
    
    


#client = Client()
#provider = Provider()

#client.send("input_file.txt", provider)




f = open("input_file.txt","rb")
plainbytes = f.read()
f.close()

privatekey = key()
packaged = package(plainbytes, privatekey)
unpackaged = unpackage(packaged, privatekey)

f = open("compressed.txt", "wb")
f.write(packaged)
f.close()

print(len(plainbytes), len(packaged), len(unpackaged))