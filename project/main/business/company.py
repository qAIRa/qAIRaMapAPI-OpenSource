from flask import jsonify, make_response, request

import project.main.business.post_business_helper as post_business_helper
import project.main.exceptions as exception_helper
from project import app


@app.route("/api/create_company/", methods=["POST"])
def createCompany():
    req_json = request.get_json()
    try:
        exception_helper.getCompanyTargetofJson(req_json)
        post_business_helper.createCompany(req_json)
        return make_response({"Success": "Company has been created"}, 200)
    except (TypeError, ValueError) as e:
        json_message = jsonify({"error": "'%s'" % (e)})
        return make_response(json_message, 400)
    except (Exception) as e:
        json_message = jsonify({"database error": "'%s'" % (e)})
        return make_response(json_message, 400)
