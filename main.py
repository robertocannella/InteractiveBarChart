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

cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),aspect=10)
cbar.set_ticks([])
print(df.mean().values)
print (df.mean().values/42000)

line1 = plt.axhline(y=y_value, picker=5)
mouse_off = False

def on_move(event):
    global line1
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

        mean_normalize = mpl.colors.Normalize(df.mean().values.min(),df.mean().values.max())
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=mean_normalize, cmap=cmap),aspect=10)
        cbar.set_ticks([df.mean().values.min(),df.mean().values.mean(),df.mean().values.max()])
        cbar.ax.set_yticklabels(['Below', 'Within', 'Above'])  # horizontal colorbar
        #y_coordinates = [y_value, y_value]
        line1 = plt.axhline(y=y_value, picker=5)
        #plt.plot(x_coordinates, y_coordinates)
        plt.draw()

binding_id = ''

def on_click(event):
    print(event.inaxes)
    if event.button is MouseButton.LEFT:
        print('on_click')
        # print('disconnecting callback')
        # print(mouse_off)
        # plt.disconnect(binding_id)


def on_pick(event):
    global mouse_off
    global line1
    global binding_id
    print(event.artist)

    print('removing')
    thisline = event.artist
    thisline.remove()
    plt.draw()

    binding_id = plt.connect('motion_notify_event', on_move)
    plt.connect('button_press_event', on_click)

plt.connect('pick_event', on_pick)
# coords = []
# def on_click(event):
#     global ix, iy
#     ix, iy = event.xdata, event.ydata
#     print ('x = %d, y = %d'%(
#         ix, iy))
#
#     global coords
#     coords.append((ix, iy))
#
#     if len(coords) == 2:
#         fig.canvas.mpl_disconnect(cid)
#
#     return coords
# cid = fig.canvas.mpl_connect('button_press_event', on_click)

# def onpick(event):
#     origin = df.iloc[event.ind[0]]['origin']
#     plt.gca().set_title('Selected item came from {}'.format(origin))

binding_id = plt.connect('motion_notify_event', on_move)
plt.connect('button_press_event', on_click)

plt.show()