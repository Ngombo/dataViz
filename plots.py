import pandas
import numpy
import matplotlib.pyplot as plot
import seaborn as sns
from matplotlib.patches import Polygon

from floader import load

# Load the datasets
df1 = pandas.DataFrame(load('mobileidaslwm2m', '1', 'lwm2m'))
df2 = pandas.DataFrame(load('mobileidaslwm2m', '1', 'lwm2m'))
# df2 = pandas.DataFrame(load('mobileorion', '1', ' '))
df3 = pandas.DataFrame(load('mobileidaslwm2m', '3', 'lwm2m'))
df4 = pandas.DataFrame(load('mobileidaslwm2m', '3', 'lwm2m'))
# df4 = pandas.DataFrame(load('mobileorion', '2', ' '))
df5 = pandas.DataFrame(load('mobileidaslwm2m', '2', 'lwm2m'))
df6 = pandas.DataFrame(load('mobileidaslwm2m', '2', 'lwm2m'))


# df6 = pandas.DataFrame(load('mobileorion', '3', ' '))

def fillcolor(dataset, plot, color1, color2):
    box_colors = [color1, color2]
    num_boxes = len(dataset)
    for i in range(num_boxes):
        box = plot['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        box_coords = numpy.column_stack([boxX, boxY])
        # Alternate the colrs
        plot.add_patch(Polygon(box_coords, facecolor=box_colors[i % 2]))


# print dataFrame['cupped_delay1']

def runplots(feature, units):
    dataset = [df1[feature], df2[feature], df3[feature], df4[feature], df5[feature], df6[feature]]

    # Custumises the displayed tags
    box_colors = ['lightgrey', 'firebrick', 'black']
    medianprops = dict(linestyle='-', linewidth=2.5, color=box_colors[1])
    meanpointprops = dict(marker='x', markeredgecolor=box_colors[1])

    # Subplots Sharing the same X Axis
    figures, (above, below) = plot.subplots(2, sharex=True)
    above.boxplot(dataset, notch=1, sym='o', vert=1, whis=1.5, meanprops=meanpointprops, meanline=False, showmeans=True)

    # Plot below customised format and do not showing outlier points
    below.boxplot(dataset, notch='true', showfliers=False, patch_artist=True,
                  boxprops={'facecolor': box_colors[0],
                            'edgecolor': box_colors[2]},
                  medianprops=medianprops, meanprops=meanpointprops, meanline=False, showmeans=False,
                  labels=['Trial 1', '', 'Trial 2', '', 'Trial 3', ''])

    # To overlaying the numeric value
    # toDo

    # Add a basic legend
    above.set_title(feature.title() + ' Full Distributions')
    below.set_title('Without Outliers')

    # for f(x) axis => Units
    figures.text(0.03, 0.5, units, ha='center', va='center', rotation='vertical')
    # for tags according to the color of the figures
    figures.text(0.91, 0.05, 'Lwm2m/udp', backgroundcolor=box_colors[0], color=box_colors[2], weight='roman',
                 size='x-small')

    # Add a horizontal grid to the plot, but make it very light in color
    above.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    below.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

    # Now fill the boxes with desired colors
    # fillcolor(dataset, above, box_colors[0], box_colors[1])
    # fillcolor(dataset, below, box_colors[0], box_colors[1])


# plot the length chart
runplots('length', 'Bytes')
# plot.savefig('length.png', dpi=300)

# plot the delay
plot.figure(1)
runplots('delay', 'Milliseconds')

plot.show()  # to keep the figures alive

# plot.savefig('delays.png', dpi=300)
