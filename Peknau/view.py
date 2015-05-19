# -*- coding: utf-8 -*-
import datetime

__author__ = 'gareth'
from Peknau import app
from flask import render_template, flash, redirect, url_for, request, make_response
from model import Group,Specialty

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

@app.route('/groups/<int:group_number>')
def group_timetable(group_number):
    if request.method == 'GET':
        week = int(request.args.get('week'))
        print (week)
        return render_template('timetable.html', group=Group.get_group_by_number(group_number), week=week)
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/admin/specialty')
def admin_specialty():
    return render_template('specialty.html',all=Specialty.get_all_specialty())

@app.route('/admin/specialty/update')
def specialty_update(specialty_id):
    specialty.short_form = "lalka"
    Specialty.update_specialty(specialty)

@app.route('/admin/specialty/delete',methods=['POST','GET','DELETE'])
def specialty_delete():
    if request.method == 'GET':
        specialty_id = int(request.args.get('specialty_id'))
        #Specialty.delete(specialty_id)
        return redirect(url_for('admin_specialty'))
    if request.method == 'DELETE':
        data = request.form['id']
        print(data)
        print("END")
        return u'Спеціальність успішно видалено!'
    return "Ну нічого"