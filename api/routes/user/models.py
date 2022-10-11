from api import db

class User(db.Document):
    username = db.StringField(required=True)
    password = db.StringField(required=True)
    meta = {
        'collection': 'users',
    }
    
    def to_json(self):
        return {
            "id": str(self.pk),
            "username": self.username,
            "password": self.password
        }
        
    def payload(self):
        return {
            "identity": str(self.pk),
            "username": self.username
        }