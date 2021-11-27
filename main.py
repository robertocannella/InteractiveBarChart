import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
from matplotlib.backend_bases import MouseButton
import plotly.express as px

import math

# Generate random data
np.random.seed(12345)
df = pd.DataFrame([np.random.normal(32000,200000,3650),
                   np.random.normal(43000,100000,3650),
                   np.random.normal(43500,140000,3650),
                   np.random.normal(48000,70000,3650)],
                  index=[1992,1993,1994,1995]).T


# Set figure defaults here.

fig = plt.figure(figsize=(5, 5))

# Set parameter defaults here.
y_value = df.mean().values.mean()                    # initial y value
y_error = stats.sem(df)*1.96                         # Standard Error * Confidence Level
cmap = mpl.cm.RdBu_r                                 # Color scheme



# Plot bars.
for n, item in enumerate(df.columns):
    norm = mpl.colors.Normalize(df[item].mean() - y_error[n], df[item].mean() + y_error[n])
    colors = cmap(norm(abs(y_value)))

    _ = plt.bar(item, df[item].mean(),
                color=colors, width=1.0,
                edgecolor='grey', label='',
                yerr=stats.sem(df[item]) * 1.96, capsize=10)
_ = plt.xticks(df.columns)
_ = plt.title('Mean Probability Comparison')
line1 = plt.axhline(y=y_value, picker=5, color='k')

# Color bar configuration
below = df.mean().values.min()-y_error.max()
within = df.mean().values.mean()-y_error.min()
above = df.mean().values.max()+ y_error.min()
mean_normalize = mpl.colors.Normalize(below,above)
cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=mean_normalize, cmap=cmap), aspect=10)
cbar.set_ticks([below, within, above])
cbar.ax.set_yticklabels(['Below', 'Within', 'Above'])  # horizontal colorbar


def on_move(event):
    global line1
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
        _ = plt.title('Mean Probability Comparison')


        mean_normalize = mpl.colors.Normalize(below,above)
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=mean_normalize, cmap=cmap),aspect=10)
        cbar.set_ticks([below,within,above])
        cbar.ax.set_yticklabels(['Below', 'Within', 'Above'])  # horizontal colorbar
        #y_coordinates = [y_value, y_value]
        line1 = plt.axhline(y=y_value, picker=5, color='k')
        #plt.plot(x_coordinates, y_coordinates)
        plt.draw()


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
binding_id = plt.connect('motion_notify_event', on_move)
plt.connect('button_press_event', on_click)

plt.show()