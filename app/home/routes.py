from datetime import date, time
from app.home import blueprint
from flask import render_template
from app.data_crawler import india_c19_dataAll
import json


@blueprint.route('/')
def index():
    today = date.today()

    datestr = today.strftime("%a %d %B %Y")

    a, b, c, l, ch_act, ch_con, ch_rec, ch_dec, abb, high_fall_infect, states = india_c19_dataAll.crawl('Kerala')

    return render_template('index.html', status=c, districts=a, data=b, today=datestr, live=l, ch_act=ch_act,
                           ch_con=ch_con, ch_rec=ch_rec, ch_dec=ch_dec, distabr=abb, TopRated=high_fall_infect,
                           states=states, state_title='Kerala')


@blueprint.route('/<sname>')
def state(sname):
    today = date.today()

    datestr = today.strftime("%a %d %B %Y")

    a, b, c, l, ch_act, ch_con, ch_rec, ch_dec, abb, high_fall_infect, states = india_c19_dataAll.crawl(sname)

    return render_template('index.html', status=c, districts=a, data=b, today=datestr, live=l, ch_act=ch_act,
                           ch_con=ch_con, ch_rec=ch_rec, ch_dec=ch_dec, distabr=abb, TopRated=high_fall_infect,
                           states=states, state_title=sname)


@blueprint.route('/<template>')
def route_template(template):
    return render_template(template + '.html')
