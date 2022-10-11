import jwt
from api import key

def decodeToken(token):
   payload = jwt.decode(token, key, algorithms=["HS256"])
   return payload