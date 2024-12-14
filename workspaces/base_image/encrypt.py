from cryptography.fernet import Fernet
import base64

# Hardcode the key value and encode it to bytes
key_bytes = b'theagentcompany is all you need'

# Pad the key to 32 bytes using the provided method
def pad_key(key):
    while len(key) < 32:
        key += b'\x00'
    return key[:32]

padded_key = pad_key(key_bytes)

# Get the Fernet instance
fernet = Fernet(base64.urlsafe_b64encode(padded_key))

# Encrypt the evaluator.py file using the Fernet instance
with open('/utils/evaluator.py', 'rb') as f:
    evaluator_content = f.read()

encrypted_evaluator = fernet.encrypt(evaluator_content)

with open('/utils/evaluator.py.enc', 'wb') as f:
    f.write(encrypted_evaluator)
