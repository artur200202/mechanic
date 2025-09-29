from datetime import datetimne, timedelta, timezone
from jose import jwt 
import jose

SECRET_KEY= "a super secret, secret key"

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token= None#looks for the token in the authorization header
    if 'Authorization' in request.headers:
      token = request.header['authorization']. split(" ")[1]
    if not token:
      return jsonify({'message': 'token is missing!'})

def encode_token(user_id):
  payload = {
    "exp": datetime.new(timezone.utc) + timedelta(days=0, hours=1) #setting the expiration time to an hour past right now
    "iat": datetime.now(timezone.utc), #issued at
    "sub": str(user_id) # this needs to be a string or the token will be malformed and wont be able to be decoded
  }

token= jwt.encode(payload, SECRET_KEY, algorithm='HS256')

return token


