from flask import request, jsonify, g
from models import general_models

def terms():
    if request.method == 'POST':
        # Handle POST request
        req_data = request.get_json()
        if not req_data or "type" not in req_data or "content" not in req_data:
            return {'message': 'Please provide details!', "status": 401}
        new_terms = general_models.Terms(type=req_data["type"], content = req_data["content"])
        new_terms.save()
        return f"Inserted terms with ID: {str(new_terms.id)}"
    elif request.method == 'GET':
        # Handle GET request
        type = request.args.get(type)
        
        terms = general_models.Terms.objects(type=type)
        return
    return {"status": 405, "message": "Method not supported."}
