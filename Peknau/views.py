# -*- coding: utf-8 -*-
__author__ = 'gareth'

import datetime

from Peknau import app
from flask import render_template, flash, redirect, url_for, request, g
from models import Group, Specialty
from forms import SearchForm


def get_week():
    start = datetime.date(datetime.date.today().year - 1, 9, 1);
    start_week = start.isocalendar()[1]
    now = datetime.date.today()
    now_week = now.isocalendar()[1]
    if start_week % 2 == now_week % 2:
        return 1
    else:
        return 2


@app.before_request
def before_request():
    g.search_form = SearchForm()


@app.route('/groups')
@app.route('/index')
@app.route('/')
def index():
    return render_template('groups.html', all_groups=Group.get_all_groups())


@app.route('/groups/<int:group_number>')
def group_timetable(group_number):
    if request.method == 'GET':
        if request.args.get('week') == None:
            week = get_week()
        else:
            week = int(request.args.get('week'))
        return render_template('timetable.html', group=Group.get_group_by_number(group_number), week=week)
    return redirect(url_for('index'))


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/admin/specialty', methods=['POST', 'GET', 'DELETE'])
def admin_specialty():
    if request.method == 'GET':
        return render_template('specialty.html', all=Specialty.get_all_specialty())
    elif request.method == 'DELETE':
        id = request.form['id']
        Specialty.delete(id)
        return u'Спеціальність успішно видалено!'
    return 'Помилка'

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        if g.search_form.validate_on_submit():
            n = unicode(g.search_form.select.data)
            text = unicode(g.search_form.text.data)
            if n == 'group':
                if text.isalnum():
                    if text.isdigit():
                        return render_template("search_result.html", type=n,
                                               data=Group.get_group_by_number_like(int(text)),
                                               count=Specialty.count() + 1)
                    else:
                        return render_template("search_result.html", type=n, data=Group.get_by_specialty_like(text),
                                               count=Specialty.count() + 1)

                return render_template("search_result.html")
            elif n == 'lecturer':
                pass
            elif n == 'subject':
                pass
            print(g.search_form.text.data)
            return redirect(url_for('index'))
        return redirect(url_for('group_timetable', group_number=427, week=get_week()))
