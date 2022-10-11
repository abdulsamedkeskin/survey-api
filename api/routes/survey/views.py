from flask import Blueprint, jsonify, request
from api.routes.user.middleware import login_required
from .models import Survey
from datetime import datetime
from bson import ObjectId

survey = Blueprint('survey', __name__, url_prefix='/survey')

@survey.route("/create", methods=['POST'])
@login_required
def create(payload):
    body = request.get_json(force=True)
    Survey(name=body['name'],questions=body['questions'], created_by=payload['identity'], creation_date=datetime.utcnow()).save()
    return {"status": 200, "message": "Survey created"}, 200

@survey.route("/<id>/delete", methods=['DELETE'])
@login_required
def delete(payload,id):
    survey = Survey.objects.get(id=id)
    if payload['identity'] != survey['created_by']:
        return {"message": 403, "message": "access denied"},403
    survey.delete()
    return {"status": 200, "message": "survey deleted"}, 200

@survey.route("/<id>/answer", methods=['POST'])
@login_required
def answer(payload, id):
    body = request.get_json()
    survey = Survey.objects.get(id=id)
    type = body['type']
    if type == "single":    
        question = survey.questions.filter(_id=body['data']['question'])[0]
        for i in question.choices:
            if payload['identity'] in i.answers:
                return {"status": 400, "message": "user already answered this question"}, 400
        choice = question.choices.filter(_id=body['data']['choice'])[0]
        choice.answers.append(payload['identity'])
        survey.save()
        return {"status": 200, "message": "answer saved"}, 200
    elif type == "bulk":
        for i in body['data']:
            question = survey.questions.filter(_id=i['question'])[0]
            for _ in question.choices:
                if payload['identity'] in _.answers:
                    break
            else:    
                choice = question.choices.filter(_id=i['choice'])[0]
                choice.answers.append(payload['identity'])
        survey.save()
        return {"status": 200, "message": "answers saved"}, 200
    else:
        return {"status": 400, "message": "wrong type"}, 400

@survey.route("/<id>/stats", methods=['GET'])
@login_required
def stats(payload, id):
    pipeline = [
        {"$match": {"_id": ObjectId(id)}},
        {"$unwind": "$questions"},
        {"$replaceRoot": {"newRoot": "$questions"}},
        {"$unwind": "$choices"},
        {"$project": {
                "_id": 0,
                "question_id": "$_id",
                "choice_id": "$choices._id",
                "text": "$choices.text",
                "count": {"$size": "$choices.answers"}
            }
        }
    ]
    survey = Survey.objects.aggregate(*pipeline)
    return list(survey)
    
@survey.route("/my_surveys", methods=['GET'])
@login_required
def my_surveys(payload):
    results = Survey.objects(created_by=payload['identity'])
    return jsonify(results)