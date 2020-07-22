# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, ForeignKey, Index, Integer, String, Table, Text, \
    VARBINARY
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql.types import BIT
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

t_balances_notpaid_sy19_1 = db.Table(
    'balances_notpaid_sy19_1',
    db.Column('charge_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('student_id', db.String(50)),
    db.Column('tbc_description', db.String(50)),
    db.Column('amount', db.Float(8, True)),
    db.Column('balance', db.Float(8, True)),
    db.Column('amountpaid', db.Float(8, True), server_default=db.FetchedValue()),
    db.Column('description', db.String(50)),
    db.Column('amount_paid', db.Float(10, True)),
    db.Column('or_number', db.String(20))
)

t_balances_view = db.Table(
    'balances_view',
    db.Column('charge_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('student_id', db.String(50)),
    db.Column('description', db.String(50)),
    db.Column('AmountPayable', db.Float(8, True)),
    db.Column('TotalPaidAmountWithOR', db.Float(19, True)),
    db.Column('balance', db.Float(8, True)),
    db.Column('reflectedAmountPaid', db.Float(8, True), server_default=db.FetchedValue()),
    db.Column('syid_ch', db.Integer),
    db.Column('sem_ch', db.Integer),
    db.Column('sy_id', db.Integer),
    db.Column('sem_id', db.Integer)
)

t_billing_part2afee = db.Table(
    'billing_part2afee',
    db.Column('student_id', db.String(50)),
    db.Column('description', db.String(50)),
    db.Column('Tuition', db.Float(19, True)),
    db.Column('Admission_Fees', db.Float(19, True)),
    db.Column('Athletic_Fees', db.Float(19, True)),
    db.Column('Computer_Fees', db.Float(19, True))
)


class Cnfileslog(db.Model):
    __tablename__ = 'cnfileslog'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.String(30), nullable=False)
    time_in = db.Column(db.String(20), nullable=False)
    sy_id = db.Column(db.Integer, nullable=False)
    sem_id = db.Column(db.Integer, nullable=False)


t_enrollment_schedules = db.Table(
    'enrollment_schedules',
    db.Column('activity', db.String(50)),
    db.Column('start', db.Date, nullable=False),
    db.Column('end', db.Date, nullable=False),
    db.Column('year_level', db.String(30)),
    db.Column('is_MS', db.Integer)
)


class Exceptiongrade(db.Model):
    __tablename__ = 'exceptiongrade'

    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(2), nullable=False)


class Graduatedcourse(db.Model):
    __tablename__ = 'graduatedcourse'

    Id = db.Column(db.Integer, primary_key=True)
    StudentId = db.Column(db.ForeignKey('tblstudent.student_id'), nullable=False, index=True)
    Course = db.Column(db.Text, nullable=False)

    tblstudent = db.relationship('Tblstudent', primaryjoin='Graduatedcourse.StudentId == Tblstudent.student_id',
                                 backref='graduatedcourses')


class Ictlab(db.Model):
    __tablename__ = 'ictlab'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.String(30), nullable=False)
    sy_id = db.Column(db.Integer, nullable=False)
    sem_id = db.Column(db.Integer, nullable=False)


class Infosystem(db.Model):
    __tablename__ = 'infosystem'

    is_id = db.Column(db.Integer, primary_key=True)
    IS_Name = db.Column(db.String(50))
    DateCreated = db.Column(db.DateTime)
    Version = db.Column(db.String(25))
    ProgrammingL = db.Column(db.String(50))
    Developer = db.Column(db.String(50))


class Previouscourse(db.Model):
    __tablename__ = 'previouscourse'

    PreviousCourseId = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.ForeignKey('tblstudent.student_id'), nullable=False, index=True)
    course_id = db.Column(db.ForeignKey('tblcourses.course_id'), nullable=False, index=True)
    sy_id = db.Column(db.ForeignKey('tbl_school_year.school_year_id'), nullable=False, index=True)
    sem_id = db.Column(db.ForeignKey('tblsemester.semester_id'), nullable=False, index=True)
    date_created = db.Column(db.String(30))

    course = db.relationship('Tblcourse', primaryjoin='Previouscourse.course_id == Tblcourse.course_id',
                             backref='previouscourses')
    sem = db.relationship('Tblsemester', primaryjoin='Previouscourse.sem_id == Tblsemester.semester_id',
                          backref='previouscourses')
    student = db.relationship('Tblstudent', primaryjoin='Previouscourse.student_id == Tblstudent.student_id',
                              backref='previouscourses')
    sy = db.relationship('TblSchoolYear', primaryjoin='Previouscourse.sy_id == TblSchoolYear.school_year_id',
                         backref='previouscourses')


class Section(db.Model):
    __tablename__ = 'section'

    SectionId = db.Column(db.Integer, primary_key=True)
    SectionName = db.Column(db.String(5), nullable=False)


class Series(db.Model):
    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    IP = db.Column(db.String(35))
    sy = db.Column(db.Integer)


class Subjectfee(db.Model):
    __tablename__ = 'subjectfee'

    Id = db.Column(db.Integer, primary_key=True)
    SubjectId = db.Column(db.ForeignKey('tblsubjects.subject_id'), nullable=False, index=True)
    Fee = db.Column(db.String(50), nullable=False)
    Amount = db.Column(db.Float(8, True), nullable=False)
    Fund = db.Column(db.String(30), nullable=False)
    DateCreated = db.Column(db.DateTime)

    tblsubject = db.relationship('Tblsubject', primaryjoin='Subjectfee.SubjectId == Tblsubject.subject_id',
                                 backref='subjectfees')


t_tbl_current_sy = db.Table(
    'tbl_current_sy',
    db.Column('id', db.Integer, nullable=False, index=True),
    db.Column('sy', db.String(50)),
    db.Column('sem', db.String(50)),
    db.Column('enrollment', db.String(11)),
    db.Column('term', db.String(12))
)

t_tbl_documents = db.Table(
    'tbl_documents',
    db.Column('documentID', db.Integer),
    db.Column('Name', db.String(255)),
    db.Column('CategoryID', db.Integer),
    db.Column('Description', db.String(255)),
    db.Column('DateTime', db.DateTime)
)


class TblInstructor(db.Model):
    __tablename__ = 'tbl_instructor'

    instructor_id = db.Column(db.Integer, primary_key=True, nullable=False)
    designation = db.Column(db.String(45))
    UserStatus = db.Column(db.Integer)
    first_name = db.Column(db.String(45))
    middle_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45), index=True)
    Email = db.Column(db.VARBINARY(45))
    institute_id = db.Column(db.ForeignKey('tblinstitute.institute_id'), primary_key=True, nullable=False, index=True)
    date_created = db.Column(db.String(45))
    date_modified = db.Column(db.String(45))

    institute = db.relationship('Tblinstitute', primaryjoin='TblInstructor.institute_id == Tblinstitute.institute_id',
                                backref='tbl_instructors')


class TblInstructorUser(db.Model):
    __tablename__ = 'tbl_instructor_user'

    Id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.ForeignKey('tbl_instructor.instructor_id'), nullable=False, index=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    isInstructor = db.Column(db.Boolean(1), nullable=False)

    instructor = db.relationship('TblInstructor',
                                 primaryjoin='TblInstructorUser.instructor_id == TblInstructor.instructor_id',
                                 backref='tbl_instructor_users')


class TblIsUseraccount(db.Model):
    __tablename__ = 'tbl_is_useraccount'

    acc_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    staff_id = db.Column(db.String(30))
    instructor_id = db.Column(db.Integer)


t_tbl_nstp = db.Table(
    'tbl_nstp',
    db.Column('SerialNumber', db.String(25)),
    db.Column('Name', db.String(50)),
    db.Index('SerialNumber', 'SerialNumber', 'Name')
)


class TblSchoolYear(db.Model):
    __tablename__ = 'tbl_school_year'

    school_year_id = db.Column(db.Integer, primary_key=True)
    school_year = db.Column(db.String(25), nullable=False)


class TblStudentModality(db.Model):
    __tablename__ = 'tbl_student_modality'

    Id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(255))
    modality_id = db.Column(db.ForeignKey('tbl_student_modality_type.Id'), index=True)
    blended_learning = db.Column(db.String(255))

    modality = db.relationship('TblStudentModalityType',
                               primaryjoin='TblStudentModality.modality_id == TblStudentModalityType.Id',
                               backref='tbl_student_modalities')


class TblStudentModalityType(db.Model):
    __tablename__ = 'tbl_student_modality_type'

    Id = db.Column(db.Integer, primary_key=True)
    modality_type = db.Column(db.String(255), nullable=False)


class TblStudentUser(db.Model):
    __tablename__ = 'tbl_student_user'

    Id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.ForeignKey('tblstudent.std_id'), nullable=False, index=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_login = db.Column(db.Integer)

    student = db.relationship('Tblstudent', primaryjoin='TblStudentUser.student_id == Tblstudent.std_id',
                              backref='tbl_student_users')


t_tbl_user_accounts = db.Table(
    'tbl_user_accounts',
    db.Column('id', db.Integer, nullable=False, index=True),
    db.Column('user_id', db.String(50), nullable=False),
    db.Column('Password', db.String(50)),
    db.Column('Rights', db.String(50), server_default=db.FetchedValue()),
    db.Column('Dept', db.Integer, nullable=False)
)

t_tblbarangay = db.Table(
    'tblbarangay',
    db.Column('barangay_id', db.String(225)),
    db.Column('barangay', db.String(225)),
    db.Column('municipality_id', db.String(225))
)


class Tblcharge(db.Model):
    __tablename__ = 'tblcharge'

    charge_id = db.Column(db.Integer, primary_key=True)
    Fee_id = db.Column(db.Integer, server_default=db.FetchedValue())
    description = db.Column(db.String(50, 'latin1_general_ci'), nullable=False)
    student_id = db.Column(db.String(50), nullable=False, index=True)
    amount = db.Column(db.Float(8, True), nullable=False)
    balance = db.Column(db.Float(8, True), nullable=False)
    amountpaid = db.Column(db.Float(8, True))
    fund = db.Column(db.String(10, 'latin1_general_ci'), nullable=False, server_default=db.FetchedValue())
    priority_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    sy_id = db.Column(db.Integer, nullable=False, index=True)
    sem_id = db.Column(db.Integer, nullable=False, index=True)
    CreationDate = db.Column(db.String(125, 'latin1_general_ci'), nullable=False)
    CreatedBy = db.Column(db.String(20, 'latin1_general_ci'), nullable=False)


class Tblcourse(db.Model):
    __tablename__ = 'tblcourses'

    course_id = db.Column(db.Integer, primary_key=True)
    institute_id = db.Column(db.ForeignKey('tblinstitute.institute_id'), nullable=False, index=True)
    course_title = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(255), nullable=False)
    is_MS = db.Column(db.Integer, server_default=db.FetchedValue())
    is_board = db.Column(db.Integer, server_default=db.FetchedValue())

    institute = db.relationship('Tblinstitute', primaryjoin='Tblcourse.institute_id == Tblinstitute.institute_id',
                                backref='tblcourses')


class TblcreditedSubject(db.Model):
    __tablename__ = 'tblcredited_subjects'

    credited_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.ForeignKey('tblstudent.student_id'), nullable=False, index=True)
    subject_id = db.Column(db.ForeignKey('tblsubjects.subject_id'), nullable=False, index=True)
    final_grade = db.Column(db.String(15), nullable=False)
    date_saved = db.Column(db.String(45))

    student = db.relationship('Tblstudent', primaryjoin='TblcreditedSubject.student_id == Tblstudent.student_id',
                              backref='tblcredited_subjects')
    subject = db.relationship('Tblsubject', primaryjoin='TblcreditedSubject.subject_id == Tblsubject.subject_id',
                              backref='tblcredited_subjects')


class Tblcurrentschoolyear(db.Model):
    __tablename__ = 'tblcurrentschoolyear'

    Id = db.Column(db.Integer, primary_key=True)
    sy_id = db.Column(db.ForeignKey('tbl_school_year.school_year_id'), nullable=False, index=True)
    sem_id = db.Column(db.ForeignKey('tblsemester.semester_id'), nullable=False, index=True)

    sem = db.relationship('Tblsemester', primaryjoin='Tblcurrentschoolyear.sem_id == Tblsemester.semester_id',
                          backref='tblcurrentschoolyears')
    sy = db.relationship('TblSchoolYear', primaryjoin='Tblcurrentschoolyear.sy_id == TblSchoolYear.school_year_id',
                         backref='tblcurrentschoolyears')


class Tblcurriculum(db.Model):
    __tablename__ = 'tblcurriculum'
    __table_args__ = (
        db.Index('course_id_2', 'course_id', 'subject_id', 'yr_level', 'semester_id', 'Effectivity', 'Remarks'),
    )

    curriculum_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.ForeignKey('tblcourses.course_id'), index=True)
    subject_id = db.Column(db.ForeignKey('tblsubjects.subject_id'), index=True)
    yr_level = db.Column(db.Integer)
    semester_id = db.Column(db.Integer, index=True)
    Effectivity = db.Column(db.String(50))
    Remarks = db.Column(db.String(225))

    course = db.relationship('Tblcourse', primaryjoin='Tblcurriculum.course_id == Tblcourse.course_id',
                             backref='tblcurriculums')
    subject = db.relationship('Tblsubject', primaryjoin='Tblcurriculum.subject_id == Tblsubject.subject_id',
                              backref='tblcurriculums')


class Tbldatesubmission(db.Model):
    __tablename__ = 'tbldatesubmission'

    id = db.Column(db.Integer, primary_key=True)
    submitDate = db.Column(db.DateTime)
    sy_id = db.Column(db.Integer)
    sem_id = db.Column(db.Integer)
    YearStatus = db.Column(db.String(11))


t_tblenrolmentprocess = db.Table(
    'tblenrolmentprocess',
    db.Column('EnrolmentProcessNo', db.Integer, nullable=False),
    db.Column('Student_ID', db.String(50), nullable=False),
    db.Column('Process_Name', db.String(50)),
    db.Column('Processed_by', db.String(50)),
    db.Column('Date_Process', db.Date),
    db.Column('Status', db.String(50), server_default=db.FetchedValue()),
    db.Column('Remarks', db.String(255))
)

t_tblesgppafee = db.Table(
    'tblesgppafee',
    db.Column('OtherfeeID', db.Integer, nullable=False, index=True),
    db.Column('StudentID', db.String(50), nullable=False, index=True),
    db.Column('Description', db.String(255), index=True),
    db.Column('Amount', db.Float(8, True)),
    db.Column('SemesterID', db.Integer),
    db.Column('SchoolYearID', db.Integer),
    db.Column('DateCreated', db.String(255)),
    db.Index('SchoolYearID', 'SchoolYearID', 'SemesterID')
)


class TblethnicGroup(db.Model):
    __tablename__ = 'tblethnic_group'

    Ethnic_id = db.Column(db.Integer, primary_key=True)
    EthnicGroup = db.Column(db.String(255), nullable=False)


class Tblexamschedule(db.Model):
    __tablename__ = 'tblexamschedule'

    schedule_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.ForeignKey('tblsubjects.subject_id'), nullable=False, index=True)
    offer_subject_id = db.Column(db.Integer, nullable=False)
    _class = db.Column('class', db.String(10), nullable=False)
    instructor_id = db.Column(db.ForeignKey('tbl_instructor.instructor_id'),
                              db.ForeignKey('tbl_instructor.instructor_id'), nullable=False, index=True)
    proctor_id = db.Column(db.ForeignKey('tbl_instructor.instructor_id'), nullable=False, index=True)
    days = db.Column(db.String(15), nullable=False)
    room_id = db.Column(db.ForeignKey('tblrooms.room_id'), nullable=False, index=True)
    time_in = db.Column(db.String(25), nullable=False)
    time_out = db.Column(db.String(25), nullable=False)
    date = db.Column(db.String(25), nullable=False)
    school_year_id = db.Column(db.ForeignKey('tbl_school_year.school_year_id'), nullable=False, index=True)
    semester_id = db.Column(db.ForeignKey('tblsemester.semester_id'), nullable=False, index=True)
    date_created = db.Column(db.String(25), nullable=False)
    created_by = db.Column(db.String(20), nullable=False)
    date_modified = db.Column(db.String(25))
    modified_by = db.Column(db.String(20))


class Tblfee(db.Model):
    __tablename__ = 'tblfee'

    fee_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100, 'latin1_general_ci'), nullable=False, index=True)
    amount = db.Column(db.Float(8, True), nullable=False)
    charge_type = db.Column(db.String(250, 'latin1_general_ci'))
    category = db.Column(db.String(250, 'latin1_general_ci'))
    Applicable_year = db.Column(db.String(11, 'latin1_general_ci'))
    Fee_status = db.Column(db.String(255, 'latin1_general_ci'))
    is_cons = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    fund = db.Column(db.String(10, 'latin1_general_ci'), nullable=False)
    is_msa_fee = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    priority_status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_other_fee = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    CreationDate = db.Column(db.String(25, 'latin1_general_ci'))
    CreatedBy = db.Column(db.String(20, 'latin1_general_ci'))
    ModifiedDate = db.Column(db.String(25, 'latin1_general_ci'))
    ModifiedBy = db.Column(db.String(20, 'latin1_general_ci'))


class Tblgrade(db.Model):
    __tablename__ = 'tblgrades'
    __table_args__ = (
        db.Index('subject_id_2', 'subject_id', 'subject_offered_id', 'student_id', 'school_yr_id', 'semester_id'),
    )

    grade_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.ForeignKey('tblsubjects.subject_id'), nullable=False, index=True)
    subject_offered_id = db.Column(db.ForeignKey('tblofferedsubjects.offered_id'), nullable=False, index=True)
    student_id = db.Column(db.ForeignKey('tblstudent.student_id'), nullable=False, index=True)
    final_grade = db.Column(db.String(15), nullable=False, server_default=db.FetchedValue())
    remarks = db.Column(db.String(45), nullable=False)
    is_assessed = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    date_created = db.Column(db.String(50))
    CreatedBy = db.Column(db.String(50, 'latin1_general_ci'))
    school_yr_id = db.Column(db.ForeignKey('tbl_school_year.school_year_id'), nullable=False, index=True)
    semester_id = db.Column(db.ForeignKey('tblsemester.semester_id'), nullable=False, index=True)
    DateSubmitted = db.Column(db.DateTime)
    Status = db.Column(db.Integer, server_default=db.FetchedValue())

    school_yr = db.relationship('TblSchoolYear', primaryjoin='Tblgrade.school_yr_id == TblSchoolYear.school_year_id',
                                backref='tblgrades')
    semester = db.relationship('Tblsemester', primaryjoin='Tblgrade.semester_id == Tblsemester.semester_id',
                               backref='tblgrades')
    student = db.relationship('Tblstudent', primaryjoin='Tblgrade.student_id == Tblstudent.student_id',
                              backref='tblgrades')
    subject = db.relationship('Tblsubject', primaryjoin='Tblgrade.subject_id == Tblsubject.subject_id',
                              backref='tblgrades')
    subject_offered = db.relationship('Tblofferedsubject',
                                      primaryjoin='Tblgrade.subject_offered_id == Tblofferedsubject.offered_id',
                                      backref='tblgrades')


class Tblinstitute(db.Model):
    __tablename__ = 'tblinstitute'

    institute_id = db.Column(db.Integer, primary_key=True)
    institute_title = db.Column(db.String(45), nullable=False)
    institute = db.Column(db.String(100), nullable=False)


t_tblmunicipality = db.Table(
    'tblmunicipality',
    db.Column('municipality_name', db.String(225)),
    db.Column('province_id', db.String(225)),
    db.Column('municipality_id', db.String(225))
)


class Tblofferedsubject(db.Model):
    __tablename__ = 'tblofferedsubjects'

    offered_id = db.Column(db.Integer, primary_key=True, nullable=False)
    subject_id = db.Column(db.ForeignKey('tblsubjects.subject_id'), nullable=False, index=True)
    course_id = db.Column(db.ForeignKey('tblcourses.course_id'), nullable=False, index=True)
    year_level = db.Column(db.String(5), nullable=False, index=True)
    offer_subject_id = db.Column(db.Integer, primary_key=True, nullable=False)
    section = db.Column(db.String(5), nullable=False, index=True)
    slots = db.Column(db.String(5), nullable=False, server_default=db.FetchedValue())
    school_year_id = db.Column(db.ForeignKey('tbl_school_year.school_year_id'), nullable=False, index=True)
    semester_id = db.Column(db.ForeignKey('tblsemester.semester_id'), nullable=False, index=True)
    date_created = db.Column(db.String(25), nullable=False)
    created_by = db.Column(db.String(25), nullable=False)
    modified_date = db.Column(db.String(25))
    modified_by = db.Column(db.String(25))

    course = db.relationship('Tblcourse', primaryjoin='Tblofferedsubject.course_id == Tblcourse.course_id',
                             backref='tblofferedsubjects')
    school_year = db.relationship('TblSchoolYear',
                                  primaryjoin='Tblofferedsubject.school_year_id == TblSchoolYear.school_year_id',
                                  backref='tblofferedsubjects')
    semester = db.relationship('Tblsemester', primaryjoin='Tblofferedsubject.semester_id == Tblsemester.semester_id',
                               backref='tblofferedsubjects')
    subject = db.relationship('Tblsubject', primaryjoin='Tblofferedsubject.subject_id == Tblsubject.subject_id',
                              backref='tblofferedsubjects')


class Tblotherfee(db.Model):
    __tablename__ = 'tblotherfees'

    fee_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100, 'latin1_general_ci'))
    amount = db.Column(db.Float(5, True))
    fund = db.Column(db.String(100, 'latin1_general_ci'))
    CreationDate = db.Column(db.String(100, 'latin1_general_ci'))
    CreatedBy = db.Column(db.String(100, 'latin1_general_ci'))
    ModifiedDate = db.Column(db.String(100, 'latin1_general_ci'))
    ModifiedBy = db.Column(db.String(100, 'latin1_general_ci'))


class Tbloverpayment(db.Model):
    __tablename__ = 'tbloverpayment'

    payment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.ForeignKey('tblstudent.student_id'), nullable=False, index=True)
    amount = db.Column(db.Float(8, True), nullable=False)
    trandate = db.Column(db.String(45), nullable=False)
    sy_id = db.Column(db.ForeignKey('tbl_school_year.school_year_id'), nullable=False, index=True)
    sem_id = db.Column(db.ForeignKey('tblsemester.semester_id'), nullable=False, index=True)

    sem = db.relationship('Tblsemester', primaryjoin='Tbloverpayment.sem_id == Tblsemester.semester_id',
                          backref='tbloverpayments')
    student = db.relationship('Tblstudent', primaryjoin='Tbloverpayment.student_id == Tblstudent.student_id',
                              backref='tbloverpayments')
    sy = db.relationship('TblSchoolYear', primaryjoin='Tbloverpayment.sy_id == TblSchoolYear.school_year_id',
                         backref='tbloverpayments')


class Tblpayment(db.Model):
    __tablename__ = 'tblpayment'

    payment_id = db.Column(db.Integer, primary_key=True)
    charge_id = db.Column(db.Integer, nullable=False)
    is_primary_fee = db.Column(db.Integer, nullable=False)
    or_number = db.Column(db.String(20), nullable=False)
    student_id = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.String(50), nullable=False, index=True)
    amount_paid = db.Column(db.Float(10, True), nullable=False)
    cash_tendered = db.Column(db.Float(10, True))
    payment_change = db.Column(db.Float(10, True))
    fund = db.Column(db.String(20), nullable=False)
    tran_date = db.Column(db.Date, nullable=False, index=True)
    sy_id = db.Column(db.ForeignKey('tbl_school_year.school_year_id'), nullable=False, index=True)
    sem_id = db.Column(db.ForeignKey('tblsemester.semester_id'), nullable=False, index=True)
    creation_date = db.Column(db.String(50))
    created_by = db.Column(db.String(20))

    sem = db.relationship('Tblsemester', primaryjoin='Tblpayment.sem_id == Tblsemester.semester_id',
                          backref='tblpayments')
    sy = db.relationship('TblSchoolYear', primaryjoin='Tblpayment.sy_id == TblSchoolYear.school_year_id',
                         backref='tblpayments')


class Tblprerequisite(db.Model):
    __tablename__ = 'tblprerequisite'

    prerequisite_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.ForeignKey('tblsubjects.subject_id'), nullable=False, index=True)
    prerequisite_subject_id = db.Column(db.ForeignKey('tblsubjects.subject_id'), nullable=False, index=True)

    prerequisite_subject = db.relationship('Tblsubject',
                                           primaryjoin='Tblprerequisite.prerequisite_subject_id == Tblsubject.subject_id',
                                           backref='tblsubject_tblprerequisites')
    subject = db.relationship('Tblsubject', primaryjoin='Tblprerequisite.subject_id == Tblsubject.subject_id',
                              backref='tblsubject_tblprerequisites_0')


t_tblprovince = db.Table(
    'tblprovince',
    db.Column('province_id', db.String(225)),
    db.Column('province_name', db.String(225))
)


class Tblrequirement(db.Model):
    __tablename__ = 'tblrequirements'

    id = db.Column(db.Integer, primary_key=True)
    Req_ID = db.Column(db.String(25))
    Particulars = db.Column(db.String(25))
    ReqType = db.Column(db.String(25))


class Tblroom(db.Model):
    __tablename__ = 'tblrooms'

    room_id = db.Column(db.Integer, primary_key=True, nullable=False)
    room = db.Column(db.String(50))
    institute_id = db.Column(db.ForeignKey('tblinstitute.institute_id'), primary_key=True, nullable=False, index=True)
    date_created = db.Column(db.String(30), nullable=False)
    date_modified = db.Column(db.String(30))

    institute = db.relationship('Tblinstitute', primaryjoin='Tblroom.institute_id == Tblinstitute.institute_id',
                                backref='tblrooms')


class Tblscholar(db.Model):
    __tablename__ = 'tblscholar'

    scholar_id = db.Column(db.Integer, primary_key=True)
    scholarship_id = db.Column(db.ForeignKey('tblscholarship.scholarship_id'), nullable=False, index=True)
    student_id = db.Column(db.ForeignKey('tblstudent.student_id'), nullable=False, index=True)
    sy_id = db.Column(db.ForeignKey('tbl_school_year.school_year_id'), nullable=False, index=True)
    sem_id = db.Column(db.ForeignKey('tblsemester.semester_id'), nullable=False, index=True)
    date_created = db.Column(db.DateTime, nullable=False)

    scholarship = db.relationship('Tblscholarship',
                                  primaryjoin='Tblscholar.scholarship_id == Tblscholarship.scholarship_id',
                                  backref='tblscholars')
    sem = db.relationship('Tblsemester', primaryjoin='Tblscholar.sem_id == Tblsemester.semester_id',
                          backref='tblscholars')
    student = db.relationship('Tblstudent', primaryjoin='Tblscholar.student_id == Tblstudent.student_id',
                              backref='tblscholars')
    sy = db.relationship('TblSchoolYear', primaryjoin='Tblscholar.sy_id == TblSchoolYear.school_year_id',
                         backref='tblscholars')


class Tblscholarship(db.Model):
    __tablename__ = 'tblscholarship'

    scholarship_id = db.Column(db.Integer, primary_key=True)
    scholarship = db.Column(db.String(50), index=True)
    Allocation = db.Column(db.String(50))
    Benefactor = db.Column(db.String(50))
    CreatedBy = db.Column(db.String(50))
    CreationDate = db.Column(db.String(50))


class Tblsemester(db.Model):
    __tablename__ = 'tblsemester'

    semester_id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(25), nullable=False)


class Tblseq(db.Model):
    __tablename__ = 'tblseq'

    id = db.Column(db.Integer, primary_key=True)


class Tblstaff(db.Model):
    __tablename__ = 'tblstaff'

    staff_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable=False)
    designation = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    UnitID = db.Column(db.Integer)


class Tblstudent(db.Model):
    __tablename__ = 'tblstudent'

    std_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), index=True)
    FirstName = db.Column(db.String(50), nullable=False)
    MiddleName = db.Column(db.String(50))
    LastName = db.Column(db.String(50), nullable=False, index=True)
    Suffix = db.Column(db.String(25))
    course_id = db.Column(db.Integer, nullable=False, index=True)
    Gender = db.Column(db.String(10), nullable=False)
    PhoneNumber = db.Column(db.String(11))
    Status = db.Column(db.String(10))
    Email = db.Column(db.String(25))
    Citizenship = db.Column(db.String(15))
    BirthDate = db.Column(db.String(25))
    PlaceOfBirth = db.Column(db.String(100))
    ZipCode = db.Column(db.Integer)
    HomeAddress = db.Column(db.String(100))
    PresentAddress = db.Column(db.String(100))
    CityAddress = db.Column(db.String(100))
    BloodType = db.Column(db.String(10))
    Religion = db.Column(db.String(50))
    EthnicGroup = db.Column(db.String(50))
    Disability = db.Column(db.String(50))
    DSWDHOUSEHOLDNO = db.Column(db.String(50))
    HOUSEHOLDPERCAPITAINCOME = db.Column(db.String(50))
    SpouseName = db.Column(db.String(100))
    SpouseAddress = db.Column(db.String(100))
    Intermediate = db.Column(db.String(100))
    EntranceCredential = db.Column(db.String(100))
    DateOfAdmission = db.Column(db.String(100))
    LastSchoolName = db.Column(db.String(100))
    LastSchoolContactNumber = db.Column(db.String(100))
    LastSchoolAddress = db.Column(db.String(100))
    GenAve = db.Column(db.String(20))
    MotherName = db.Column(db.String(50))
    MotherOccupation = db.Column(db.String(30))
    FatherName = db.Column(db.String(50))
    FatherOccupation = db.Column(db.String(30))
    ParentsContactNumber = db.Column(db.String(100))
    ParentsAddress = db.Column(db.String(100))
    GuardianName = db.Column(db.String(50))
    GuardianAddress = db.Column(db.String(100))
    GuardianContactNumber = db.Column(db.String(20))
    Transferee = db.Column(db.String(10), server_default=db.FetchedValue())
    TransfereeYL = db.Column(db.String(10), server_default=db.FetchedValue())
    code = db.Column(db.String(25))
    CreationDate = db.Column(db.String(25))
    CreatedBy = db.Column(db.String(20))
    ModifiedDate = db.Column(db.String(25))
    ModifiedBy = db.Column(db.String(25))
    Province = db.Column(db.String(25))
    Municipality = db.Column(db.String(25))
    Barangay = db.Column(db.String(25))
    PA_Province = db.Column(db.String(25))
    PA_Municipality = db.Column(db.String(25))
    PA_Barangay = db.Column(db.String(25))
    PA_Zipcode = db.Column(db.Integer)
    MotherFirstName = db.Column(db.String(100))
    MotherMiddleName = db.Column(db.String(100))
    MotherLastName = db.Column(db.String(100))
    MotherMaidenName = db.Column(db.String(100))
    FatherFirstName = db.Column(db.String(100))
    FatherMiddleName = db.Column(db.String(100))
    FatherLastName = db.Column(db.String(100))
    Remark = db.Column(db.String(25))
    NSTPSerial = db.Column(db.String(55))
    PWD = db.Column(db.String(100))


class Tblstudentgrade(db.Model):
    __tablename__ = 'tblstudentgrades'

    gradeid = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(20), nullable=False, index=True)
    Remarks = db.Column(db.String(20))


class Tblstudentstatu(db.Model):
    __tablename__ = 'tblstudentstatus'
    __table_args__ = (
        db.Index('StudentStatus', 'student_id', 'sy_id', 'semester_id'),
    )

    status_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False, index=True)
    status = db.Column(db.String(20))
    course_id = db.Column(db.Integer, nullable=False, index=True)
    yr_level = db.Column(db.String(10))
    previous_course_id = db.Column(db.String(15))
    is_oficially_enrolled = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    date_created = db.Column(db.String(40))
    CreatedBy = db.Column(db.String(50))
    date_updated = db.Column(db.String(50))
    sy_id = db.Column(db.Integer, nullable=False, index=True)
    semester_id = db.Column(db.Integer, nullable=False, index=True)



class TblstudentstatusNew(db.Model):
    __tablename__ = 'tblstudentstatus_new'
    __table_args__ = (
        db.Index('StudentStatus', 'student_id', 'sy_id', 'semester_id'),
    )

    status_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False, index=True)
    status = db.Column(db.String(20))
    course_id = db.Column(db.Integer, nullable=False, index=True)
    yr_level = db.Column(db.String(10))
    previous_course_id = db.Column(db.String(15))
    is_oficially_enrolled = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    date_created = db.Column(db.String(40))
    CreatedBy = db.Column(db.String(50))
    date_updated = db.Column(db.String(50))
    sy_id = db.Column(db.Integer, nullable=False, index=True)
    semester_id = db.Column(db.Integer, nullable=False, index=True)


class Tblsubject(db.Model):
    __tablename__ = 'tblsubjects'

    subject_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.ForeignKey('tblcourses.course_id'), nullable=False, index=True)
    subject = db.Column(db.String(45), nullable=False, index=True)
    description = db.Column(db.String(125), nullable=False)
    units = db.Column(db.String(5), nullable=False)
    lecture_units = db.Column(db.String(5), nullable=False)
    laboratory_units = db.Column(db.String(5), nullable=False)
    lecture_fee = db.Column(db.Float(8, True), nullable=False)
    laboratory_fee = db.Column(db.Float(8, True), nullable=False)
    laboratory_category = db.Column(db.String(25))
    is_auto = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_des_use = db.Column(db.Integer, server_default=db.FetchedValue())
    date_created = db.Column(db.String(45), nullable=False)
    created_by = db.Column(db.String(20), nullable=False)
    modified_date = db.Column(db.String(45))
    modified_by = db.Column(db.String(20))

    course = db.relationship('Tblcourse', primaryjoin='Tblsubject.course_id == Tblcourse.course_id',
                             backref='tblsubjects')


class Tblsubjectschedule(db.Model):
    __tablename__ = 'tblsubjectschedule'

    schedule_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.ForeignKey('tblsubjects.subject_id'), nullable=False, index=True)
    offer_subject_id = db.Column(db.Integer, nullable=False)
    _class = db.Column('class', db.String(10), nullable=False)
    instructor_id = db.Column(db.ForeignKey('tbl_instructor.instructor_id'), nullable=False, index=True)
    days = db.Column(db.String(15), nullable=False)
    room_id = db.Column(db.ForeignKey('tblrooms.room_id'), nullable=False, index=True)
    time_in = db.Column(db.String(25), nullable=False)
    time_out = db.Column(db.String(25), nullable=False)
    school_year_id = db.Column(db.ForeignKey('tbl_school_year.school_year_id'), nullable=False, index=True)
    semester_id = db.Column(db.ForeignKey('tblsemester.semester_id'), nullable=False, index=True)
    date_created = db.Column(db.String(25), nullable=False)
    created_by = db.Column(db.String(20), nullable=False)
    date_modified = db.Column(db.String(25))
    modified_by = db.Column(db.String(20))

    instructor = db.relationship('TblInstructor',
                                 primaryjoin='Tblsubjectschedule.instructor_id == TblInstructor.instructor_id',
                                 backref='tblsubjectschedules')
    room = db.relationship('Tblroom', primaryjoin='Tblsubjectschedule.room_id == Tblroom.room_id',
                           backref='tblsubjectschedules')
    school_year = db.relationship('TblSchoolYear',
                                  primaryjoin='Tblsubjectschedule.school_year_id == TblSchoolYear.school_year_id',
                                  backref='tblsubjectschedules')
    semester = db.relationship('Tblsemester', primaryjoin='Tblsubjectschedule.semester_id == Tblsemester.semester_id',
                               backref='tblsubjectschedules')
    subject = db.relationship('Tblsubject', primaryjoin='Tblsubjectschedule.subject_id == Tblsubject.subject_id',
                              backref='tblsubjectschedules')


class TblsysAdmin(db.Model):
    __tablename__ = 'tblsys_admin'

    user_id = db.Column(db.Integer, primary_key=True)
    StaffID = db.Column(db.ForeignKey('tblstaff.staff_id'), index=True)
    Username = db.Column(db.String(25))
    Password = db.Column(db.String(25))
    Department = db.Column(db.String(25))

    tblstaff = db.relationship('Tblstaff', primaryjoin='TblsysAdmin.StaffID == Tblstaff.staff_id',
                               backref='tblsys_admins')


class TblsysAdminAcces(db.Model):
    __tablename__ = 'tblsys_admin_access'

    access_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True)
    Rights = db.Column(db.String(50))
    IS_Id = db.Column(db.Integer, index=True)


class Tbltemp(db.Model):
    __tablename__ = 'tbltemp'

    Temp_Id = db.Column(db.Integer, primary_key=True)
    Student_Id = db.Column(db.String(100), nullable=False)
    ItemNo = db.Column(db.Integer, nullable=False)
    GroupNo = db.Column(db.Integer, nullable=False)
    FeeDescription = db.Column(db.String(100), nullable=False)
    Amount = db.Column(db.Float(8, True), nullable=False)
    AmountInWords = db.Column(db.String(255))


class Tbltempenlist(db.Model):
    __tablename__ = 'tbltempenlist'

    subject_id = db.Column(db.ForeignKey('tblsubjects.subject_id'), index=True)
    course_id = db.Column(db.ForeignKey('tblcourses.course_id'), index=True)
    year_level = db.Column(db.String(5))
    school_year_id = db.Column(db.Integer)
    semester_id = db.Column(db.Integer)
    student_id = db.Column(db.String(50))
    Remarks = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    pri_id = db.Column(db.Integer, primary_key=True)

    course = db.relationship('Tblcourse', primaryjoin='Tbltempenlist.course_id == Tblcourse.course_id',
                             backref='tbltempenlists')
    subject = db.relationship('Tblsubject', primaryjoin='Tbltempenlist.subject_id == Tblsubject.subject_id',
                              backref='tbltempenlists')


class Tbluser(db.Model):
    __tablename__ = 'tblusers'

    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.Text, nullable=False)
    PasswordHash = db.Column(db.VARBINARY(4000), nullable=False)
    PasswordSalt = db.Column(db.VARBINARY(4000), nullable=False)


class Tblzipcode(db.Model):
    __tablename__ = 'tblzipcode'

    zicode_id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.String(225))
    barangay_id = db.Column(db.String(225))


class TbyearLevelStatu(db.Model):
    __tablename__ = 'tbyear_level_status'
    __table_args__ = (
        db.Index('YearLevel', 'YearLevel', 'SubmissionStatus'),
    )

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    YearLevel = db.Column(db.Integer, primary_key=True, nullable=False)
    SubmissionStatus = db.Column(db.Integer, primary_key=True, nullable=False)


t_view_credited_subjects = db.Table(
    'view_credited_subjects',
    db.Column('credited_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('student_id', db.String(50)),
    db.Column('subject_id', db.Integer),
    db.Column('subject', db.String(45)),
    db.Column('description', db.String(125)),
    db.Column('units', db.String(5)),
    db.Column('final_grade', db.String(15))
)

t_view_curriculum_subjects = db.Table(
    'view_curriculum_subjects',
    db.Column('curriculum_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('course_id', db.Integer),
    db.Column('course_title', db.String(50)),
    db.Column('course', db.String(255)),
    db.Column('Effectivity', db.String(50)),
    db.Column('Remarks', db.String(225)),
    db.Column('subject_id', db.Integer),
    db.Column('subject', db.String(45)),
    db.Column('description', db.String(125)),
    db.Column('units', db.String(5)),
    db.Column('yr_level', db.Integer),
    db.Column('semester_id', db.Integer),
    db.Column('semester', db.String(25))
)

t_view_fullpayment = db.Table(
    'view_fullpayment',
    db.Column('charge_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('SID', db.String(50)),
    db.Column('TotalAmountPayable', db.Float(19, True)),
    db.Column('TotalBalance', db.Float(19, True)),
    db.Column('syid_ch', db.Integer),
    db.Column('sem_ch', db.Integer),
    db.Column('TotalPaidAmountWithOR', db.Float(19, True))
)

t_view_grades_subjects = db.Table(
    'view_grades_subjects',
    db.Column('grade_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('student_id', db.String(50)),
    db.Column('subject_id', db.Integer),
    db.Column('final_grade', db.String(15)),
    db.Column('subject', db.String(45)),
    db.Column('description', db.String(125)),
    db.Column('units', db.String(5)),
    db.Column('remarks', db.String(45)),
    db.Column('is_assessed', db.Integer, server_default=db.FetchedValue()),
    db.Column('school_yr_id', db.Integer),
    db.Column('semester_id', db.Integer)
)

t_view_prereq = db.Table(
    'view_prereq',
    db.Column('subject_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('subject', db.String(45)),
    db.Column('description', db.String(125)),
    db.Column('PreReq_ID', db.Integer),
    db.Column('countPre', db.BigInteger, server_default=db.FetchedValue()),
    db.Column('PreReqDES', db.String(125)),
    db.Column('PreReq_Subject_Title', db.String(45)),
    db.Column('course_id', db.Integer),
    db.Column('course_title', db.String(50))
)

t_view_prerequisitesubjects = db.Table(
    'view_prerequisitesubjects',
    db.Column('subject_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('subject', db.String(45)),
    db.Column('description', db.String(125)),
    db.Column('units', db.String(5)),
    db.Column('PreReq_ID', db.Integer),
    db.Column('PreReqDES', db.String(125)),
    db.Column('PreReq_Subject_Title', db.String(45)),
    db.Column('PreReq_Subject_Units', db.String(5)),
    db.Column('course_id', db.Integer),
    db.Column('course_title', db.String(50))
)

t_vw_studentinfo = db.Table(
    'vw_studentinfo',
    db.Column('student_id', db.String(50)),
    db.Column('Name', db.String(104)),
    db.Column('Gender', db.String(10)),
    db.Column('course_id', db.Integer, server_default=db.FetchedValue()),
    db.Column('course_title', db.String(50)),
    db.Column('BirthDate', db.String(25)),
    db.Column('FatherName', db.String(50)),
    db.Column('ParentsContactNumber', db.String(100)),
    db.Column('ParentsAddress', db.String(100)),
    db.Column('BloodType', db.String(10))
)
