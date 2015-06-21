# -*- coding: utf-8 -*-

__author__ = 'gareth'

from Peknau import app
from flask import render_template, flash, redirect, url_for, request, g, jsonify
from models import Group, Specialty, User, Lessons, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Replacement
from forms import *
from flask.ext.login import login_user, login_required, logout_user
from urlparse import urlparse, urljoin
from num2words import num2words
import datetime


def get_week(start=None):
    if not start:
        start = datetime.date(datetime.date.today().year - 1, 9, 1)
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
        else:
            form.password.errors.append(u'Логін або пароль не вірні')
            form.username.errors.append('')

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

        group = Group.get_group_by_number(group_number)
        if group.replacement:
            for item in group.replacement:
                if item.start_subject > 0:
                    pass
                    # item.start_subject = .get_by_id(item.start_subject).title
                if item.finish_subject > 0:
                    pass
                    # item.finish_subject = Subject.get_by_id(item.finish_subject).title
                else:
                    item.finish_subject = unicode(item.finish_subject * -1) + u' пара'

        return render_template('timetable.html', group=group, week=week,
                               day=datetime.date.today().weekday())
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    return render_template('base.html')


@app.route('/admin/rest/<int:subject>')
@login_required
def admin_rest(subject):
    return jsonify(result=[(h.serialize) for h in Lessons.get_by_subject(subject)])


@app.route('/admin/timetable', methods=['GET', 'POST'])
@login_required
def admin_timetable():
    form = TimeTable()
    all_groups = Group.get_all()
    choises = []
    courses = [u'Перший курс', u'Другий курс', u'Третій курс', u'Четвертий', u'Бакалаврат']
    index = 1
    for j in courses:
        tmp = [j]
        tmp.append([(h.id, unicode(h.group_number) + '-' + h.specialty.short_form) for h in all_groups if
                    h.group_course == index])
        choises.append(tmp)
        index += 1
    form.group.choices = choises
    edit = EditForm()

    if form.validate_on_submit():
        group = form.group.data
        day = form.day.data
        item = None
        if group or group != 'None':
            item = Group.get_by_id(group)
        if day or day != 'None':
            item_day = getattr(item, day)
            if item_day != []:
                for i in item_day:
                    if i.week == 1:
                        if i.subject_one:
                            edit.one_lesson_one.data = i.subject_one.subject_id
                            edit.one_lesson_one_lecturer.data = i.subject_one.lecturer_id
                        if i.subject_two:
                            edit.one_lesson_two.data = i.subject_two.subject_id
                            edit.one_lesson_two_lecturer.data = i.subject_two.lecturer_id
                        if i.subject_three:
                            edit.one_lesson_three.data = i.subject_three.subject_id
                            edit.one_lesson_three_lecturer.data = i.subject_three.lecturer_id
                        if i.subject_four:
                            edit.one_lesson_four.data = i.subject_four.subject_id
                            edit.one_lesson_four_lecturer.data = i.subject_four.lecturer_id
                        if i.subject_five:
                            edit.one_lesson_five.data = i.subject_five.subject_id
                            edit.one_lesson_five_lecturer.data = i.subject_five.lecturer_id
                        if i.subject_six:
                            edit.one_lesson_six.data = i.subject_six.subject_id
                            edit.one_lesson_six_lecturer.data = i.subject_six.lecturer_id
                    if i.week == 2:
                        if i.subject_one:
                            edit.two_lesson_one.data = i.subject_one.subject_id
                            edit.two_lesson_one_lecturer.data = i.subject_one.lecturer_id
                        if i.subject_two:
                            edit.two_lesson_two.data = i.subject_two.subject_id
                            edit.two_lesson_two_lecturer.data = i.subject_two.lecturer_id
                        if i.subject_three:
                            edit.two_lesson_three.data = i.subject_three.subject_id
                            edit.two_lesson_three_lecturer.data = i.subject_three.lecturer_id
                        if i.subject_four:
                            edit.two_lesson_four.data = i.subject_four.subject_id
                            edit.two_lesson_four_lecturer.data = i.subject_four.lecturer_id
                        if i.subject_five:
                            edit.two_lesson_five.data = i.subject_five.subject_id
                            edit.two_lesson_five_lecturer.data = i.subject_five.lecturer_id
                        if i.subject_six:
                            edit.two_lesson_six.data = i.subject_six.subject_id
                            edit.two_lesson_six_lecturer.data = i.subject_six.lecturer_id
            return render_template('admin_timetable.html', form=form, edit=edit)
    elif request.method == 'POST' and edit.data:
        day = None
        group = None
        try:
            day = request.args.get('day')
            group = int(request.args.get('group'))
        except ValueError:
            pass
        if group != None and day != None:
            lessons = globals().get(day.capitalize()).get_by_group(group)
            while len(lessons) < 2:
                lessons.append(globals().get(day.capitalize())(week=len(lessons) + 1, group_id=group))
            for item in lessons:
                for i in range(1, 7):
                    if item.week == 1:
                        setattr(item, 'lesson_' + num2words(i), Lessons.get_id(
                            getattr(edit, unicode(num2words(1)) + '_lesson_' + unicode(num2words(i))).data,
                            getattr(edit, unicode(num2words(1)) + '_lesson_' + unicode(num2words(i)) + unicode(
                                '_lecturer')).data))
                    if item.week == 2:
                        setattr(item, 'lesson_' + num2words(i), Lessons.get_id(
                            getattr(edit, unicode(num2words(2)) + '_lesson_' + unicode(num2words(i))).data,
                            getattr(edit, unicode(num2words(2)) + '_lesson_' + unicode(num2words(i)) + unicode(
                                '_lecturer')).data))
                    globals().get(day.capitalize()).update(item)
            flash(u'Розклад успішно оновлено')
            form.day.errors = None
            form.group.errors = None
        return render_template('admin_timetable.html', form=form)
    else:
        return render_template('admin_timetable.html', form=form)


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
        elif request.method == 'POST':
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
        elif request.method == 'POST':
            next = get_redirect_target()
            return render_template('admin_update.html', form=form, type=what, id=id, next=next)
        else:
            form.title.data = tmp.title
            next = get_redirect_target()
            return render_template('admin_update.html', form=form, type=what, id=id, next=next)
    if what == 'group':
        form = GroupForm()
        form.group_specialty.choices = [(h.id, h.long_form) for h in Specialty.get_all()]
        tmp = Group.get_by_id(id)
        if form.validate_on_submit():
            tmp.group_number = form.group_number.data
            tmp.group_course = form.group_course.data
            tmp.specialty_id = form.group_specialty.data
            Group.update(tmp)
            flash(u'Групу упішно оновлено!')
            return redirect_back('admin_group')
        elif request.method == 'POST':
            next = get_redirect_target()
            return render_template('admin_update.html', form=form, type=what, id=id, next=next)
        else:
            form.group_number.data = tmp.group_number
            form.group_course.data = tmp.group_course
            form.group_specialty.data = tmp.specialty_id
            next = get_redirect_target()
            return render_template('admin_update.html', form=form, type=what, id=id, next=next)
    if what == 'lecturer':
        form = LecturerForm()
        form.lessons.choices = [(h.id, h.title) for h in Subject.get_all()]
        tmp = Lecturer.get_by_id(id)

        if form.validate_on_submit():
            tmp.first_name = form.first_name.data
            tmp.middle_name = form.middle_name.data
            tmp.last_name = form.last_name.data
            Lecturer.update(tmp)
            Lessons.add(id, form.lessons.data)
            flash(u'Дані викладача успішно оновлено!')
            return redirect_back('admin_lecturer')
        elif request.method == 'POST':
            next = get_redirect_target()
            return render_template('admin_update.html', form=form, type=what, id=id, next=next)
        else:
            form.lessons.data = [h.id for h in tmp.subjects]
            form.first_name.data = tmp.first_name
            form.middle_name.data = tmp.middle_name
            form.last_name.data = tmp.last_name
            next = get_redirect_target()
            return render_template('admin_update.html', form=form, type=what, id=id, next=next)


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


@app.route('/admin/groups', methods=['GET', 'POST'])
@login_required
def admin_group():
    form = GroupForm()
    form.group_specialty.choices = [(h.id, h.long_form) for h in Specialty.get_all()]
    if form.validate_on_submit():
        Group.add(form.group_number.data, form.group_course.data, form.group_specialty.data)
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
    form.lessons.choices = [(h.id, h.title) for h in Subject.get_all()]
    if form.validate_on_submit():
        Lecturer.add(form.first_name.data, form.middle_name.data, form.last_name.data)
        id = Lecturer.get_id_by_strict_name(form.first_name.data, form.middle_name.data, form.last_name.data)
        Lessons.add(id, form.lessons.data)
        flash(u'Викладача ' + form.last_name.data + ' ' + form.first_name.data + u' успішно додано!')
        return redirect_back('admin_lecturer')
    return render_template('admin_lecturer.html', data=Lecturer.get_all(), form=form)


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
            return redirect(url_for('index'))
        return redirect(url_for('group_timetable', group_number=427, week=get_week()))


@app.route('/admin/replacement',methods=['GET','POST'])
@login_required
def admin_replacement():
    form = ReplacementForm()
    choises = []
    courses = [u'Перший курс', u'Другий курс', u'Третій курс', u'Четвертий', u'Бакалаврат']
    index = 1
    for j in courses:
        tmp = [j]
        tmp.append([(h.id, unicode(h.group_number) + '-' + h.specialty.short_form) for h in Group.get_all() if
                    h.group_course == index])
        choises.append(tmp)
        index += 1
    form.group.choices = choises
    # form.finish_subject.choices = [(i.id,i.subject.title)for i in Lessons.get]
    if request.method == 'POST':
        Replacement.add(form.group.data,form.start.data,form.start_lesson.data,form.start_subject.data,form.finish.data,form.finish_lesson.data,form.finish_subject.data)
        flash(u'Заміну здійснено!')
    return render_template('admin_replacement.html', form=form)


@app.route('/admin/replacement/get')
@login_required
def admin_replacement_get():
    group = None
    date = None
    try:
        group = int(request.args.get('group'))
    except ValueError:
        return 'Value Error', 400
    getted = datetime.datetime.strptime(request.args.get('date'), "%d-%m-%Y").date()
    week = get_week(getted)
    lessons = globals().get(getted.strftime('%A'))
    answer = []
    if lessons:
        lessons = lessons.get_by_group(group)
        for item in lessons:
            if item.week == week:
                for i in range(0, 7):
                    if i == 0:
                        answer.append(({'id': 0,
                                        'value': 'Не визначено'}))
                        continue
                    if getattr(item, 'subject_' + unicode(num2words(i))) != None:
                        answer.append(({'id': getattr(item, 'lesson_' + unicode(num2words(i))),
                                        'value': unicode(i) + '. ' + getattr(item, 'subject_' + unicode(
                                            num2words(i))).subject.title + '(' + getattr(item, 'subject_' + unicode(
                                            num2words(i))).lecturer.last_name + ' ' +
                                                 getattr(item, 'subject_' + unicode(num2words(i))).lecturer.first_name[
                                                     0] + '. ' +
                                                 getattr(item, 'subject_' + unicode(num2words(i))).lecturer.middle_name[
                                                     0] + '.)',
                                        'number': unicode(i) }))
                    else:
                        answer.append(({'id': i * -1, 'value': unicode(i) + u' пара'}))

    return jsonify(result=answer)

@app.route('/admin/replacement/get_group')
@login_required
def admin_replacement_get_group():
    group = None
    try:
        group = int(request.args.get('group'))
    except ValueError:
        return 'Value Error', 400
    all = Group.get_all_subjects(group)
    answer = []
    for item in all:
        check = True
        for j in answer:
            if item.id == j.get('id'):
                check = False

        if check:
            answer.append(({'id':item.id,'value': item.subject.title}))

    return jsonify(result = answer)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(401)
def page_not_found(error):
    return render_template('404.html'), 401
