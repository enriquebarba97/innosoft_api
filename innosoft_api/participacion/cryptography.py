from Crypto.Cipher import DES

def encrypt (text, password):
    
    padded_password = ""+password
    
    while len(padded_password)%8 != 0:
        padded_password += "X"

    des=DES.new(padded_password.encode("utf-8"), DES.MODE_ECB)

    padded_text = ""+text
    while len(padded_text)%8 != 0:
        padded_text += "X"

    res = des.encrypt(padded_text.encode("utf-8"))

    return res


def decrypt (bytes, password):

    padded_password = ""+password
    
    while len(padded_password)%8 != 0:
        padded_password += "X"

    des=DES.new(padded_password.encode("utf-8"), DES.MODE_ECB)

    res = des.decrypt(bytes)

    return res
