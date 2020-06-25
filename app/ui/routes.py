from app.ui import blueprint
from flask import render_template



@blueprint.route('/<template>')

def route_template(template):
    return render_template(template + '.html')
