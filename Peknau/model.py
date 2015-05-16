__author__ = 'Stepanov Valentin'
# Import
from Peknau import db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    group_number = db.Column(db.Integer, nullable=False)
    group_course = db.Column(db.Integer, nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey("specialty.id"))

class Specialty(db.Model):
    __tablename__ = 'specialty'
    id = db.Column(db.Integer, primary_key=True)
    short_form = db.Column(db.Unicode, nullable=False)
    long_form = db.Column(db.Unicode, nullable=False)
    group = db.relationship('Group', backref='specialty')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText,nullable=False)
    lecturer_id  = db.Column(db.Integer,db.ForeignKey("lecturer.id"))
    lecturer = db.relationship('Lecturer', backref='subjects')


class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    initials = db.Column(db.UnicodeText,nullable=False)

class Day(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = db.Column(db.Integer, primary_key=True)
    @declared_attr
    def group_id(cls):
        return db.Column(db.Integer,db.ForeignKey("group.id"))
    @declared_attr
    def group(cls):
        return db.relationship('Group',backref = cls.__name__.lower())

    @declared_attr
    def lesson_one(cls):
        return  db.Column(db.Integer,db.ForeignKey("subject.id"))

    @declared_attr
    def lesson_two(cls):
        return  db.Column(db.Integer,db.ForeignKey("subject.id"))

    @declared_attr
    def lesson_three(cls):
        return  db.Column(db.Integer,db.ForeignKey("subject.id"))

    @declared_attr
    def lesson_four(cls):
        return  db.Column(db.Integer,db.ForeignKey("subject.id"))

    @declared_attr
    def lesson_five(cls):
        return  db.Column(db.Integer,db.ForeignKey("subject.id"))

    @declared_attr
    def lesson_six(cls):
        return  db.Column(db.Integer,db.ForeignKey("subject.id"))

    @declared_attr
    def subject_one(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_one])
    def subject_two(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_two])

    @declared_attr
    def subject_three(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_one])
    def subject_four(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_two])

    @declared_attr
    def subject_five(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_one])
    def subject_six(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_two])


class Monday(Day,db.Model):
    pass

class Tuesday(Day,db.Model):
    pass

class Wednesday(Day,db.Model):
    pass

class Thursday(Day,db.Model):
    pass

class Friday(Day,db.Model):
    pass

class Saturday(Day,db.Model):
    pass
