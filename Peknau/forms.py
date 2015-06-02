# -*- coding: utf-8 -*-
__author__ = 'stepanov'

from flask_wtf import Form
from wtforms import SelectField,StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Length,NumberRange

class SearchForm(Form):
    select = SelectField('Параметри пошуку', choices=[('group', u'Група'), ('lecturer', u'Викладач'), ('subject', u'Предмет')])
    text = StringField('Текст пошуку',validators=[DataRequired()])

class LoginForm(Form):
    username = StringField(u'Логін',validators=[DataRequired(),Length(min=4,max=10)])
    password = PasswordField(u'Пароль',validators=[DataRequired(),Length(min=4)])

class SpecialtyForm(Form):
    long_form = StringField(u'Повна форма', validators=[DataRequired(message=u'Введіть повну назву спеціальності')])
    short_form = StringField(u'Скорочена форма',validators=[DataRequired(message=u'Це поле обов’язкове'),Length(max=3,message=u'Скорочена форма не може перевищувати 3 символів')])
    submit = SubmitField(u'Оновити')

class SubjectForm(Form):
    title = StringField(u'Назва предмету',validators=[DataRequired(message=u'Введіть назву предмету')])
    submit = SubmitField(u'Оновити')

class GroupForm(Form):
    group_number = IntegerField(u'Номер групи',validators=[DataRequired(message=u'Введіть номер групи'),NumberRange(max=999,message=u'Можна ввести не більше 3 цифр')])
    group_course = SelectField(u'Курс',choices=[(1,u'Перший курс'),(2,u'Другий курс'),(3,u'Третій курс'),(4,u'Четвертий курс'),(5,u'Бакалаврат')],coerce=int)
    group_specialty = SelectField(u'Спеціальність групи',coerce=int)
    submit = SubmitField(u'Оновити')