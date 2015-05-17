__author__ = 'gareth'
from Peknau import app
from flask import render_template, flash, redirect, url_for, request
from model import Group


@app.route('/')
@app.route('/index')
@app.route('/groups')
def groups():
    return render_template('groups.html', group=Group.get_course_groups(1), all_groups=Group.get_all_groups())


@app.route('/groups/<group_number>')
def group_timetable(group_number):
    return render_template('timetable.html', group=Group.get_group_by_number(group_number))
