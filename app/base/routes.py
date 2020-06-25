from flask import jsonify, render_template, redirect, request, url_for

from app.base import blueprint


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.load'))


@blueprint.route('/<template>')
def route_template(template):
    return render_template(template + '.html')


@blueprint.route('/fixed_<template>')
def route_fixed_template(template):
    return render_template('fixed/fixed_{}.html'.format(template))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))


@blueprint.route('/index', methods=['GET', 'POST'])
def load():
     
    return redirect(url_for('home_blueprint.index'))


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500
