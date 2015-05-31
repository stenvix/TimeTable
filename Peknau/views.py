# -*- coding: utf-8 -*-
__author__ = 'gareth'

import datetime

from Peknau import app
from flask import render_template, flash, redirect, url_for, request, g
from models import Group, Specialty, Subject, Lecturer, User
from forms import SearchForm, LoginForm, SpecialtyForm
from flask.ext.login import login_user, login_required, logout_user
from urlparse import urlparse, urljoin

def get_week():
    start = datetime.date(datetime.date.today().year - 1, 9, 1);
    start_week = start.isocalendar()[1]
    now = datetime.date.today()
    now_week = now.isocalendar()[1]
    if start_week % 2 == now_week % 2:
        return 1
    else:
        return 2

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)

@app.before_request
def before_request():
    g.search_form = SearchForm()


@app.route('/groups')
@app.route('/index')
@app.route('/')
def index():
    return render_template('groups.html', all_groups=Group.get_all_groups())


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.validate(form.username.data, form.password.data)

        if user:
            login_user(user)
            if request.form['next'] != '':
                return redirect(request.form['next'])
            else:
                return redirect(url_for('admin'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/groups/<int:group_number>')
def group_timetable(group_number):
    if request.method == 'GET':
        if request.args.get('week') == None:
            week = get_week()
        else:
            week = int(request.args.get('week'))
        return render_template('timetable.html', group=Group.get_group_by_number(group_number), week=week,
                               subject=Subject.get_by_title(u'Людино-машинний інтерфейс'))
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/admin/update/<string:what>/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_update(what, id):
    if what == 'specialty':
        form = SpecialtyForm()
        sp = Specialty.get_by_id(id)
        if form.validate_on_submit():
            sp.long_form = form.long_form.data
            sp.short_form = form.short_form.data
            Specialty.update(sp)
            flash(u'Спеціальність успішно оновлено!')
            return redirect_back('admin_specialty')

        else:
            form.long_form.data = sp.long_form
            form.short_form.data = sp.short_form
            next = get_redirect_target()
            return render_template('admin_update.html', form=form, type=what,id = id,next = next)


@app.route('/admin/specialty', methods=['GET', 'DELETE','POST'])
@login_required
def admin_specialty():
    form = SpecialtyForm()
    if request.method == 'DELETE':
        id = request.form['id']
        Specialty.delete(id)
        flash(u'Спеціальність успішно видалено!')
        return 'Спеціальність успішно видалено!'
    elif form.validate_on_submit():
        Specialty.add(form.short_form.data,form.long_form.data)
        flash(u'Спеціальність успішно додано')
        return redirect_back('admin_specialty')
    return render_template('admin_specialty.html', data=Specialty.get_all(),form = form)

@app.route('/admin/lecturer',methods=['GET','DELETE'])
@login_required
def admin_lecturer():
    if request.method=='GET':
        return render_template('admin_lecturer.html', data = Lecturer.get_all())

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        if g.search_form.validate_on_submit():
            n = unicode(g.search_form.select.data)
            text = unicode(g.search_form.text.data)
            if n == 'group':
                if text.isdigit():
                    return render_template('search_result.html', type=n,
                                           data=Group.get_group_by_number_like(int(text)),
                                           count=Specialty.count() + 1)
                elif text.isalpha():
                    return render_template('search_result.html', type=n, data=Group.get_by_specialty_like(text),
                                           count=Specialty.count() + 1)
                else:
                    if text.find(' ') != -1:
                        arr = text.split(' ')
                        if arr[0].isdigit():
                            return render_template('search_result.html', type=n,
                                                   data=Group.get_by_number_and_specialty(arr[0], arr[1]),
                                                   count=Specialty.count() + 1)
                        else:
                            return render_template('search_result.html', type=n,
                                                   data=Group.get_by_number_and_specialty(arr[1], arr[0]),
                                                   count=Specialty.count() + 1)
            elif n == 'lecturer':
                if text.isalpha():
                    return render_template('search_result.html', type=n, data=Lecturer.get_by_name(text))
            elif n == 'subject':
                if text.isalnum():
                    return render_template('search_result.html', type=n, data=Subject.get_by_substring(text), text=text)
            print(g.search_form.text.data)
            return redirect(url_for('index'))
        return redirect(url_for('group_timetable', group_number=427, week=get_week()))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(401)
def page_not_found(error):
    return render_template('404.html'), 401
