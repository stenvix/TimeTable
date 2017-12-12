# -*- coding: utf-8 -*-
__author__ = 'gareth'
from Peknau import app, db
from Peknau.models import *
from flask.ext.script import Manager, prompt_bool, Command, Option, Server
import datetime



class GunicornServer(Command):
    """Run the app within Gunicorn"""

    def get_options(self):
        from gunicorn.config import make_settings

        settings = make_settings()
        options = (
            Option(*klass.cli, action=klass.action)
            for setting, klass in settings.iteritems() if klass.cli
        )
        return options

    def run(self, *args, **kwargs):
        from gunicorn.app.wsgiapp import WSGIApplication

        app = WSGIApplication()
        app.app_uri = 'manage:app'
        return app.run()


manager = Manager(app)
manager.add_command("gunicorn", GunicornServer())


@manager.command
def initdb():
    db.create_all()

    db.session.add(Specialty(short_form=u'КН', long_form=u'Комп\'ютерні науки'))  # 1
    
    db.session.add(Group(group_number=104, group_course=1, specialty_id=1))
    db.session.add(Group(group_number=214, group_course=1, specialty_id=1))
    db.session.add(Group(group_number=34, group_course=1, specialty_id=1))
    db.session.add(Group(group_number=44, group_course=1, specialty_id=1))


    db.session.add(Lecturer(first_name=u"Наталія", middle_name=u"Іванівна", last_name=u"Бокла")) # 1
    db.session.add(Lecturer(first_name=u'Євген',middle_name=u'Вікторович',last_name=u'Буров')) # 2
    db.session.add(Lecturer(first_name=u'Костянтин',middle_name=u'Констянтинович',last_name=u'Колесник'))# 3
    db.session.add(Lecturer(first_name=u'Василь',middle_name=u'Миколайович',last_name=u'Теслюк')) # 5
    db.session.add(Lecturer(first_name=u'Олег',middle_name=u'Михайлович',last_name=u'Матвійків')) # 4
    db.session.add(Lecturer(first_name=u'Юрій',middle_name=u'Юрійович',last_name=u'Ханас')) # 6
    db.session.add(Lecturer(first_name=u'Петро',middle_name=u'Ярославович',last_name=u'Пукач')) # 7
    db.session.add(Lecturer(first_name=u'Роман',middle_name=u'Теодорович',last_name=u'Панчак'))  # 8
    db.session.add(Lecturer(first_name=u'Петро',middle_name=u'Сидорович',last_name=u'Кособуцький')) # 9

    db.session.add(Subject(title=u"Технології створення програмних продуктів")) #1
    db.session.add(Subject(title=u"Компютерні мережі")) #2
    db.session.add(Subject(title=u"Теоретичні основи САПР"))  # 3
    db.session.add(Subject(title=u"Методи синтезу та оптимізації"))  # 4
    db.session.add(Subject(title=u"Математичний аналіз"))  # 5
    db.session.add(Subject(title=u"Системне програмування"))  # 6
    db.session.add(Subject(title=u"КСАК"))  # 7
    db.session.add(Subject(title=u"Адміністрування САПР"))  # 8
    db.session.add(Subject(title=u"Моделювання систем"))  # 9

    db.session.add(Lessons(subject_id=1,lecturer_id=1))
    db.session.add(Lessons(subject_id=2,lecturer_id=2))
    db.session.add(Lessons(subject_id=3,lecturer_id=3))
    db.session.add(Lessons(subject_id=4,lecturer_id=4))
    db.session.add(Lessons(subject_id=5,lecturer_id=5))
    db.session.add(Lessons(subject_id=6,lecturer_id=6))
    db.session.add(Lessons(subject_id=7,lecturer_id=7))
    db.session.add(Lessons(subject_id=8,lecturer_id=8))
    db.session.add(Lessons(subject_id=9,lecturer_id=9))

    #week
    # db.session.add(Monday(week=1, group_id=Group.get_group_by_number(427).id, lesson_three=1, lesson_four=2))
    # db.session.add(
    #     Tuesday(week=1, group_id=Group.get_group_by_number(427).id, lesson_one=3, lesson_two=4, lesson_three=5,
    #             lesson_four=6))
    # db.session.add(
    #     Wednesday(week=1, group_id=Group.get_group_by_number(427).id, lesson_one=2, lesson_two=1, lesson_three=3))
    # db.session.add(
    #     Thursday(week=1, group_id=Group.get_group_by_number(427).id, lesson_two=6, lesson_three=7, lesson_four=10))
    # db.session.add(
    #     Friday(week=1, group_id=Group.get_group_by_number(427).id, lesson_two=8, lesson_three=3, lesson_four=9))
    # db.session.add(
    #     Saturday(week=1, group_id=Group.get_group_by_number(427).id))

    # #week 2
    # db.session.add(Monday(week=2, group_id=Group.get_group_by_number(427).id, lesson_three=1, lesson_four=2))
    # db.session.add(
    #     Tuesday(week=2, group_id=Group.get_group_by_number(427).id, lesson_one=3, lesson_two=4, lesson_three=5,
    #             lesson_four=6))
    # db.session.add(
    #     Wednesday(week=2, group_id=Group.get_group_by_number(427).id, lesson_one=2, lesson_two=1, lesson_three=5))
    # db.session.add(
    #     Thursday(week=2, group_id=Group.get_group_by_number(427).id, lesson_three=7, lesson_four=10))
    # db.session.add(
    #     Friday(week=2, group_id=Group.get_group_by_number(427).id, lesson_two=8, lesson_three=3, lesson_four=9))
    # db.session.add(
    #     Saturday(week=2, group_id=Group.get_group_by_number(427).id))

    db.session.add(User(username='root',password='root',email='falken.ua@gmail.com'))
    # db.session.add(Replacement(group_id= 31,start = datetime.date(2015,06,15), start_subject = 1, finish = datetime.date(2015,06,17), finish_lesson = 4, finish_subject = 2))

    db.session.commit()
    print("Initialized the database")


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.reflect()
        db.drop_all()
        print("Dropped the database")

server = Server(host="0.0.0.0",port = 5000)
manager.add_command("runserver", server)

if __name__ == '__main__':
    manager.run()
