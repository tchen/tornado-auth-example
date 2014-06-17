import uuid
import base64

def create_cookie_secret():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

if __name__ == '__main__':
    print create_cookie_secret()
