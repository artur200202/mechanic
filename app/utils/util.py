from datetime import datetime, timedelta, timezone
from jose import jwt 
from flask import request, jsonify
from functools import wraps
import jose

SECRET_KEY= "a super secret, secret key"

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token= None # looks for the token in the authorization header
    if 'Authorization' in request.headers:
      token = request.headers['authorization']. split(" ")[1]
    if not token:
      return jsonify({'message': 'token is missing!'})

    try:
              # Decode the token
      data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
      customer_id = data['sub'] # Fetch user_id
              
    except jose.exceptions.ExpiredSignatureError:
      return jsonify({'message': 'Token has expired'}), 401
    except jose.exceptions.JWTError:
      return jsonify({'message': 'Invalid'}), 401
        
    return f(customer_id, *args, **kwargs)
    
  return decorated

def encode_token(customer_id):
  payload = {
    "exp": datetime.now(timezone.utc) + timedelta(days=0, hours=1), #setting the expiration time to an hour past right now
    "iat": datetime.now(timezone.utc), #issued at
    "sub": str(customer_id) # this needs to be a string or the token will be malformed and wont be able to be decoded
  }

  token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

  return token


