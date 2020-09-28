from flask import jsonify, make_response, request
import project.main.business.get_business_helper as get_business_helper
import project.main.business.post_business_helper as post_business_helper
from project import app

@app.route('/api/create_company/', methods=['POST'])
def createCompany():
    try:
        req_json = request.get_json()
        util_helper.getCompanyTargetofJson(req_json)
        post_business_helper.createCompany(req_json)
    except (TypeError, ValueError ) as e:
        json_message = jsonify({'error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    except (Exception) as e:
        json_message = jsonify({'database error': '\'%s\'' % (e)})
        return make_response(json_message, 400)
    else:
        return make_response({'Success':'Company has been created'}, 200)