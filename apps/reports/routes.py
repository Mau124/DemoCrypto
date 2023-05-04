# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps import db
from apps.reports import blueprint
from flask import render_template, request, flash, redirect, url_for
import os
import pandas as pd
from datetime import datetime

@blueprint.get('/generate')
def generate_get():
    return render_template('home/reports.html')

@blueprint.post('/generate')
def generate_post():
    form = request.form

    title = form.get('title')
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, f'../files/{title}.csv')


    first_name_tutor = form.get('first_name_tutor')
    last_name_tutor  = form.get('last_name_tutor')
    first_name_kid = form.get('first_name_kid')
    last_name_kid  = form.get('last_name_kid')
    date = datetime.strptime(form.get('date'), '%m/%d/%Y')
    formula = form.get('formula')
    amount = form.get('amount')
    comment = form.get('comment')

    from apps.authentication.models import Reports
    reports = Reports()
    reports.name = title
    reports.date = date
    reports.url = filename
    reports.comments = comment
    reports.username = "tom"
    
    db.session.add(reports)
    db.session.commit()

    df = pd.DataFrame({'Titulo Reporte':title, 'Nombre Tutor':first_name_tutor, 'Apellidos Tutor':last_name_tutor
                       , 'Nombre Niño':first_name_kid, 'Apellidos Nino':last_name_kid, 'Fecha de nacimiento':date, 
                       'Tipo de ONI Formula':formula,'Cantidad de ONI Formula':amount, 'Comentarios':comment}, index=[0])

    df.to_csv(filename, index=False)
    return render_template('home/index.html',success=True)
