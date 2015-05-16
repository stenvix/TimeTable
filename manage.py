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
    db.session.add(Specialty(short_form=u'Шось тут', long_form=u'Шось там'))
    db.session.add(Group(group_number=427, group_course=4, specialty_id=1))
    db.session.commit()
    print("Initialized the database")


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print("Dropped the database")


if __name__ == '__main__':
    manager.run()
