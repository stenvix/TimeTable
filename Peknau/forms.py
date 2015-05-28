# -*- coding: utf-8 -*-
__author__ = 'stepanov'

from flask_wtf import Form
from wtforms import SelectField,StringField,PasswordField
from wtforms.validators import DataRequired,Length

class SearchForm(Form):
    select = SelectField('Параметри пошуку', choices=[('group', u'Група'), ('lecturer', u'Викладач'), ('subject', u'Предмет')])
    text = StringField('Текст пошуку',validators=[DataRequired()])

class LoginForm(Form):
    username = StringField(u'Логін',validators=[DataRequired(),Length(min=4,max=10)])
    password = PasswordField(u'Пароль',validators=[DataRequired(),Length(min=4)])