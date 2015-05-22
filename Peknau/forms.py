# -*- coding: utf-8 -*-
__author__ = 'stepanov'

from flask_wtf import Form
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired

class SearchForm(Form):
    select = SelectField('Параметри пошуку', choices=[('group', u'Група'), ('lecturer', u'Викладач'), ('subject', u'Предмет')])
    text = StringField('Текст пошуку',validators=[DataRequired()])