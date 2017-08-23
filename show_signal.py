import random

import matplotlib.finance as mpf
import matplotlib.pyplot as plt
import pandas
from matplotlib.dates import date2num

# シグナルが正しく生成されているかをチャートで確認する。
df = pandas.read_csv('EURUSD_M1_201706_with_signal.csv')  # type DataFrame
df.index = range(len(df))
# signalが発生しているインデックスをランダムに取得する
signalIndex = random.sample(df[df['signal'] != 0].index.tolist(), 1)
print(signalIndex)
# シグナル後4時間を見る
df = df[signalIndex[0]: signalIndex[0] + 240]
df.index = df['datetime'].apply(lambda x: pandas.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
df['d'] = df.index.map(date2num)

plt.grid()
plt.xticks(df['d'][::10], df.index[::10], rotation=45, size='small')
ax = plt.subplot()
# y軸のオフセット表示を無効にする。
ax.get_yaxis().get_major_formatter().set_useOffset(False)
data = df[['d', 'o', 'h', 'l', 'c']].values
# print(data)
# ローソク足は1日分の太さが1である。1日分の分足で割ってさらにその1/3の太さにする
wdth = 1.0 / (60 * 24) / 3
mpf.candlestick_ohlc(ax, data, width=wdth, colorup='g', colordown='r')
plt.show()
print('finished')
