import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
from matplotlib.backend_bases import MouseButton

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650),
                   np.random.normal(43000,100000,3650),
                   np.random.normal(43500,140000,3650),
                   np.random.normal(48000,70000,3650)],
                  index=[1992,1993,1994,1995]).T


fig = plt.figure(figsize=(5,5))
y_value = df.mean().values.max()
y_error = stats.sem(df)

x_coordinates = [df.columns.min(),df.columns.max()]
cmap = mpl.cm.RdBu_r
norm = mpl.colors.Normalize(df.mean().values.min() - y_error.min(), df.mean().values.max() + y_error.max())
#norm = mpl.colors.Normalize(y_error.min(),y_value)
#norm = mpl.colors.Normalize(df.mean().values.min(),y_value)
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap))
colors = cmap(norm(df.mean().values))
ax = plt.bar(df.columns, df.mean(),
              color = colors, width=1.0,
              edgecolor = 'grey', label='',
              yerr=stats.sem(df), capsize=10)
ax = plt.xticks(df.columns)

print(df.mean().values)
print (df.mean().values/42000)



def on_move(event):

    x, y = event.x, event.y
    if event.inaxes:
        _ = event.inaxes  # the axes instance
        y_value = event.ydata
        plt.clf()

        cmap = mpl.cm.RdBu_r

        for n, item in enumerate(df.columns):
            norm = mpl.colors.Normalize(df[item].mean() - y_error[n], df[item].mean() + y_error[n])
            colors = cmap(norm(abs(y_value)))

            ax = plt.bar(item, df[item].mean(),
                         color=colors, width=1.0,
                         edgecolor='grey', label='',
                         yerr=stats.sem(df[item]), capsize=10)
            print(item)
        ax = plt.xticks(df.columns)


        #norm = mpl.colors.Normalize(df[1992].mean() - y_error.min(), y_value)
        bot_y_error = df.mean().values - y_error
        top_y_error = df.mean().values + y_error
        conf = df.mean().values * 0.196
        #norm = mpl.colors.Normalize(bot_y_error,top_y_error)
        print('conf: {}'.format(conf))
        print('y/top: {}'.format(y_value/top_y_error))
        print('y/mean: {}'.format(y_value/df.mean().values))
        print('y/bot: {}'.format(y_value/bot_y_error))


        fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap))

        print(colors)



        y_coordinates = [y_value, y_value]

        plt.plot(x_coordinates, y_coordinates)
        plt.draw()  # redraw




def on_click(event):
    if event.button is MouseButton.LEFT:
        print('disconnecting callback')
        plt.disconnect(binding_id)



binding_id = plt.connect('motion_notify_event', on_move)
plt.connect('button_press_event', on_click)


plt.show()