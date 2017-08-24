import numpy
from keras.callbacks import EarlyStopping, TensorBoard
from keras.layers import GRU, Dense, Activation
from keras.models import Sequential
from keras.optimizers import Adam
from matplotlib import pyplot
from sklearn.model_selection import train_test_split


def weight_variable(shape, name=None):
    return numpy.random.normal(scale=.01, size=shape)


maxlen = 1440  # ひとつの時系列データの長さ(24時間)
x = numpy.load('EURUSD_M1_201706_x.npy')
y = numpy.load('EURUSD_M1_201706_y.npy')

x = x.reshape((int(len(x) / maxlen), maxlen, 1))
y = y.reshape((len(x), 1))

X_train, X_test, Y_train, Y_test = train_test_split(x, y, train_size=0.8)
X_train, X_validation, Y_train, Y_validation = \
    train_test_split(X_train, Y_train, train_size=0.8)

n_in = len(x[0][0])  # 1440
n_hidden = 30
n_out = len(y[0])  # 1

epochs = 500
batch_size = 10

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


hist = model.fit(X_train, Y_train,
                 batch_size=batch_size,
                 epochs=epochs,
                 validation_data=(X_validation, Y_validation),
                 callbacks=[early_stopping, TensorBoard(log_dir="log", histogram_freq=1)])

'''
学習の進み具合を可視化
'''
acc = hist.history['val_acc']
loss = hist.history['val_loss']

pyplot.rc('font', family='serif')
fig = pyplot.figure()
pyplot.plot(range(len(loss)), loss,
            label='loss', color='black')
pyplot.xlabel('epochs')
pyplot.show()

'''
予測精度の評価
'''
loss_and_metrics = model.evaluate(X_test, Y_test)
print(loss_and_metrics)
