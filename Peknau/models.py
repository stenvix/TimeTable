

__author__ = 'Stepanov Valentin'
# Import
from Peknau import db, login_manager
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import or_, func
from sqlalchemy.orm import backref
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True, index=True)
    registered_on = db.Column(db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    @staticmethod
    def add(username,password,email):
        db.session.add(User(username=username,password=password,email=email))
        db.commit()

    @staticmethod
    def validate(username,password):
        return User.query.filter_by(username=username,password=password).first()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True


    def is_anonymous(self):
        return False


    def get_id(self):
        return unicode(self.id)


    def __repr__(self):
        return '<User %r>' % (self.username)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    group_number = db.Column(db.Integer, nullable=False)
    group_course = db.Column(db.Integer, nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey("specialty.id"))

    @staticmethod
    def get_course_groups(number):
        return Group.query.filter_by(group_course=number).all()

    @staticmethod
    def get_by_specialty(specialty):
        return Group.query.filter_by(specialty.short_form == specialty).all()

    @staticmethod
    def get_by_specialty_like(specialty):
        return Group.query.join(Specialty).filter((Specialty.short_form.like('%' + specialty.upper() + '%'))).all()

    @staticmethod
    def get_group_by_number(number):
        return Group.query.filter_by(group_number=number).first()

    @staticmethod
    def get_group_by_number_like(number):
        return Group.query.filter(Group.group_number.like('%' + str(number) + '%')).all()

    @staticmethod
    def get_all_groups():
        return Group.query.all()

    @staticmethod
    def get_by_number_and_specialty(number, specialty):
        return Group.query.join(Specialty).filter(Group.group_number.like('%' + number + '%'),
                                                  Specialty.short_form.like('%' + specialty.upper() + '%')).all()


class Specialty(db.Model):
    __tablename__ = 'specialty'
    id = db.Column(db.Integer, primary_key=True)
    short_form = db.Column(db.Unicode, nullable=False)
    long_form = db.Column(db.Unicode, nullable=False)
    group = db.relationship('Group', backref='specialty',cascade="save-update, merge, delete")

    def __init__(self,short_form,long_form):
        self.short_form = short_form
        self.long_form = long_form

    @staticmethod
    def add(short_form,long_form):
        tmp = Specialty(short_form,long_form)
        db.session.add(tmp)
        db.session.commit()

    @staticmethod
    def get_all():
        return Specialty.query.all()

    @staticmethod
    def get_by_id(specialty_id):
        return Specialty.query.filter_by(id=specialty_id).first()

    @staticmethod
    def update(specialty):
        db.session.add(specialty)
        db.session.commit()

    @staticmethod
    def delete(specialty_id):
        db.session.delete(Specialty.get_by_id(specialty_id))
        db.session.commit()

    @staticmethod
    def count():
        return Specialty.query.count()


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText, nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey("lecturer.id"))
    lecturer = db.relationship('Lecturer', backref='subjects', cascade="save-update, merge, delete")

    @staticmethod
    def get_by_title(title):
        return Subject.query.filter_by(title=title).first()

    @staticmethod
    def get_by_substring(text):
        all = Subject.query.all()
        result = []
        for item in all:
            low_title = item.title.lower()
            if low_title.find(text.lower())!=-1:
                result.append(item)
        if len(result)!=0:
            return result
        else:return None



class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String, nullable=False)

    @staticmethod
    def get_by_name(text):
        all = Lecturer.query.all()
        result = []
        for item in all:
            tmp_first = item.first_name.lower()
            tmp_last = item.last_name.lower()
            tmp_middle = item.middle_name.lower()
            if tmp_first.find(text.lower())!=-1 or tmp_last.find(text.lower())!=-1 or tmp_middle.find(text.lower())!=-1:
                result.append(item)

        if len(result)!=0:
          return result
        else:return None

    @staticmethod
    def get_all():
        return  Lecturer.query.all()


class Day(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def week(cls):
        return db.Column(db.Integer, nullable=False)

    @declared_attr
    def group_id(cls):
        return db.Column(db.Integer, db.ForeignKey("group.id"))

    @declared_attr
    def group(cls):
        return db.relationship('Group',cascade="all,delete", backref=backref(cls.__name__.lower(), cascade="all,delete"))


    @declared_attr
    def lesson_one(cls):
        return db.Column(db.Integer, db.ForeignKey("subject.id"))

    @declared_attr
    def lesson_two(cls):
        return db.Column(db.Integer, db.ForeignKey("subject.id"))

    @declared_attr
    def lesson_three(cls):
        return db.Column(db.Integer, db.ForeignKey("subject.id"))

    @declared_attr
    def lesson_four(cls):
        return db.Column(db.Integer, db.ForeignKey("subject.id"))

    @declared_attr
    def lesson_five(cls):
        return db.Column(db.Integer, db.ForeignKey("subject.id"))

    @declared_attr
    def lesson_six(cls):
        return db.Column(db.Integer, db.ForeignKey("subject.id"))

    @declared_attr
    def subject_one(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_one], backref=cls.__name__.lower() + u'_one', cascade="save-update, merge, delete")

    @declared_attr
    def subject_two(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_two], backref=cls.__name__.lower() + u'_two', cascade="save-update, merge, delete")

    @declared_attr
    def subject_three(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_three], backref=cls.__name__.lower() + u'_three', cascade="save-update, merge, delete")

    @declared_attr
    def subject_four(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_four], backref=cls.__name__.lower() + u'_four', cascade="save-update, merge, delete")

    @declared_attr
    def subject_five(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_five], backref=cls.__name__.lower() + u'_five', cascade="save-update, merge, delete")

    @declared_attr
    def subject_six(cls):
        return db.relationship('Subject', foreign_keys=[cls.lesson_six], backref=cls.__name__.lower() + u'_six', cascade="save-update, merge, delete")


class Monday(Day, db.Model):
    pass


class Tuesday(Day, db.Model):
    pass


class Wednesday(Day, db.Model):
    pass


class Thursday(Day, db.Model):
    pass


class Friday(Day, db.Model):
    pass


class Saturday(Day, db.Model):
    pass
