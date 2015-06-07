# -*- coding: utf-8 -*-
__author__ = 'gareth'

import datetime

from Peknau import app
from flask import render_template, flash, redirect, url_for, request, g
from models import Group, Specialty, Subject, Lecturer, User, Lessons
from forms import *
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
    return render_template('groups.html', all_groups=Group.get_all())


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
                               day=datetime.date.today().weekday())
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/admin/timetable')
@login_required
def admin_timetable():
    pass


@app.route('/admin/<string:what>/update/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_update(what, id):
    if what == 'specialty':
        form = SpecialtyForm()
        tmp = Specialty.get_by_id(id)
        if form.validate_on_submit():
            tmp.long_form = form.long_form.data
            tmp.short_form = form.short_form.data
            Specialty.update(tmp)
            flash(u'Спеціальність успішно оновлено!')
            return redirect_back('admin_specialty')
        elif request.method=='POST':
            next = get_redirect_target()
            return render_template('admin_update.html', form=form, type=what, id=id, next=next)
        else:
            form.long_form.data = tmp.long_form
            form.short_form.data = tmp.short_form
            next = get_redirect_target()
            return render_template('admin_update.html', form=form, type=what, id=id, next=next)
    if what == 'subject':
        form = SubjectForm()
        tmp = Subject.get_by_id(id)
        if form.validate_on_submit():
            tmp.title = form.title.data
            Subject.update(tmp)
            flash(u'Предмет успішно оновлено!')
            return redirect_back('admin_subject')
        elif request.method=='POST':
            next = get_redirect_target()
            return render_template('admin_update.html', form=form, type=what, id=id, next=next)
        else:
            form.title.data = tmp.title
            next = get_redirect_target()
            return render_template('admin_update.html', form=form, type=what, id=id, next=next)
    if what == 'group':
        form = GroupForm()
        form.group_specialty.choices=[(h.id,h.long_form)for h in Specialty.get_all()]
        tmp = Group.get_by_id(id)
        if form.validate_on_submit():
            tmp.group_number = form.group_number.data
            tmp.group_course = form.group_course.data
            tmp.specialty_id = form.group_specialty.data
            Group.update(tmp)
            flash(u'Групу упішно оновлено!')
            return redirect_back('admin_group')
        elif request.method=='POST':
            next = get_redirect_target()
            return render_template('admin_update.html',form=form, type=what, id=id, next=next)
        else:
            form.group_number.data = tmp.group_number
            form.group_course.data = tmp.group_course
            form.group_specialty.data = tmp.specialty_id
            next = get_redirect_target()
            return render_template('admin_update.html',form=form, type=what, id=id, next=next)
    if what == 'lecturer':
        form = LecturerForm()
        form.lessons.choices = [(h.id,h.title)for h in Subject.get_all()]
        tmp = Lecturer.get_by_id(id)

        if form.validate_on_submit():
            tmp.first_name = form.first_name.data
            tmp.middle_name = form.middle_name.data
            tmp.last_name = form.last_name.data
            Lecturer.update(tmp)
            Lessons.add(id,form.lessons.data)
            flash(u'Дані викладача успішно оновлено!')
            return redirect_back('admin_lecturer')
        elif request.method =='POST':
            next = get_redirect_target()
            return render_template('admin_update.html',form = form,type=what,id=id,next = next)
        else:
            form.lessons.data = [h.id for h in tmp.subjects]
            form.first_name.data = tmp.first_name
            form.middle_name.data = tmp.middle_name
            form.last_name.data = tmp.last_name
            next=get_redirect_target()
            return render_template('admin_update.html',form = form,type=what,id=id,next = next)


@app.route('/admin/<string:what>/delete/<int:id>')
@login_required
def admin_delete(what, id):
    if what == 'specialty':
        Specialty.delete(id)
        flash(u"Спеціальність успішно видалено!")
        return redirect(url_for('admin_specialty'))
    if what == 'subject':
        Subject.delete(id)
        flash(u"Предмет успішно видалено!")
        return redirect(url_for('admin_subject'))
    if what == 'group':
        Group.delete(id)
        flash(u'Групу успішно видалено!')
        return redirect(url_for('admin_group'))
    if what == 'lecturer':
        Lecturer.delete(id)
        flash(u'Викладача успішно видалено!')
        return redirect(url_for('admin_lecturer'))


@app.route('/admin/groups',methods=['GET','POST'])
@login_required
def admin_group():
    form = GroupForm()
    form.group_specialty.choices=[(h.id,h.long_form)for h in Specialty.get_all()]
    if form.validate_on_submit():
        Group.add(form.group_number.data,form.group_course.data,form.group_specialty.data)
        flash(u'Спеціальність успішно додано')
        return redirect_back('admin_group')
    return render_template('admin_group.html', data=Group.get_all(), form=form)


@app.route('/admin/specialty', methods=['GET', 'POST'])
@login_required
def admin_specialty():
    form = SpecialtyForm()
    if form.validate_on_submit():
        Specialty.add(form.short_form.data, form.long_form.data)
        flash(u'Спеціальність успішно додано')
        return redirect_back('admin_specialty')
    return render_template('admin_specialty.html', data=Specialty.get_all(), form=form)


@app.route('/admin/lecturer', methods=['GET', 'POST'])
@login_required
def admin_lecturer():
    form = LecturerForm()
    form.lessons.choices = [(h.id,h.title)for h in Subject.get_all()]
    if form.validate_on_submit():
        Lecturer.add(form.first_name.data,form.middle_name.data,form.last_name.data)
        id = Lecturer.get_id_by_strict_name(form.first_name.data,form.middle_name.data,form.last_name.data)
        Lessons.add(id,form.lessons.data)
        flash(u'Викладача '+form.last_name.data+' '+form.first_name.data+u' успішно додано!')
        return  redirect_back('admin_lecturer')
    return render_template('admin_lecturer.html', data=Lecturer.get_all(),form=form)


@app.route('/admin/subject', methods=['GET', 'POST'])
@login_required
def admin_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        Subject.add(form.title.data)
        flash(u'Предмет успішно додано!')
        return redirect_back('admin_subject')
    if request.method == 'GET':
        return render_template('admin_subject.html', data=Subject.get_all(), form=form)


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
