import pandas
import numpy

df = pandas.read_csv('EURUSD_M1_201706_with_signal.csv')
df.drop('datetime', axis=1)
maxlen = 1440  # ひとつの時系列データの長さ(24時間)

x = numpy.empty((0, 1440), float)
y = numpy.empty((0, 1), int)
df.drop('v', axis=1)
signal = df['signal']
df.drop('signal', axis=1)

# 1時間ごとにトレーニングデータを作る
for i in range(1440, len(df), 60):
    # とりあえず終値だけにしてみる
    append_x = numpy.array([df['c'].ix[i - maxlen: i - 1]])
    append_y = numpy.array([signal.ix[i]])
    x = numpy.append(x, append_x)
    y = numpy.append(y, append_y)

numpy.save('EURUSD_M1_201706_x.npy', x)
numpy.save('EURUSD_M1_201706_y.npy', y)
