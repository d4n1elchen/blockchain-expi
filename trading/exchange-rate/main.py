from pprint import pprint
import json, requests
import time

while(True):
    coindesk_twd = "http://api.coindesk.com/v1/bpi/currentprice/TWD.json"
    resp = requests.get(url=coindesk_twd)
    data = json.loads(resp.text)
    btc_twd = data["bpi"]["TWD"]["rate_float"]
    btc_usd = data["bpi"]["USD"]["rate_float"]

    coindesk_jpy = "http://api.coindesk.com/v1/bpi/currentprice/JPY.json"
    resp = requests.get(url=coindesk_jpy)
    data = json.loads(resp.text)
    btc_jpy = data["bpi"]["JPY"]["rate_float"]

    coindesk_cny = "http://api.coindesk.com/v1/bpi/currentprice/CNY.json"
    resp = requests.get(url=coindesk_cny)
    data = json.loads(resp.text)
    btc_cny = data["bpi"]["CNY"]["rate_float"]

    openexchange = "https://openexchangerates.org/api/latest.json"
    params = dict(
        app_id="7d1c7c920b474b81b025ede2264952b5",
    )
    resp = requests.get(url=openexchange, params=params)
    data = json.loads(resp.text)

    usd_twd = data["rates"]["TWD"]
    usd_jpy = data["rates"]["JPY"]
    usd_cny = data["rates"]["CNY"]

    pprint(btc_twd/usd_twd);
    pprint(btc_cny/usd_cny);
    pprint(btc_jpy/usd_jpy);
    pprint(btc_usd);
    print("");

    time.sleep(1);
