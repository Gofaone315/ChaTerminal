KEY = 17  # Basic XOR key

def encrypt_msg(msg):
    return bytes([b ^ KEY for b in msg.encode('utf-8')])

def decrypt_msg(data):
    return ''.join([chr(b ^ KEY) for b in data])
