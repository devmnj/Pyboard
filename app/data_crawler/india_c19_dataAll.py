import json
from datetime import date, timedelta
from turtle import goto
from pip._vendor import urllib3

from pip._vendor import urllib3
from config import config_dict


def j_connection(url):
    try:
        http = urllib3.PoolManager()
        weburl = http.request('GET', url)
        data = weburl.data.decode('utf-8')
        return data

    except urllib3.exceptions:
        print('Error')
        # return j_data, j_data1
    return


def json_connection():
    try:
        urldata = 'https://api.covid19india.org/state_district_wise.json'
        data = j_connection(urldata)
        j_datax = json.loads(data)

        urldata1 = 'https://api.covid19india.org/v4/timeseries.json'
        data1 = j_connection(urldata1)
        j_datax2 = json.loads(data1)

        data3 = j_connection('https://api.covid19india.org/state_test_data.json')
        t_data = json.loads(data3)
        return j_datax, j_datax2, t_data

    except urllib3.exceptions:
        print('Error')
    # return j_data


def crawl_USA():
    print('USA - STATUS')


def local_json():
    data = open('state_district_wise.json', 'r')
    jdata = json.loads(data.read(), encoding='utf-8')
    t_series_data = json.loads(open('timeseries.json', 'r').read())
    test_data = json.loads(open('state_test_data.json', 'r').read())

    return jdata, t_series_data, test_data


def filter_dist_data(data_pack, d_name):
    active_count = data_pack[d_name]["active"]
    confirmed_count = data_pack[d_name]["confirmed"]
    recovered_count = data_pack[d_name]["recovered"]
    deceased_count = data_pack[d_name]["deceased"]
    return active_count, confirmed_count, recovered_count, deceased_count


def all_india(j_data=None, state_names=[]):
    ct = 0
    at = 0
    rt = 0
    dt = 0
    for s in state_names:
        s_data1 = j_data[s]["districtData"]

        d_names1 = list(s_data1.keys())

        dist_filtered_data1 = {}

        ct = 0
        at = 0
        rt = 0
        dt = 0
        for d in d_names1:
            a, c, r, d1 = filter_dist_data(s_data1, d)
            dist_filtered_data1[d] = {"active": a, "confirmed": c, "recovered": r, "deceased": d1}
            ct = ct + c
            at = at + a
            dt = dt + d1
            rt = rt + r
    all_ = dict({"active": at, "confirmed": ct, "recovered": rt, "deceased": dt})
    print('All India')
    print(all_)
    return all_


def test_locator(data,state, def_date):
    dt = def_date
    tst_ = []
    try:
        tst_ = [k for k in data if k['state'] == state and k['updatedon'] == dt.strftime('%d/%m/%Y')]
        if tst_.__len__() <= 0:
            dt = def_date - timedelta(days=1);
            return test_locator(data, state, dt)

        else:
            return tst_



    except:
        pass


def get_tests(test_data, state_names, state):
    today = date.today()
    y_day = today - timedelta(days=1)
    t = test_data['states_tested_data']
    tst_results = []
    tst_ = []

    tests_all = {'positive': 0, 'negative': 0, 'unconfirmed': 0, 'total_tested': 0,
                 'currently_in_quarantine': 0, 'released_from_quarantine': 0,
                 'tests_per_positive_case': 0}
    neg = 0
    pos = 0
    unc = 0
    tt = 0
    c_q = 0
    r_q = 0
    t_per_pos = 0
    for name in state_names:

        tst_ = [k for k in t if k['state'] == name and k['updatedon'] == y_day.strftime('%d/%m/%Y')]
        tst_ = test_locator(t,name, today)

        try:
            if len(str(tst_[0]['positive'])) > 0:
                pos = pos + int(tst_[0]['positive'])
            if len(str(tst_[0]['negative'])) > 0:
                neg = neg + int(tst_[0]['negative'])
            if len(str(tst_[0]['unconfirmed'])) > 0:
                unc = unc + int(tst_[0]['unconfirmed'])
            if len(str(tst_[0]['totaltested'])) > 0:
                tt = tt + int(tst_[0]['totaltested'])
            if len(str(tst_[0]['totalpeoplecurrentlyinquarantine'])) > 0:
                c_q = c_q + int(tst_[0]['totalpeoplecurrentlyinquarantine'])
            if len(str(tst_[0]['totalpeoplereleasedfromquarantine'])) > 0:
                r_q = r_q + int(tst_[0]['totalpeoplereleasedfromquarantine'])
            if len(str(tst_[0]['testsperpositivecase'])) > 0:
                t_per_pos = t_per_pos + int(tst_[0]['testsperpositivecase'])
        except:
            pass

    tests_all['positive'] = pos
    tests_all['negative'] = neg
    tests_all['unconfirmed'] = unc
    tests_all['total_tested'] = tt
    tests_all['currently_in_quarantine'] = c_q
    tests_all['released_from_quarantine'] = r_q
    tests_all['tests_per_positive_case'] = t_per_pos

    tests = {'positive': 0, 'negative': 0, 'unconfirmed': 0, 'total_tested': 0,
             'currently_in_quarantine': 0, 'released_from_quarantine': 0,
             'tests_per_positive_case': 0, 'date': ''}

    #tst_results = [k for k in t if k['state'] == state and k['updatedon'] == y_day.strftime('%d/%m/%Y')]
    tst_results = test_locator( t,state, today)

    # print('result')
    # print(tst_results)
    neg = 0
    pos = 0
    unc = 0
    tt = 0
    c_q = 0
    r_q = 0
    t_per_pos = 0
    try:
        if len(str(tst_results[0]['positive'])) > 0:
            pos = int(tst_results[0]['positive'])
        if len(str(tst_results[0]['negative'])) > 0:
            neg = int(tst_results[0]['negative'])
        if len(str(tst_results[0]['unconfirmed'])) > 0:
            unc = int(tst_results[0]['unconfirmed'])
        if len(str(tst_results[0]['totaltested'])) > 0:
            tt = int(tst_results[0]['totaltested'])
        if len(str(tst_results[0]['totalpeoplecurrentlyinquarantine'])) > 0:
            c_q = int(tst_results[0]['totalpeoplecurrentlyinquarantine'])
        if len(str(tst_results[0]['totalpeoplereleasedfromquarantine'])) > 0:
            r_q = int(tst_results[0]['totalpeoplereleasedfromquarantine'])
        if len(str(tst_results[0]['testsperpositivecase'])) > 0:
            t_per_pos = int(tst_results[0]['testsperpositivecase'])
    except:
        pass

    tests['positive'] = pos
    tests['negative'] = neg
    tests['unconfirmed'] = unc
    tests['total_tested'] = tt
    tests['currently_in_quarantine'] = c_q
    tests['released_from_quarantine'] = r_q
    tests['tests_per_positive_case'] = t_per_pos
    tests['date'] = tst_results[0]['updatedon']

    return tests, tests_all


def latest(state, t_data=[]):
    today = date.today()
    y_day = today - timedelta(days=1)
    state_dict = {'Andaman and Nicobar Islands': 'AN', 'Andhra Pradesh': 'AP',
                  'Arunachal Pradesh': 'AR', 'Assam': 'AS', 'Bihar': 'BR', 'Chandigarh': 'CH', 'Chhattisgarh': 'CT',
                  'Delhi': 'DL', 'Dadra and Nagar Haveli and Daman and Diu': 'DN', 'Goa': 'GA', 'Gujarat': 'GJ',
                  'Himachal Pradesh': 'HP', 'Haryana': 'HT', 'Jharkhand': 'JH', 'Jammu and Kashmir': 'JK',
                  'Karnataka': 'KA',
                  'Kerala': 'KL', 'Ladakh': 'LA', 'Lakshadweep': '', 'Maharashtra': 'MH', 'Meghalaya': 'ML',
                  'Manipur': 'MN',
                  'Madhya Pradesh': 'MP', 'Mizoram': 'MZ', 'Nagaland': 'NL', 'Odisha': 'OR', 'Punjab': 'PB',
                  'Puducherry': 'PY',
                  'Rajasthan': 'RJ', 'Sikkim': 'SK', 'Telangana': 'TG', 'Tamil Nadu': 'TN', 'Tripura': 'TR',
                  'Uttar Pradesh': 'UP',
                  'Uttarakhand': 'UT', 'West Bengal': 'WB'}

    tdy = []
    td_ = {'confirmed': 0, 'dead': 0, 'recovered': 0}

    # daily statistics
    try:
        tdy = t_data[state_dict[state]]['dates'][y_day.strftime('%Y-%m-%d')]['delta']
        td_['confirmed'] = tdy['confirmed']
        td_['dead'] = tdy['deceased']
        td_['recovered'] = tdy['recovered']
    except:
        pass
    tdy = t_data[state_dict[state]]['dates']
    return td_


def get_state_data(state, j_data=None):
    d_data = j_data[state]["districtData"]

    d_names = list(d_data.keys())

    dist_filtered_data = {}

    ct = 0
    at = 0
    rt = 0
    dt = 0
    for d in d_names:
        a, c, r, d1 = filter_dist_data(d_data, d)
        dist_filtered_data[d] = {"active": a, "confirmed": c, "recovered": r, "deceased": d1}
        ct = ct + c
        at = at + a
        dt = dt + d1
        rt = rt + r
    status = dict({"active": at, "confirmed": ct, "recovered": rt, "deceased": dt})

    all_sorted = {k: d_data[k] for k in sorted(d_data)}

    high_fall_ = sorted(all_sorted, key=lambda x: all_sorted[x]['active'], reverse=True)

    abbre = [str(k[:3]).upper() for k in all_sorted.keys()]

    chart_act_all = []
    chart_con_all = []
    chart_rec_all = []
    chart_dec_all = []

    for x in d_names:
        chart_act_all.append(all_sorted[x]['active'])
        chart_con_all.append(all_sorted[x]['confirmed'])
        chart_rec_all.append(all_sorted[x]['recovered'])
        chart_dec_all.append(all_sorted[x]['deceased'])

    return d_names, dist_filtered_data, status, chart_act_all, chart_con_all, chart_rec_all, chart_dec_all, abbre, high_fall_


def crawl(state='Kerala'):
    if config_dict['LOCAL_MODE'] is True:
        j_data, t_data, test_data = local_json()
    else:
        j_data, t_data, test_data = json_connection()
    today = date.today()
    y_day = today - timedelta(days=1)
    state_names = list(j_data.keys())
    districts, data, stat, act, con, rec, death, abr, high_fall_infect = get_state_data(state, j_data)
    all_ind = all_india(j_data, state_names)
    test_results, tests_all = get_tests(test_data, state_names, state)
    last = latest(state, t_data)
    return districts, data, stat, act, con, rec, death, abr, high_fall_infect, state_names, all_ind, last, test_results, tests_all
