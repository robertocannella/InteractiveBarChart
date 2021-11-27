import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
from matplotlib.backend_bases import MouseButton
import math

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650),
                   np.random.normal(43000,100000,3650),
                   np.random.normal(43500,140000,3650),
                   np.random.normal(48000,70000,3650)],
                  index=[1992,1993,1994,1995]).T


fig = plt.figure(figsize=(5,5))
y_value = df.mean().values.max()



y_error = df.std().values/ (math.sqrt(df.count().values[0]))
print (y_error)
y_error = stats.sem(df)*1.96
print (y_error)

y_value = 30000

cmap = mpl.cm.RdBu_r


x_coordinates = [df.columns.min(),df.columns.max()]


cmap = mpl.cm.RdBu_r
for n, item in enumerate(df.columns):
    norm = mpl.colors.Normalize(df[item].mean() - y_error[n], df[item].mean() + y_error[n])
    colors = cmap(norm(abs(y_value)))

    _ = plt.bar(item, df[item].mean(),
                color=colors, width=1.0,
                edgecolor='grey', label='',
                yerr=stats.sem(df[item]) * 1.96, capsize=10)
_ = plt.xticks(df.columns)

fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap))

print(df.mean().values)
print (df.mean().values/42000)



def on_move(event):

    x, y = event.x, event.y
    if event.inaxes:
        _ = event.inaxes  # the axes instance
        y_value = event.ydata
        plt.clf()

        for n, item in enumerate(df.columns):
            norm = mpl.colors.Normalize(df[item].mean() - y_error[n], df[item].mean() + y_error[n])
            colors = cmap(norm(abs(y_value)))

            _ = plt.bar(item, df[item].mean(),
                         color=colors, width=1.0,
                         edgecolor='grey', label='',
                         yerr=stats.sem(df[item])*1.96, capsize=10)
        _ = plt.xticks(df.columns)

        fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap))

        #y_coordinates = [y_value, y_value]
        plt.axhline(y=y_value)
        #plt.plot(x_coordinates, y_coordinates)
        plt.draw()

mouse_off = False
def on_click(event):
    global mouse_off
    mouse_off = not mouse_off


    if event.button is MouseButton.LEFT:
        print('disconnecting callback')
        print(mouse_off)
        plt.disconnect(binding_id)


binding_id = plt.connect('motion_notify_event', on_move)
plt.connect('button_press_event', on_click)


plt.show()