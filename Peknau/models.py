from lib2to3.pytree import Base

__author__ = 'Stepanov Valentin'
# Import
from Peknau import db, login_manager
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref
from datetime import datetime
from num2words import num2words

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
    def add(username, password, email):
        db.session.add(User(username=username, password=password, email=email))
        db.commit()

    @staticmethod
    def validate(username, password):
        return User.query.filter_by(username=username, password=password).first()

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

    def __init__(self, group_number, group_course, specialty_id):
        self.group_number = group_number
        self.group_course = group_course
        self.specialty_id = specialty_id

    @staticmethod
    def add(group_number, group_course, specialty_id):
        db.session.add(Group(group_number, group_course, specialty_id))
        db.session.commit()

    @staticmethod
    def delete(group_id):
        db.session.delete(Group.get_by_id(group_id))
        db.session.commit()

    @staticmethod
    def update(group):
        db.session.add(group)
        db.session.commit()

    @staticmethod
    def get_by_id(group_id):
        return Group.query.get(group_id)

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
    def get_all():
        return Group.query.order_by(Group.group_course, Group.group_number).all()

    @staticmethod
    def get_by_number_and_specialty(number, specialty):
        return Group.query.join(Specialty).filter(Group.group_number.like('%' + number + '%'),
                                                  Specialty.short_form.like('%' + specialty.upper() + '%')).all()
    @staticmethod
    def get_all_subjects(group_id):
        lessons = []
        group = Group.get_by_id(group_id)
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        for day in days:
            for item in getattr(group,day):
                for i in range(1,7):
                    if getattr(item,'lesson_'+ num2words(i))!=None or getattr(item,'lesson_'+ num2words(i)) > 0:
                        lessons.append(Lessons.query.get(getattr(item,'lesson_'+ num2words(i))))
        return lessons


class Specialty(db.Model):
    __tablename__ = 'specialty'
    id = db.Column(db.Integer, primary_key=True)
    short_form = db.Column(db.Unicode, nullable=False)
    long_form = db.Column(db.Unicode, nullable=False)
    group = db.relationship('Group', backref='specialty', cascade="save-update, merge, delete")

    def __init__(self, short_form, long_form):
        self.short_form = short_form
        self.long_form = long_form

    @staticmethod
    def add(short_form, long_form):
        tmp = Specialty(short_form, long_form)
        db.session.add(tmp)
        db.session.commit()

    @staticmethod
    def get_all():
        return Specialty.query.order_by(Specialty.long_form).all()

    @staticmethod
    def get_by_id(specialty_id):
        return Specialty.query.get(specialty_id)

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


class Lessons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship("Subject")
    lecturer = db.relationship("Lecturer")

    def __init__(self, lecturer_id, subject_id):
        self.lecturer_id = lecturer_id
        self.subject_id = subject_id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'lecturer': self.lecturer_id,
            'subject': self.subject_id
        }

    @staticmethod
    def get_by_subject(subject_id):
        return Lessons.query.filter_by(subject_id=subject_id).all()

    @staticmethod
    def get_id(subject_id, lecturer_id):
        id = None
        if subject_id != 0 and lecturer_id != 0:
            tmp = Lessons.query.filter(Lessons.subject_id == subject_id, Lessons.lecturer_id == lecturer_id).first()
            id = tmp.id
        return id

    @staticmethod
    def add(lecturer_id, subjects):
        all = Lessons.query.filter_by(lecturer_id=lecturer_id).all()
        all_dict = []
        for i in all:
            all_dict.append(i.subject_id)

        delete = set(all_dict).difference(set(subjects))

        for i in delete:
            Lessons.query.filter(Lessons.lecturer_id == lecturer_id, Lessons.subject_id == i).delete()

        for i in subjects:
            if i not in all_dict:
                db.session.add(Lessons(lecturer_id, i))
        db.session.commit()


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText, nullable=False)
    lecturers = db.relationship("Lecturer",
                                secondary="lessons", backref=db.backref('subjects', lazy='joined'))

    def __init__(self, title):
        self.title = title

    @staticmethod
    def add(title):
        db.session.add(Subject(title))
        db.session.commit()

    @staticmethod
    def get_by_title(title):
        return Subject.query.filter_by(title=title).first()

    @staticmethod
    def get_by_substring(text):
        all = Subject.query.all()
        result = []
        for item in all:
            low_title = item.title.lower()
            if low_title.find(text.lower()) != -1:
                result.append(item)
        if len(result) != 0:
            return result
        else:
            return None

    @staticmethod
    def get_all():
        return Subject.query.order_by('title').all()

    @staticmethod
    def get_by_id(id):
        return Subject.query.get(id)

    @staticmethod
    def update(subject):
        db.session.add(subject)
        db.session.commit()

    @staticmethod
    def delete(subject_id):
        db.session.delete(Subject.get_by_id(subject_id))
        db.session.commit()


class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String, nullable=False)

    def __init__(self, first_name, middle_name, last_name):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name

    @staticmethod
    def add(first_name, middle_name, last_name):
        db.session.add(Lecturer(first_name, middle_name, last_name))
        db.session.commit()

    @staticmethod
    def update(lecturer):
        db.session.add(lecturer)
        db.session.commit()

    @staticmethod
    def delete(id):
        db.session.delete(Lecturer.query.get(id))
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Lecturer.query.get(id)

    @staticmethod
    def get_by_name(text):
        all = Lecturer.query.all()
        result = []
        for item in all:
            tmp_first = item.first_name.lower()
            tmp_last = item.last_name.lower()
            tmp_middle = item.middle_name.lower()
            if tmp_first.find(text.lower()) != -1 or tmp_last.find(text.lower()) != -1 or tmp_middle.find(
                    text.lower()) != -1:
                result.append(item)

        if len(result) != 0:
            return result
        else:
            return None

    @staticmethod
    def get_id_by_strict_name(first_name, middle_name, last_name):
        return Lecturer.query.filter(Lecturer.first_name == first_name, Lecturer.middle_name == middle_name,
                                     Lecturer.last_name == last_name).first().id

    @staticmethod
    def get_all():
        return Lecturer.query.order_by('last_name').all()


class Day(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def add(week, group_id, lesson_one, lesson_two, lesson_three, lesson_four, lesson_five, lesson_six):
        db.session.add(
            Monday(week, group_id, lesson_one, lesson_two, lesson_three, lesson_four, lesson_five, lesson_six))
        db.session.commit()

    @classmethod
    def update(cls, item):
        db.session.add(item)
        db.session.commit()

    @classmethod
    def get_by_group(cls, group_id):
        return cls.query.filter(cls.group_id == group_id).all()

    @declared_attr
    def week(cls):
        return db.Column(db.Integer, nullable=False)

    @declared_attr
    def group_id(cls):
        return db.Column(db.Integer, db.ForeignKey("group.id"))

    @declared_attr
    def group(cls):
        return db.relationship('Group', cascade="all,delete",
                               backref=backref(cls.__name__.lower(), cascade="all,delete"))

    @declared_attr
    def lesson_one(cls):
        return db.Column(db.Integer, db.ForeignKey("lessons.id"))

    @declared_attr
    def lesson_two(cls):
        return db.Column(db.Integer, db.ForeignKey("lessons.id"))

    @declared_attr
    def lesson_three(cls):
        return db.Column(db.Integer, db.ForeignKey("lessons.id"))

    @declared_attr
    def lesson_four(cls):
        return db.Column(db.Integer, db.ForeignKey("lessons.id"))

    @declared_attr
    def lesson_five(cls):
        return db.Column(db.Integer, db.ForeignKey("lessons.id"))

    @declared_attr
    def lesson_six(cls):
        return db.Column(db.Integer, db.ForeignKey("lessons.id"))

    @declared_attr
    def subject_one(cls):
        return db.relationship('Lessons', foreign_keys=[cls.lesson_one], backref=cls.__name__.lower() + u'_one',
                               cascade="save-update, merge, delete")

    @declared_attr
    def subject_two(cls):
        return db.relationship('Lessons', foreign_keys=[cls.lesson_two], backref=cls.__name__.lower() + u'_two',
                               cascade="save-update, merge, delete")

    @declared_attr
    def subject_three(cls):
        return db.relationship('Lessons', foreign_keys=[cls.lesson_three], backref=cls.__name__.lower() + u'_three',
                               cascade="save-update, merge, delete")

    @declared_attr
    def subject_four(cls):
        return db.relationship('Lessons', foreign_keys=[cls.lesson_four], backref=cls.__name__.lower() + u'_four',
                               cascade="save-update, merge, delete")

    @declared_attr
    def subject_five(cls):
        return db.relationship('Lessons', foreign_keys=[cls.lesson_five], backref=cls.__name__.lower() + u'_five',
                               cascade="save-update, merge, delete")

    @declared_attr
    def subject_six(cls):
        return db.relationship('Lessons', foreign_keys=[cls.lesson_six], backref=cls.__name__.lower() + u'_six',
                               cascade="save-update, merge, delete")


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


class Replacement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    start = db.Column(db.Date)
    start_lesson = db.Column(db.Integer)
    start_subject_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    start_subject = db.relationship('Lessons',foreign_keys=[start_subject_id])
    finish = db.Column(db.Date)
    finish_lesson = db.Column(db.Integer)
    finish_subject_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    finish_subject = db.relationship('Lessons',foreign_keys=[finish_subject_id])
    group = db.relationship('Group', backref='replacement')

    @staticmethod
    def add(group_id, start, start_lesson, start_subject_id, finish, finish_lesson, finish_subject_id):
        item = Replacement(group_id=group_id, start=start, start_lesson=start_lesson, start_subject_id=start_subject_id,
                        finish=finish, finish_lesson=finish_lesson, finish_subject_id=finish_subject_id)
        db.session.add(item)
        db.session.commit()
