# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.reports import blueprint
from flask import render_template, request, flash, redirect, url_for
import os
import pandas as pd

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
    date = form.get('date')
    formula = form.get('formula')
    amount = form.get('amount')
    comment = form.get('comment')

    df = pd.DataFrame({'Titulo Reporte':title, 'Nombre Tutor':first_name_tutor, 'Apellidos Tutor':last_name_tutor
                       , 'Nombre Niño':first_name_kid, 'Apellidos Nino':last_name_kid, 'Fecha de nacimiento':date, 
                       'Tipo de ONI Formula':formula,'Cantidad de ONI Formula':amount, 'Comentarios':comment}, index=[0])

    df.to_csv(filename, index=False)
    return render_template('home/index.html',success=True)
