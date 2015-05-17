# -*- coding: utf-8 -*-
__author__ = 'gareth'
from Peknau import app, db
from Peknau.model import *
from flask.ext.script import Manager, prompt_bool, Command, Option
# from Bookmarks.model import User
from sqlalchemy import create_engine

app.debug = True


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

    db.session.add(Specialty(short_form=u'ПОМ', long_form=u'Програмування обчислювальних машин'))  # 1
    db.session.add(Specialty(short_form=u'РПЗ', long_form=u'Розробка програмного забезпечення'))  # 2
    db.session.add(
        Specialty(short_form=u'КОІ', long_form=u'Комп’ютерна обробка текстової, графічної та образної інформації'))  # 3
    db.session.add(Specialty(short_form=u'КД', long_form=u'Комерційна діяльність'))  # 4
    db.session.add(Specialty(short_form=u'ЕП', long_form=u'Економіка підприємства'))  # 5
    db.session.add(Specialty(short_form=u'БО', long_form=u'Бухгалтерський облік'))  # 6
    db.session.add(Specialty(short_form=u'ІДП', long_form=u'Інформаційна діяльність підприємства'))  # 7
    db.session.add(Specialty(short_form=u'П', long_form=u'Правознавство'))  # 8
    db.session.add(Specialty(short_form=u'ПЕА',
                             long_form=u'Виробництво, обслуговування та ремонт електронної побутової апаратури'))  # 9

    db.session.add(Group(group_number=101, group_course=1, specialty_id=5))
    db.session.add(Group(group_number=102, group_course=1, specialty_id=5))
    db.session.add(Group(group_number=103, group_course=1, specialty_id=6))
    db.session.add(Group(group_number=104, group_course=1, specialty_id=4))
    db.session.add(Group(group_number=105, group_course=1, specialty_id=7))
    db.session.add(Group(group_number=107, group_course=1, specialty_id=2))
    db.session.add(Group(group_number=108, group_course=1, specialty_id=2))
    db.session.add(Group(group_number=109, group_course=1, specialty_id=9))
    db.session.add(Group(group_number=110, group_course=1, specialty_id=9))
    db.session.add(Group(group_number=111, group_course=1, specialty_id=3))
    db.session.add(Group(group_number=112, group_course=1, specialty_id=8))

    db.session.add(Group(group_number=201, group_course=2, specialty_id=5))
    db.session.add(Group(group_number=202, group_course=2, specialty_id=5))
    db.session.add(Group(group_number=203, group_course=2, specialty_id=6))
    db.session.add(Group(group_number=204, group_course=2, specialty_id=4))
    db.session.add(Group(group_number=205, group_course=2, specialty_id=7))
    db.session.add(Group(group_number=207, group_course=2, specialty_id=2))
    db.session.add(Group(group_number=208, group_course=2, specialty_id=2))
    db.session.add(Group(group_number=209, group_course=2, specialty_id=9))
    db.session.add(Group(group_number=210, group_course=2, specialty_id=9))
    db.session.add(Group(group_number=211, group_course=2, specialty_id=3))

    db.session.add(Group(group_number=437, group_course=3, specialty_id=5))
    db.session.add(Group(group_number=439, group_course=3, specialty_id=4))
    db.session.add(Group(group_number=441, group_course=3, specialty_id=6))
    db.session.add(Group(group_number=442, group_course=3, specialty_id=1))
    db.session.add(Group(group_number=443, group_course=3, specialty_id=1))
    db.session.add(Group(group_number=444, group_course=3, specialty_id=9))
    db.session.add(Group(group_number=445, group_course=3, specialty_id=9))
    db.session.add(Group(group_number=446, group_course=3, specialty_id=3))
    db.session.add(Group(group_number=447, group_course=3, specialty_id=7))

    db.session.add(Group(group_number=427, group_course=4, specialty_id=1))
    db.session.add(Group(group_number=428, group_course=4, specialty_id=1))
    db.session.add(Group(group_number=429, group_course=4, specialty_id=9))
    db.session.add(Group(group_number=430, group_course=4, specialty_id=9))
    db.session.add(Group(group_number=431, group_course=4, specialty_id=3))

    db.session.add(Group(group_number=201, group_course=5, specialty_id=5))
    db.session.add(Group(group_number=202, group_course=5, specialty_id=5))
    db.session.add(Group(group_number=301, group_course=5, specialty_id=5))
    db.session.add(Group(group_number=302, group_course=5, specialty_id=5))
    db.session.add(Group(group_number=450, group_course=5, specialty_id=5))

    db.session.add(Lecturer(first_name=u"Наталія", middle_name=u"Анатоліївна", last_name=u"Рябчук"))

    db.session.add(Subject(name=u"Математичні методи дослідження операцій"))  # 1
    db.session.add(Subject(name=u"Інженерна та комп'ютерна графіка"))  # 2
    db.session.add(Subject(name=u"Конструювання програмного забеспечення", lecturer_id=1))  # 3
    db.session.add(Subject(name=u"Людино-машинний інтерфейс"))  # 4
    db.session.add(Subject(name=u"Основи менеджменту і макретингу"))  # 5
    db.session.add(Subject(name=u"Веб-дизайн"))  # 6
    db.session.add(Subject(name=u"Економіка і планування виробництва"))  # 7
    db.session.add(Subject(name=u"Проектний практикум"))  # 8
    db.session.add(Subject(name=u"Охорона праці в галузі"))  # 9
    db.session.add(Subject(name=u"Проектування автоматизованих інформаційних систем"))  # 10

    db.session.add(Monday(week=1, group_id=Group.get_group_by_number(427).id, lesson_three=1, lesson_four=2))
    db.session.add(
        Tuesday(week=1, group_id=Group.get_group_by_number(427).id, lesson_one=3, lesson_two=4, lesson_three=5,
                lesson_four=6))
    db.session.add(
        Wednesday(week=1, group_id=Group.get_group_by_number(427).id, lesson_one=2, lesson_two=1, lesson_three=3))
    db.session.add(
        Thursday(week=1, group_id=Group.get_group_by_number(427).id, lesson_two=6, lesson_three=7, lesson_four=10))
    db.session.add(
        Friday(week=1, group_id=Group.get_group_by_number(427).id, lesson_two=8, lesson_three=3, lesson_four=9))

    db.session.commit()
    print("Initialized the database")


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print("Dropped the database")


if __name__ == '__main__':
    manager.run()
