import json
import operator
from datetime import date
from pip._vendor import urllib3
from config import config_dict


def jconnection(url):
    try:
        http = urllib3.PoolManager()
        weburl = http.request('GET', url)
        data = weburl.data.decode('utf-8')

    except urllib3.exceptions:
        print('Error')
        # return j_data, j_data1
    return data


def json_connection():
    try:
        urldata = 'https://api.covid19india.org/state_district_wise.json'

        data = jconnection(urldata)
        j_datax = json.loads(data)

        # http = urllib3.PoolManager()
        urldata1 = 'https://api.covid19india.org/districts_daily.json'

        data1 = jconnection(urldata1)
        j_datax2 = json.loads(data1)
    except urllib3.exceptions:
        print('Error')
    # return j_data, j_data1
    return j_datax, j_datax2


def crawl_USA():
    print('USA - STATUS')


def local_json():
    data = open('state_district_wise.json', 'r')
    jdata = json.loads(data.read(), encoding='utf-8')

    data1 = open('districts_daily.json', 'r')
    jdata1 = json.loads(data1.read(), encoding='utf-8')
    return jdata, jdata1


def crawl(state='Kerala'):
    if config_dict['LOCAL_MODE'] is True:
        j_data, j_data1 = local_json()
    else:
        j_data, j_data1 = json_connection()

    state_names = list(j_data.keys())

    def filter_dist_data(data_pack, dname):
        active_count = data_pack[dname]["active"]
        confirmed_count = data_pack[dname]["confirmed"]
        recovered_count = data_pack[dname]["recovered"]
        deceased_count = data_pack[dname]["deceased"]
        return active_count, confirmed_count, recovered_count, deceased_count

    def get_state_data(state):

        d_data = j_data[state]["districtData"]

        d_data1 = {k: v for k, v in j_data[state]["districtData"].items() if k == 'Kannur'}
        print(d_data1)
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

        high_fall_infect = sorted(all_sorted, key=lambda x: all_sorted[x]['active'], reverse=True)

        abbre = [str(k[:3]).upper() for k in all_sorted.keys()]

        chart_act_all = []
        chart_con_all = []
        chart_rec_all = []
        chart_dec_all = []
        # print('-----')
        for x in d_names:
            chart_act_all.append(all_sorted[x]['active'])
            chart_con_all.append(all_sorted[x]['confirmed'])
            chart_rec_all.append(all_sorted[x]['recovered'])
            chart_dec_all.append(all_sorted[x]['deceased'])

        tdy_source = {k: v1 for (k, v) in j_data1['districtsDaily'][state].items() for v1 in v for (k2, v2) in
                      v1.items()
                      if v2 == str(date.today())}

        tdy = {}
        tdy_active = list({int(v1) for (k, v) in tdy_source.items() for (k1, v1) in v.items() if k1 == "active"})
        tdy_confirmed = list({int(v1) for (k, v) in tdy_source.items() for (k1, v1) in v.items() if k1 == "confirmed"})
        tdy_recovered = list({int(v1) for (k, v) in tdy_source.items() for (k1, v1) in v.items() if k1 == "recovered"})
        tdy_deceased = list({int(v1) for (k, v) in tdy_source.items() for (k1, v1) in v.items() if k1 == "deceased"})
        if len(tdy_active) > 0:
            tdy["active"] = (tdy_active[len(tdy_active) - 1])
            # print(tdy_active)
            tdy["recovered"] = tdy_recovered[len(tdy_recovered) - 1]
            tdy["confirmed"] = tdy_confirmed[len(tdy_confirmed) - 1]
            tdy["deceased"] = tdy_deceased[len(tdy_deceased) - 1]

        return d_names, dist_filtered_data, status, tdy, chart_act_all, chart_con_all, chart_rec_all, chart_dec_all, abbre, high_fall_infect

    districts, data, stat, live, act, con, rec, death, abr, high_fall_infect = get_state_data(state)

    return districts, data, stat, live, act, con, rec, death, abr, high_fall_infect, state_names
