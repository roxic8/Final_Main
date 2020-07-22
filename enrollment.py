from functools import wraps

from flask import Flask, jsonify, request
from flask_cors import CORS

from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from dotenv import load_dotenv
from config.db import db
from config.ma import ma
from modules.student.endpoint.student import StudentResource, StudentEnrollResource, StudentGetOfferedSubjectResource, \
    StudentIntentToEnroll, StudentModality, EnrolledData, StudentGetGrades, StudentBilling, \
    StudentCheckIfAlreadyEnrolled, StudentSummary, StudentUpdatePassword, TestingResource

enrollment = Flask(__name__, static_url_path=None)
load_dotenv(".env", verbose=True)
enrollment.config.from_object("dev_config")
enrollment.config.from_envvar("APPLICATION_SETTINGS")

cors = CORS(enrollment, resources={r"/api/*": {"origins": "*"}})
api = Api(enrollment)
db.init_app(enrollment)

ma.init_app(enrollment)
jwt = JWTManager(enrollment)


@enrollment.errorhandler(ValidationError)
def handle_validation_error_marshmallow(err):
    return jsonify(err.messages), 400


@jwt.expired_token_loader
def expire_token_header(error):
    print(error)
    print("Expire na kaluoy")
    print(error)
    return {"message": "Please Login Again Session Expired"}, 401


@jwt.invalid_token_loader
def invalid_token_header(error):
    print("invalid kaluoy")
    print(error)
    return {"message": "Invalid token"}, 422


@jwt.unauthorized_loader
def missing_authorization_header(error):
    print("walay token kaluoy")
    print(error)
    return {"message": "Please Login Again"}, 401


# api.add_resource(, "/api/login/student")
# api.add_resource(UserInfoLogin, "/api/login")


# instructor area
# api.add_resource(InstructorResource, "/api/instructor")
# api.add_resource(InstructorLogin, "/api/instructor/login")

# course area
# api.add_resource(CourseResource, "/api/courses")

# student area
api.add_resource(StudentResource, "/api/student/login")
api.add_resource(StudentEnrollResource, "/api/student/enroll")
api.add_resource(StudentGetOfferedSubjectResource, "/api/student/subject")
api.add_resource(StudentIntentToEnroll, "/api/intent")
api.add_resource(StudentModality, "/api/modal")
api.add_resource(EnrolledData, "/api/enroll")
api.add_resource(StudentGetGrades, "/api/grades")
api.add_resource(StudentBilling, "/api/billing")
api.add_resource(StudentCheckIfAlreadyEnrolled, "/api/checkifenroll")
api.add_resource(StudentSummary, "/api/summary")
api.add_resource(StudentUpdatePassword, "/api/ch")
api.add_resource(TestingResource, "/api/testing")

if __name__ == "__main__":
    enrollment.run(host="127.0.0.1", port=1027)
