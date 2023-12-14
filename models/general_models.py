import mongoengine as db
from datetime import datetime
import config
db.connect(config.DATABASE_NAME, host=config.DATABASE_URI)

class Terms(db.Document):
    type = db.StringField(required=True, max_length=20)
    content = db.StringField(default="")
    created_at = db.DateTimeField(default=datetime.utcnow)  # Default creation timestamp
    updated_at = db.DateTimeField(default=datetime.utcnow, on_modification=True) # update timestamp on update

    meta = {
        'collection': 'terms'
    }
