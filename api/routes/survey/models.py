from api import db
from bson import ObjectId

class Choice(db.EmbeddedDocument):
    _id = db.ObjectIdField(default=ObjectId, required=True,sparse=True,unique=True, primary_key=True)
    text = db.StringField(required=True)
    answers = db.ListField(default=[])
    
class Question(db.EmbeddedDocument):
    _id = db.ObjectIdField(default=ObjectId, required=True, unique=True, primary_key=True)  
    question = db.StringField(required=True)
    choices = db.EmbeddedDocumentListField(Choice)
    

class Survey(db.Document):
    name = db.StringField(required=True)
    created_by = db.StringField(required=True)
    creation_date = db.DateTimeField()
    questions = db.EmbeddedDocumentListField(Question)
    meta = {
        'collection': 'surveys'
    }

    def to_json(self):
        return {
            "_id": str(self.pk),
            "name": self.name,
            "questions": self.questions,
            "created_by": self.created_by,
            "creation_date": self.creation_date
        }