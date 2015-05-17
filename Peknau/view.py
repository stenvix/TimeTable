__author__ = 'gareth'
from Peknau import app
from flask import render_template, flash, redirect, url_for, request


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
