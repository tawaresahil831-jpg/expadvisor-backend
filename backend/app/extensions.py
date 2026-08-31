from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Single shared db object, used by every model in the project
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
