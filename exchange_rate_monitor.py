import os
import json
import requests
from datetime import datetime
import schedule
import time
import matplotlib.pyplot as plt

def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    rate = data['rates'][target_currency]
    return rate

def save_exchange_rate():
    base_currency = "USD"
    target_currency = "JPY"
    rate = get_exchange_rate(base_currency, target_currency)

    # 构建数据结构并保存为 JSON 文件
    data = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'rate': rate
    }
    with open('exchange_rates.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')

def plot_exchange_rates():
    # 如果文件不存在，先生成一个空文件
    if not os.path.exists('exchange_rates.json'):
        with open('exchange_rates.json', 'w') as f:
            pass

    with open('exchange_rates.json', 'r') as f:
    data = [json.loads(line) for line in f]

    dates = [datetime.strptime(d['date'], '%Y-%m-%d %H:%M:%S') for d in data]
    rates = [float(d['rate']) for d in data]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, rates)
    plt.title("USD to JPY Exchange Rate Over Time")
    plt.xlabel("Date")
    plt.ylabel("Exchange Rate")
    plt.grid(True)
    plt.savefig('exchange_rates.png')
    plt.close()
    
save_exchange_rate()
plot_exchange_rates()
