import json
from datetime import timedelta, datetime

from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_claims, get_jwt_identity
from flask_restful import Resource
from sqlalchemy import func, create_engine

from sqlalchemy.sql import text
from werkzeug.security import safe_str_cmp

from config.db import db, engine

from modules.student.models.student import TblStudentUser, Tblstudent, Tblstudentstatu, Tblgrade, TblStudentModality, \
    TblSchoolYear
from modules.student.schema.student import StudentSchemaLogin, SchoolYearSchema, StudentPasswordSchema
from rich.console import Console

console = Console()
ERROR_INSERTING = "An error occurred while inserting the record."

schema_login_schema = StudentSchemaLogin()
school_year_schema = SchoolYearSchema(many=True)


# engine = create_engine('mysql+pymysql://root:12345678@127.0.0.1:3306/test1', pool_recycle=3600)
def call_procedure(function_name, *params):
    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.callproc(function_name, params)
        results = list(cursor.fetchall())
        cursor.close()
        connection.commit()
        return results
    except Exception as e:
        print("wrong:" + e)
    finally:
        connection.close()


class StudentResource(Resource):
    @staticmethod
    @jwt_required
    def get():
        return "test", 200

    @staticmethod
    def post():
        student_user_json = request.get_json()
        student_user_data = schema_login_schema.load(student_user_json, partial=("student_id",))
        print(str(student_user_data.username))
        data = student_user_data
        student = TblStudentUser.query.filter_by(username=str(student_user_data.username)).first_or_404()

        student_data = Tblstudent.query.filter_by(std_id=student.student_id).first()
        student_year_lvl = Tblstudentstatu.query.filter_by(student_id=student_data.student_id).order_by(
            Tblstudentstatu.sy_id.desc()).first()
        student_school_year = TblSchoolYear.query.all()
        # # student_status =
        student_claims = {
            "type": "student",
            "student_id": student_data.student_id,
            "course_idd": student_data.course_id,
            "year_lvl": student_year_lvl.yr_level,
            "status": student_year_lvl.is_oficially_enrolled,
            "school_year": 21,
            "semester": 1
        }
        #
        # print(st)
        if student and safe_str_cmp(student.password.lower(), student_user_data.password.lower()):
            access_token = create_access_token(student_data.std_id, fresh=True, expires_delta=timedelta(hours=1),
                                               user_claims=student_claims)

            user_data = call_procedure("sis_student_info_current", student_data.student_id)
            # print(user_data)
            userData = {
                "Name": None,
                "Gender": None,
                "CourseTitle": None,
                "Address": None,
                "Email": None,
                "PhoneNumber": None
            }
            for user in user_data:
                userData["Name"] = user[1] + ' ' + user[2] + ' ' + user[3]
                userData["ShortName"] = user[2]
                userData["Gender"] = user[4]
                userData["CourseTitle"] = user[5],
                userData["Address"] = user[9],
                userData["Email"] = user[12]
                userData["GuardianName"] = user[13]
                userData["GuardianAddress"] = user[14]
                userData["GuardianContactNumber"] = user[15]
                userData["PhoneNumber"] = user[11]
            console.print("access_token", access_token)
            return (
                {
                    "access_token": access_token,
                    "user": userData,
                    "schoolyear": school_year_schema.dump(student_school_year),
                    "tttt": student.first_login
                },
                200,
            )
        # db.engine.dispose()
        # print(db.engine.dispose())
        return {"message": "user not found"}, 404


class StudentGetOfferedSubjectResource(Resource):
    @staticmethod
    @jwt_required
    def get():
        data = []
        claims = get_jwt_claims()
        results = call_procedure("en_offered_subjects_per_slot", claims["course_idd"],
                                 claims["year_lvl"], claims["school_year"], claims["semester"])
        for r in results:
            data.append({
                "subject_code": r[8],
                "subject_id": r[2],
                "offered_id": r[0],
                "units": r[12],
                "instructor": r[15],
            })
        console.print("Offered Subject", data, style="bold red")
        db.engine.dispose()
        return make_response(jsonify(data), 200)


class StudentEnrollResource(Resource):
    @staticmethod
    @jwt_required
    def post():
        parameter1 = "M19-0140"
        data1 = get_jwt_claims
        print(data1)
        data = []
        results = call_procedure("sis_charge", parameter1)
        print(results)
        for r in results:
            data.append({
                "sy_id": r[0],
                "sem_id": r[1],
                "student_id": r[2],
                "description": r[3],
                "amount": r[4],
                "balance": r[5],
                "amountpaid": r[6]
            })
        return data, 201


class EnrolledData(Resource):
    @staticmethod
    @jwt_required
    def get():
        claims = get_jwt_claims()
        results_en_insert_thesis = call_procedure("sis_enrolled_subjects", claims["student_id"])
        data = []
        for r in results_en_insert_thesis:
            data.append({
                "SubjectCode": r[8],
                "Desc": r[9],
                "Class": r[12],
                "Section": r[14],
                "Instructor": r[17],
                "SubjectSched": r[18]
            })
        console.print("EnrolledData Subject", data, style="bold red")

        # db.engine.dispose()
        return make_response(jsonify(data), 200)


class StudentModality(Resource):
    @staticmethod
    @jwt_required
    def post():
        data = request.get_json()
        claims = get_jwt_claims()

        data = TblStudentModality(student_id=claims["student_id"], modality_id=data["id"],
                                  blended_learning=data["blended"])

        try:
            db.session.add(data)
            db.session.commit()
        except:
            return {'message': 'Something went wrong'}, 500
        # db.engine.dispose()
        return "save modality", 201


class StudentIntentToEnroll(Resource):
    @staticmethod
    @jwt_required
    def post():
        claims = get_jwt_claims()
        json_data = request.get_json()
        print(json_data)
        checkifofficialyenrolled = Tblstudentstatu.query.filter_by(student_id=claims["student_id"]).filter_by(
            is_oficially_enrolled=1).filter_by(
            sy_id=21).filter_by(semester_id=1).first()

        if checkifofficialyenrolled:
            return "already enrolled", 400

        for r in json_data:
            print(r)
            print(r["offered_id"])
            checkIfSubjectAdded = Tblgrade.query.filter_by(subject_id=r["subject_id"]).filter_by(
                school_yr_id=21).filter_by(semester_id=1).filter_by(student_id=claims["student_id"]).first()
            if checkIfSubjectAdded is None:
                data = Tblgrade(subject_id=r["subject_id"], subject_offered_id=r["offered_id"],
                                student_id=claims["student_id"],
                                is_assessed=1,
                                final_grade='', remarks="ENROLLED", date_created=datetime.now(),
                                CreatedBy="app", school_yr_id=21, semester_id=1)
                db.session.add(data)
        db.session.commit()

        enroll_data = Tblstudentstatu.query.filter_by(student_id=claims["student_id"], sy_id=21, semester_id=1).first()

        enroll_data.is_oficially_enrolled = 1
        db.session.merge(enroll_data)
        db.session.commit()
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(enroll_data.is_oficially_enrolled)
        print("ENROLLED NAKA: ", claims["student_id"])
        print(enroll_data)
        print(enroll_data)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        # charge auto fees

        # results_auto_fees = call_procedure("en_auto_fees", claims["student_id"], claims["year_lvl"])
        # results_insert_fess_new_student = call_procedure("en_insert_fees_new_student", claims["student_id"])
        # results_en_insert_tuition = call_procedure("en_insert_tuition", claims["student_id"])
        # results_en_insert_lab_fees = call_procedure("en_insert_lab_fees", claims["student_id"])
        # results_en_insert_insurance = call_procedure("en_insert_insurance", claims["student_id"])
        # results_en_insert_fieldstudies = call_procedure("en_insert_fieldstudies", claims["student_id"])
        # results_en_insert_NSTP = call_procedure("en_insert_NSTP", claims["student_id"])
        # results_en_thesis_outline = call_procedure("en_thesis_outline", claims["student_id"])
        # results_en_insert_thesis = call_procedure("en_insert_thesis", claims["student_id"])
        # results_en_insert_graduating_fees = call_procedure("en_insert_graduating_fees", claims["student_id"])
        # db.session.dispose()
        return json_data, 200


class StudentGetGrades(Resource):
    @staticmethod
    @jwt_required
    def get():
        claims = get_jwt_claims()
        grades = call_procedure("sis_scholastic_record", claims["student_id"])
        data = []
        for r in grades:
            data.append({
                "SubjectCode": r[5],
                "Description": r[6],
                "Units": r[7],
                "FinalGrade": r[8],
                "SchoolYear": r[12],
                "Semester": r[14]
            })
        console.print("Get Grades:", claims["student_id"], style="bold red")
        db.session.dispose()
        return make_response(jsonify(data), 200)


class StudentBilling(Resource):
    @staticmethod
    @jwt_required
    def get():
        claims = get_jwt_claims()
        billing = call_procedure("sis_charge", claims['student_id'])
        data = []
        for r in billing:
            data.append({
                "sy_id": r[0],
                "semester_id": r[1],
                "Description": r[3],
                "Obligation": r[4],
                "Balance": r[5],
                "AmoudPaid": r[6],
                "ChargeType": r[7],
                "SchoolYear": r[8],
                "Semester": r[9]
            })
        console.print("Get Billing: ", claims["student_id"], style="bold red")
        db.session.dispose()
        return make_response(jsonify(data), 200)


class StudentCheckIfAlreadyEnrolled(Resource):
    @staticmethod
    @jwt_required
    def get():
        claims = get_jwt_claims()
        checkifofficialyenrolled = Tblstudentstatu.query.filter_by(student_id=claims["student_id"]).filter_by(
            is_oficially_enrolled=1).filter_by(
            sy_id=21).filter_by(semester_id=1).first()

        print("=================")
        print(checkifofficialyenrolled)
        print(checkifofficialyenrolled)
        print(checkifofficialyenrolled)
        print(checkifofficialyenrolled)
        print("=================")

        if checkifofficialyenrolled:
            return True, 200
        return False, 200


class StudentSummary(Resource):
    @staticmethod
    @jwt_required
    def get():
        claims = get_jwt_claims()
        summary = call_procedure("sis_accountsummary", claims['student_id'])
        data = []
        for r in summary:
            data.append({
                "SchoolYear": r[2],
                "Semester": r[3],
                "Amount": r[5],
                "Balance": r[6],
                "AmountPaid": r[7]
            })
        console.print("Summary", data, style="bold red")
        db.session.dispose()
        return make_response(jsonify(data), 200)


class StudentUpdatePassword(Resource):
    @staticmethod
    @jwt_required
    def post():
        password = request.get_json()
        print(password)
        password_Schema = StudentPasswordSchema()
        data = password_Schema.load(password)
        student = TblStudentUser.query.filter_by(student_id=get_jwt_identity()).first()
        student.password = data["password"]
        student.first_login = 1
        db.session.merge(student)
        db.session.commit()
        return data, 200


class TestingResource(Resource):
    @staticmethod
    def get():
        id = "m19-0140"
        call_procedure("en_auto_fees", "m19-0140", 1)
        call_procedure("en_insert_fees_new_student", id)
        call_procedure("en_insert_tuition", id)
        call_procedure("en_insert_lab_fees", id)
        call_procedure("en_insert_insurance", id)
        call_procedure("en_insert_fieldstudies", id)
        call_procedure("en_insert_NSTP", id)
        call_procedure("en_thesis_outline", id)
        call_procedure("en_insert_thesis", id)
        call_procedure("en_insert_graduating_fees", id)

        return "Ok", 200
