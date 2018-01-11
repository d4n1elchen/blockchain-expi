import smtplib
import json, requests
import csv
from email.mime.text import MIMEText
from time import sleep
from datetime import datetime as dt

def sendMail(sender, passwd, receivers, subject, content):
    msg = MIMEText(content)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ','.join(receivers)

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(sender, passwd)
    s.sendmail(sender, receivers, msg.as_string())
    s.quit()

    print("Send mail to "+msg['To'])

def getTick():
    url = 'https://www.bitoex.com/sync/dashboard_fixed/0'
    resp = requests.get(url=url)
    data = json.loads(resp.text)

    return data[0:2]

def write_csv(filename, buy, sell):
    with open(filename, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        ts = dt.strftime(dt.now(), '%Y-%m-%d %H:%M:%S')
        writer.writerow([ts, buy, sell])

def init_csv():
    filename = dt.strftime(dt.now(), '%Y%m%d%H%M') + '_history.csv'
    with open(filename, 'w') as csvfile:
        csvfile.write('time,buy,sell\n')
    return filename

sender = 'ccns.bitcoin@gmail.com'
passwd = 'CCNSccns'
receivers = ['team6612@gmail.com']

check = True

fn = init_csv()

while True:
    price = getTick()
    buy = price[0]
    sell = price[1]

    print(dt.strftime(dt.now(), '%Y-%m-%d %H:%M:%S'))
    print("Buy: "+buy)
    print("Sell: "+sell)
    # if int(buy.replace(',', '')) < 72000 and check:
    #     print("!!!!!")
    #     sendMail(sender, passwd, receivers, "Bitoex Price Report", str(getTick()))
    #     check = False
    # else:
    #     check = True
    write_csv(fn, int(buy.replace(",","")), int(sell.replace(",","")));

    print("")
    sleep(2)
