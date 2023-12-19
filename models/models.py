import mongoengine as db
from datetime import datetime
import config
db.connect(config.DATABASE_NAME, host=config.DATABASE_URI)

class BaseDocument(db.Document):
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow, on_modification=True)
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(BaseDocument, self).save(*args, **kwargs)

    meta = {'abstract': True}