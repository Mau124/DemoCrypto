# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
import pyotp
from apps.authentication.models import Reports
from apps import db

@blueprint.route('/index')
@login_required
def index():
    reports = db.session.query(Reports).all()

    
    return render_template('home/index.html', segment='index', reports=reports)

@blueprint.get('/login_2fa')
def login_2fa():

    # Detect the current page
    segment = get_segment(request)
    secret = 'M23RCSMWMLSZJTICTXSRC2OKG6X7NZXR'

    return render_template('accounts/login_2fa.html', segment=segment, secret=secret)

@blueprint.post('/login_2fa')
def login_2fa_post():
    
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid", "success")
        return redirect(url_for("home_blueprint.index"))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("home_blueprint.login_2fa"))


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
