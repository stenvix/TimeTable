# -*- coding: utf-8 -*-
__author__ = 'stepanov'
from models import Subject, Lecturer
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField,DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from wtforms_components import SelectMultipleField, SelectField,DateField
from sqlalchemy.exc import SQLAlchemyError


class SearchForm(Form):
    select = SelectField('Параметри пошуку',
                         choices=[('group', u'Група'), ('lecturer', u'Викладач'), ('subject', u'Предмет')])
    text = StringField('Текст пошуку', validators=[DataRequired()])


class LoginForm(Form):
    username = StringField(u'Логін', validators=[DataRequired(), Length(min=4, max=10)])
    password = PasswordField(u'Пароль', validators=[DataRequired(), Length(min=4)])


class SpecialtyForm(Form):
    long_form = StringField(u'Повна форма', validators=[DataRequired(message=u'Введіть повну назву спеціальності')])
    short_form = StringField(u'Скорочена форма', validators=[DataRequired(message=u'Це поле обов’язкове'), Length(max=3,
                                                                                                                  message=u'Скорочена форма не може перевищувати 3 символів')])
    submit = SubmitField(u'Оновити')


class SubjectForm(Form):
    title = StringField(u'Назва предмету', validators=[DataRequired(message=u'Введіть назву предмету')])
    submit = SubmitField(u'Оновити')


class GroupForm(Form):
    group_number = IntegerField(u'Номер групи', validators=[DataRequired(message=u'Введіть номер групи'),
                                                            NumberRange(max=999,
                                                                        message=u'Можна ввести не більше 3 цифр')])
    group_course = SelectField(u'Курс', choices=[(1, u'Перший курс'), (2, u'Другий курс'), (3, u'Третій курс'),
                                                 (4, u'Четвертий курс'), (5, u'Бакалаврат')], coerce=int)
    group_specialty = SelectField(u'Спеціальність групи', coerce=int)
    submit = SubmitField(u'Оновити')


class LecturerForm(Form):
    first_name = StringField(u'Ім’я', validators=[DataRequired(message=u'Введіть ім’я')])
    middle_name = StringField(u'По-батькові', validators=[DataRequired(message=u'Введіть по батькові')])
    last_name = StringField(u'Прізвище', validators=[DataRequired(message=u'Введіть прізвище')])
    lessons = SelectMultipleField(u'Предмети', coerce=int)
    submit = SubmitField(u'Оновити')


class TimeTable(Form):
    group = SelectField(u'Група', coerce=int)
    day = SelectField(u'День тижня',
                      choices=[('monday', u'Понеділок'), ('tuesday', u'Вівторок'), ('wednesday', u'Середа'),
                               ('thursday', u'Четверг'), ('friday', u'П’ятниця'), ('saturday', u'Субота')],
                      validators=[Optional()])


class EditForm(Form):
    ch = [(0, u'Відсутній')]
    try:
        for i in Subject.get_all():
            ch.append([i.id, i.title])
    except SQLAlchemyError:
        pass
    lecturer = u'Викладач'
    try:
        lch = [(i.id, unicode(i.last_name) + ' ' + unicode(i.first_name[0]) + '.' + unicode(i.middle_name[0]) + '.') for
               i in Lecturer.get_all()]
    except SQLAlchemyError:
        lch = []
    lch.insert(0, (0, u'Відсутній'))

    one_lesson_one = SelectField(u'Перший урок', choices=ch, coerce=int,validators=[DataRequired()])
    one_lesson_one_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

    one_lesson_two = SelectField(u'Другий урок', choices=ch, coerce=int,validators=[DataRequired()])
    one_lesson_two_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

    one_lesson_three = SelectField(u'Третій урок', choices=ch, coerce=int,validators=[DataRequired()])
    one_lesson_three_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

    one_lesson_four = SelectField(u'Четвертий урок', choices=ch, coerce=int,validators=[DataRequired()])
    one_lesson_four_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

    one_lesson_five = SelectField(u'П’ятий урок', choices=ch, coerce=int,validators=[DataRequired()])
    one_lesson_five_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

    one_lesson_six = SelectField(u'Шостий урок', choices=ch, coerce=int,validators=[DataRequired()])
    one_lesson_six_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

    two_lesson_one = SelectField(u'Перший урок', choices=ch, coerce=int,validators=[DataRequired()])
    two_lesson_one_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

    two_lesson_two = SelectField(u'Другий урок', choices=ch, coerce=int,validators=[DataRequired()])
    two_lesson_two_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

    two_lesson_three = SelectField(u'Третій урок', choices=ch, coerce=int,validators=[DataRequired()])
    two_lesson_three_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

    two_lesson_four = SelectField(u'Четвертий урок', choices=ch, coerce=int,validators=[DataRequired()])
    two_lesson_four_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

    two_lesson_five = SelectField(u'П’ятий урок', choices=ch, coerce=int,validators=[DataRequired()])
    two_lesson_five_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

    two_lesson_six = SelectField(u'Шостий урок', choices=ch, coerce=int,validators=[DataRequired()])
    two_lesson_six_lecturer = SelectField(lecturer, choices=lch, coerce=int,validators=[DataRequired()])

class ReplacementForm(Form):
    group = SelectField(u'Група',validators=[DataRequired(u'Виберіть групу')])

    start = DateField(u'Дата заміни',format=u'%d-%m-%Y')
    start_lesson = StringField(u'Пара')
    start_subject = SelectField(u'Предмет',choices=[])

    finish = DateField(u'Дата перенесення',format=u'%d-%m-%Y')
    finish_lesson = SelectField(u'Пара',choices=[(1,u'1 пара'),(2,u'2 пара'),(3,u'3 пара'),(4,u'4 пара'),(5,u'5 пара'),(6,u'6 пара')])
    finish_subject = SelectField(u'Перенесено на',choices=[])