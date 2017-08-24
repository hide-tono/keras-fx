import pandas

positive_pips = 30
negative_pips = 10
point = 0.0001

# ファイルはここからダウンロードしている
# http://www.histdata.com/download-free-forex-historical-data/?/metatrader/1-minute-bar-quotes/EURUSD

df = pandas.read_csv('DAT_MT_EURUSD_M1_201706.csv',
                     names=['date', 'time', 'o', 'h', 'l', 'c', 'v'],
                     parse_dates={'datetime': ['date', 'time']},
                     )  # type DataFrame
df.index = df['datetime']
# print(df[1707:1950])
df['signal'] = 0
print(len(df))

# シグナルを作成する。対象は4時間(240分)。
# 下にnegative pips動く前に上にpositive pips動いていたら買い
# 上下にnegative pipsも動かなかった場合は凪
# 上にnegative pips動く前に上にpositive pips動いていたら売り
for i in range(len(df) - 241):
    base = df.ix[i]
    target = df[i:i + 240]
    upper_negative = target.ix[target['h'] > df['h'][i] + negative_pips * point]
    upper_positive = target.ix[target['h'] > df['h'][i] + positive_pips * point]
    lower_negative = target.ix[target['l'] < df['l'][i] - negative_pips * point]
    lower_positive = target.ix[target['l'] < df['l'][i] - positive_pips * point]

    if len(upper_positive) > 0:
        if len(lower_negative) == 0:
            df['signal'][i] = 1
        elif upper_positive.ix[0]['datetime'] < lower_negative.ix[0]['datetime']:
            df['signal'][i] = 1
    if len(lower_positive) > 0:
        if len(upper_negative) == 0:
            df['signal'][i] = -1
        elif lower_positive.ix[0]['datetime'] < upper_negative.ix[0]['datetime']:
            df['signal'][i] = -1

df.dropna()
df.to_csv('EURUSD_M1_201706_with_signal.csv')
