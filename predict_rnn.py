import pandas

positive_pips = 30
negative_pips = 10
point = 0.0001

df = pandas.read_csv('DAT_MT_EURUSD_M1_201706.csv',
                     names=['date', 'time', 'o', 'h', 'l', 'c', 'v'],
                     parse_dates={'datetime': ['date', 'time']},
                     )  # type DataFrame
df.index = df['datetime']

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
