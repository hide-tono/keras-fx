import numpy
import pandas
import sklearn
from keras.callbacks import EarlyStopping
from keras.layers import GRU, Dense, Activation
from keras.models import Sequential
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split

df = pandas.read_csv('EURUSD_M1_201706_with_signal.csv')
df.drop('datetime', axis=1)
maxlen = 1440  # ひとつの時系列データの長さ(24時間)

x, y = []
df.drop('v', axis=1)
signal = x['signal']
x.drop('signal', axis=1)

for i in range(1440, len(df)):
    x.append(df.ix[i: i + maxlen])
    x.append(signal.ix[i: i + maxlen])


X_train, X_test, Y_train, Y_test = train_test_split(x, y, train_size=0.8)


def weight_variable(shape, name=None):
    return numpy.random.normal(scale=.01, size=shape)


n_in = len(x[0][0])  # 1
n_hidden = 30
n_out = len(y[0])  # 1

early_stopping = EarlyStopping(monitor='loss', patience=100, verbose=1)

model = Sequential()
model.add(GRU(n_hidden,
              kernel_initializer=weight_variable,
              input_shape=(maxlen, n_in)))
model.add(Dense(n_out, kernel_initializer=weight_variable))
model.add(Activation('linear'))

optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
model.compile(loss='mean_squared_error',
              optimizer=optimizer)

epochs = 500
batch_size = 10

model.fit(X_train, Y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(X_validation, Y_validation),
          callbacks=[early_stopping])