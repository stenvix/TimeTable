import datetime

__author__ = 'gareth'
from Peknau import app
from flask import render_template, flash, redirect, url_for, request
from model import Group

def get_week():
    start = datetime.date(datetime.date.today().year-1,9,1);
    start_week = start.isocalendar()[1]
    now = datetime.date.today()
    now_week = now.isocalendar()[1]
    if  start_week%2==now_week%2:
        return 1
    else:
        return 2

@app.route('/groups')
@app.route('/index')
@app.route('/')
def index():
    return render_template('groups.html', group=Group.get_course_groups(1), all_groups=Group.get_all_groups(),current_week=get_week())

@app.route('/groups/<int:group_number>/<int:week>')
def group_timetable(group_number,week):
    return render_template('timetable.html', group=Group.get_group_by_number(group_number), week=week)

