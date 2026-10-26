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
    plt.plot(dates, rates, label='Exchange Rate', color='#1f77b4')

    # ===== 新增：异常波动检测与标注逻辑 =====
    # 设定预警阈值，例如 1% (即 0.01)
    THRESHOLD = 0.01 
    
    # 确保至少有两天的数据才能计算波动
    if len(rates) > 1:
        for i in range(1, len(rates)):
            prev_rate = rates[i-1]
            curr_rate = rates[i]
            
            # 计算涨跌幅百分比
            change = (curr_rate - prev_rate) / prev_rate
            
            # 如果波动超过了阈值（暴涨或暴跌）
            if abs(change) >= THRESHOLD:
                # 打印到日志里（这样你在 GitHub Actions 运行日志里也能看到警告）
                print(f"🚨 警告：{dates[i].strftime('%Y-%m-%d')} 发生大幅波动！涨跌幅: {change*100:.2f}%")
                
                # 在图上把这个点画成红色（如果是跌就是红色，涨就是绿色）
                color = 'red' if change < 0 else 'green'
                plt.scatter(dates[i], curr_rate, color=color, zorder=5, s=50)
                
                # 在图上的数据点旁边加上文字注释
                plt.annotate(f"{change*100:+.2f}%", 
                             xy=(dates[i], curr_rate), 
                             xytext=(0, 15 if change > 0 else -25), # 根据涨跌调整文字位置
                             textcoords='offset points', 
                             ha='center', va='bottom',
                             color=color, fontweight='bold')
    # =======================================

    plt.title("USD to JPY Exchange Rate Over Time")
    plt.xlabel("Date")
    plt.ylabel("Exchange Rate")
    plt.grid(True)
    plt.savefig('exchange_rates.png')
    plt.close()

    
save_exchange_rate()
plot_exchange_rates()
