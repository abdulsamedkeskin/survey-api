from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_SETTINGS = {
    "host": os.environ.get('DB_HOST'),
    "db": "test"
}
JSON_SORT_KEYS = False
JSONIFY_PRETTYPRINT_REGULAR= True
JSON_AS_ASCII = False