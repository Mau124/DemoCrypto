# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps import db
from apps.reports import blueprint
from flask import render_template, request, send_file, flash, redirect, url_for
import os
import pandas as pd
from datetime import datetime
import requests
import json

@blueprint.get('/generate')
def generate_get():
    return render_template('home/reports.html')

@blueprint.post('/generate')
def generate_post():
    url = "http://127.0.0.1:5000/eSignatureApi/v1/generateSignature"

    form = request.form

    title = form.get('title')

    relative_path = f'/files/{title}.csv'

    dirname = os.path.dirname(__file__)
    abs_path = os.path.join(dirname, f'../{relative_path}')

    first_name_tutor = form.get('first_name_tutor')
    last_name_tutor  = form.get('last_name_tutor')
    first_name_kid = form.get('first_name_kid')
    last_name_kid  = form.get('last_name_kid')
    date = datetime.strptime(form.get('date'), '%m/%d/%Y')
    formula = form.get('formula')
    amount = form.get('amount')
    comment = form.get('comment')
    
    df = pd.DataFrame({'Titulo Reporte':title, 'Nombre Tutor':first_name_tutor, 'Apellidos Tutor':last_name_tutor
                       , 'Nombre Niño':first_name_kid, 'Apellidos Nino':last_name_kid, 'Fecha de nacimiento':date, 
                       'Tipo de ONI Formula':formula,'Cantidad de ONI Formula':amount, 'Comentarios':comment}, index=[0])

    df.to_csv(abs_path, index=False)

    payload = {'private_key': 'c7c05166985bddca9ad8987f0e52813d98a55789f614368481ac7dfa33f624aa'}
    files=[('file',(f'{title}.csv',open(abs_path,'rb'),'text/csv'))]
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    print(response.text)

    from apps.authentication.models import Reports
    reports = Reports()
    reports.name = title
    reports.date = date
    reports.url = relative_path
    reports.comments = comment
    reports.username = "tom"
    reports.signature = response.text
    
    db.session.add(reports)
    db.session.commit()

    return render_template('home/index.html',success=True)

@blueprint.route('/download/<path:url_file>/<string:signature>')
def download_report(url_file, signature=None):
    print(url_file)
    url = "http://127.0.0.1:5000/eSignatureApi/v1/verify"

    payload = {'signature': signature, 'public_key': '12c27ef5e36e8a7358871feb6dd4521a8b584cbdd3a6600278eac8fcd93f97d73f71fc0025bf7df43ff5b1e0c193886f8e6d995959bc2f39bb34e2beb45165a1'}
    files=[('file',('',open(url_file,'rb'),'text/csv'))]
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    json_data = json.loads(response.text)

    is_valid = json_data['result']
    print(json_data['result'])

    if is_valid:
        return send_file(url_file, as_attachment=True)
    else:
        return render_template('home/index.html',is_valid=True) 