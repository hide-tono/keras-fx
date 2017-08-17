import pandas

positive_pips = 30
negative_pips = 10
point = 0.0001

df = pandas.read_csv('DAT_MT_EURUSD_M1_201706.csv',
                     names=['date', 'time', 'o', 'h', 'l', 'c', 'v'],
                     parse_dates={'datetime': ['date', 'time']},
                     )  # type DataFrame
df.index = df['datetime']
# print(df[1707:1950])
df['signal'] = 0
print(len(df))

# シグナルを作成する
# 下にnegative pips動く前に上にpositive pips動いていたら買い
# 上にnegative pips動く前に下にpositive pips動いていたら売り
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

print(df.ix[df['signal'] != 0])

# print(a['h'][0] + positive_pips * point)
# print(a.ix[a['h'] > (a['h'][0] + positive_pips * point)])

# print(df['h'].rolling(window=24 * 60).max())


# n_in = len(X[0][0])  # 2
# n_hidden = 100
# n_out = len(Y[0])  # 1
#
#
# def weight_variable(shape, name=None):
#     return np.random.normal(scale=.01, size=shape)
#
#
# early_stopping = EarlyStopping(monitor='loss', patience=100, verbose=1)
#
# model = Sequential()
# model.add(GRU(n_hidden,
#               kernel_initializer=weight_variable,
#               input_shape=(maxlen, n_in)))
# model.add(Dense(n_out, kernel_initializer=weight_variable))
# model.add(Activation('linear'))
#
# optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
# model.compile(loss='mean_squared_error',
#               optimizer=optimizer)
