from bittrex.bittrex import Bittrex
from time import sleep
import json
import sys

def sell(base, market, quantity, rate):
    print("Sell "+str(quantity)+"("+market+") at "+str(rate)+"("+base+")")
    order = bt.sell_limit(base+"-"+market, quantity, rate)
    if order['success']:
        sleep(0.1)
        sys.stdout.write("Wait for "+market+" being sold...")
        uuid = order['result']['uuid']
        wait = 0
        opened = bt.get_order(uuid)['result']['IsOpen']
        while opened and wait<15:
            sys.stdout.write('.')
            wait += 1
            opened = bt.get_order(uuid)['result']['IsOpen']
        print('')

        if opened:
            # bt.cancel(uuid)
            print("Failed to sell "+market)
            return False
        else:
            print("Success to sell "+market)
            return True
    else:
        raise Exception(order['message'])

def buy(base, market, quantity, rate):
    print("Buy "+str(quantity)+"("+market+") at "+str(rate)+"("+base+")")
    order = bt.buy_limit(base+"-"+market, quantity, rate)
    if order['success']:
        sleep(0.1)
        sys.stdout.write("Wait for "+market+" being bought")
        uuid = order['result']['uuid']
        wait = 0
        opened = bt.get_order(uuid)['result']['IsOpen']
        while opened and wait<15:
            sys.stdout.write('.')
            wait += 1
            opened = bt.get_order(uuid)['result']['IsOpen']
        print('')

        if opened:
            bt.cancel(uuid)
            print("Failed to buy "+market)
            return False
        else:
            print("Success to buy "+market)
            return True
    else:
        raise Exception(order['message'])

with open("secrets.json") as secrets_file:
    secrets = json.load(secrets_file)
    secrets_file.close()
bt = Bittrex(secrets['key'], secrets['secret'])

btc_balance = bt.get_balance('BTC')['result']['Balance']
print("BTC balance: "+str(btc_balance))

# markets = bt.get_markets()['result']
# eth_markets = list(filter(lambda m: m['BaseCurrency']=='ETH' and m['IsActive'], markets))

mk_name = 'ETH-ETC'
mk_curr = 'ETC'
while True:
    # for market in eth_markets:
    #     mk_name = market['MarketName']
    #     mk_curr = market['MarketCurrency']
    print("Market name: "+mk_name)

    tick_eth_cur = bt.get_ticker(mk_name)
    tick_btc_cur = bt.get_ticker('BTC-'+mk_curr)
    if tick_btc_cur['success']:
        tick_btc_eth = bt.get_ticker('BTC-ETH')
        buy_price = tick_btc_cur['result']['Ask']
        sell_price = tick_eth_cur['result']['Bid']
        sell_eth = tick_btc_eth['result']['Bid']
        print('Buy:  '+str(buy_price))
        print('Sell: '+str(sell_price*sell_eth))
        print('')
        if sell_price*sell_eth>buy_price:
            print("!!!!!!!!!!!!!!!!!!!!!!!")

            btc_in = 0.002
            q_curr = btc_in/buy_price
            if buy("BTC", mk_curr ,q_curr ,buy_price):
                if sell("ETH", mk_curr, q_curr, sell_price):
                    q_eth = q_curr*sell_price
                    if sell("BTC", "ETH", q_eth, sell_eth):
                        print("Get money! "+str(q_eth*sell_eth-btc_in)+"(BTC)")
                    else:
                        exit()
                else:
                    exit()
            else:
                exit()
    else:
        print('Not support')
