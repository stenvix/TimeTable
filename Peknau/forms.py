# -*- coding: utf-8 -*-
__author__ = 'stepanov'

from flask_wtf import Form
from wtforms import SelectField,StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length

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