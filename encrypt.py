from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

class AES_Encryption:
    def __init__(self,data=None,
                bytes=None,
                key=None,
                ciphertext=None,
                tag=None,
                nonce=None
                ):
        self.data = data.encode("utf-8") if data is not None else ""
        self.bytes = bytes
        self.key = key
        self.ciphertext = ciphertext
        self.tag = tag
        self.nonce = nonce

    def encrypt(self):
        self.key = get_random_bytes(self.bytes)
        self.cipher = AES.new(self.key,AES.MODE_EAX)
        self.ciphertext, self.tag = self.cipher.encrypt_and_digest(self.data)
        self.nonce = self.cipher.nonce
        return [self.key,self.ciphertext,self.tag,self.nonce]

    def decrypt(self):
        self.cipher = AES.new(self.key,AES.MODE_EAX,self.nonce)
        return self.cipher.decrypt_and_verify(self.ciphertext, self.tag).decode()



if __name__ == "__main__":
    text = "hi Hello!"
    message = AES_Encryption(text,32)
    tok = message.encrypt()
    print(tok)
    dec = AES_Encryption(key=tok[0],ciphertext=tok[1],tag=tok[2],nonce=tok[3])
    print(dec.decrypt())