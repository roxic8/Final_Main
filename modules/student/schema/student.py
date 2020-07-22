from marshmallow import Schema, fields

from config.ma import ma
from modules.student.models.student import TblSchoolYear, TblStudentUser


class StudentSchemaLogin(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TblStudentUser
        include_fk = True
        load_instance = True


class StudentPasswordSchema(Schema):
    password = fields.Str()


class SchoolYearSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TblSchoolYear
        include_fk = True
        load_instance = True
        ordered = True
