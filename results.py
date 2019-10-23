import pandas
import numpy
import matplotlib.pyplot as plot
from matplotlib.patches import Polygon
from filtering import filter_end_delays, filter_network_data
from variables import root_url, number_trials
from variables import box_colors

# feature to be plotted in the dataset
feature = 'delay'

# Separate trials dataset array
sep_datasets_endtoend = []
sep_datasets_network = []

sepjs_datasets_endtoend = []
sepjs_datasets_network = []

# Simultaneous trials dataset array
sim_datasets_endtoend = []
sim_datasets_network = []

# Array to feed the Ylabels
trials_numbers = []


# Helper method to import csv files
def run_import(method, trial_num, myfile):
    df = pandas.read_csv(root_url + method + '/' + str(trial_num) + '/' + myfile + '.csv')
    # print myfile + ' DataFrame\n', df
    return df


# df = pandas.DataFrame()

def fill_array(method, array, feature, scope):
    for x in range(number_trials):
        # Import and load the datasets into dataframes, and append them into the dataset array
        ## data measured in the endpoints of the communications
        if scope == 'end':
            array.append(filter_end_delays(run_import(method, x + 1, 'boxidaslwm2morion'))[feature])
            array.append(filter_end_delays(run_import(method, x + 1, 'boxidasulorion'))[feature])

        ## data measured in at in and outbounds of the devices
        if scope == 'network':
            origin_meas_data_lw = run_import(method, x + 1, 'boxidaslwm2mtrace')
            end_meas_data_lw = run_import(method, x + 1, 'boxidaslwm2m')
            origin_meas_data_ul = run_import(method, x + 1, 'boxidasultrace')
            end_meas_data_ul = run_import(method, x + 1, 'boxidasul')

            array.append(
                filter_network_data(origin_meas_data_lw, end_meas_data_lw,
                                    str(x + 1) + ' : ' + method + ' Box-idas lw traffic')[feature])

            array.append(
                filter_network_data(origin_meas_data_ul, end_meas_data_ul,
                                    str(x + 1) + ' : ' + method + ' Box-idas ul traffic')[feature])

        # fill the ylabel array
        trials_numbers.append(x + 1)


fill_array('separate', sep_datasets_endtoend, feature, 'end')
fill_array('separate', sep_datasets_network, feature, 'network')
fill_array('separatejs', sepjs_datasets_endtoend, feature, 'end')
fill_array('separatejs', sepjs_datasets_network, feature, 'network')
fill_array('simultaneous', sim_datasets_endtoend, feature, 'end')
fill_array('simultaneous', sim_datasets_network, feature, 'network')


# print 'sim_datasets_network size', len(sim_datasets_network)
# print 'sep_datasets_network size', len(sep_datasets_network)


# Main function to run the plots and tha charts
def run_delay_boxplots(showfliersvalue, draw_notches):
    # Subplots Sharing the same X Axis
    number_plots = 3
    #figures, (above, aboventw, below, belowntw, belowjs, belowjsntw) = plot.subplots(number_plots, sharex=True)
    figures, (above, below, belowjs) = plot.subplots(number_plots, sharex=True)

    # Adjust the pltos on the screen
    figures.subplots_adjust(left=0.085, right=0.95, top=0.95, bottom=0.1)

    # Legends

    # figures.text(0.515, 0.6, 'Sample Frequency (ms)', ha='center', va='center', rotation='horizontal')
    size = 'large'
    above.set_title('(a) Simultaneous Trials', size=size, ha='center')
    #aboventw.set_title('(b) Simultaneous Network', size=size)
    below.set_title('(b) Separate Trials', size=size)
    #belowntw.set_title('(d) Separate Network', size=size)
    belowjs.set_title('(c) Separate with epoch from jsLwClient', size=size)
   # belowjsntw.set_title('(f) SeparateJSEpoch Network', size=size)

    figures.text(0.05, 0.5, 'Packet Delay (ms)', ha='center', va='center', rotation='vertical')
    figures.text(0.515, 0.03, 'Sample Frequency (ms)', ha='center', va='center', rotation='horizontal')

    figures.text(0.91, 0.03, 'LWM2M',
                 backgroundcolor=box_colors[0], color='black', weight='roman',
                 size='x-small')
    figures.text(0.94, 0.03, 'UL',
                 backgroundcolor=box_colors[1],
                 color='black', weight='roman', size='x-small')

    # Set up the boxplots
    pltbox(above, sim_datasets_endtoend, showfliersvalue, draw_notches, 'end')
    pltbox(above, sim_datasets_network, showfliersvalue, draw_notches, 'network')
    #pltbox(aboventw, sim_datasets_network, showfliersvalue, draw_notches, 'network')
    pltbox(below, sep_datasets_endtoend, showfliersvalue, draw_notches, 'end')
    pltbox(below, sep_datasets_network, showfliersvalue, draw_notches, 'network')
    #pltbox(belowntw, sep_datasets_network, showfliersvalue, draw_notches, 'network')
    pltbox(belowjs, sepjs_datasets_endtoend, showfliersvalue, draw_notches, 'end')
    pltbox(belowjs, sepjs_datasets_network, showfliersvalue, draw_notches, 'network')
   # pltbox(belowjsntw, sepjs_datasets_network, showfliersvalue, draw_notches, 'network')


def pltbox(position, datasets, showfliersvalue, draw_notches, scope):
    boxplot = position.boxplot(datasets, notch=draw_notches, showfliers=showfliersvalue, sym='o', vert=1, whis=1.5)

    # Customize the characteristics of the boxplot
    plot.setp(boxplot['boxes'], color=box_colors[2])
    plot.setp(boxplot['whiskers'], color=box_colors[2])
    plot.setp(boxplot['medians'], color=box_colors[2])
    plot.setp(boxplot['fliers'], color=box_colors[2], marker='.')

    # Add a horizontal grid to the plot, but make it very light in color
    position.yaxis.grid(True, linestyle='-', which='major', color=box_colors[3], alpha=0.5)

    # Hide these grid behind plot objects
    position.set_axisbelow(True)

    # Now fill the boxes with desired colors
    num_boxes = len(datasets)
    medians = numpy.empty(num_boxes)  # Return a new array of given shape without initializing entries.
    means = numpy.empty(num_boxes)
    for i in range(num_boxes):
        box = boxplot['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        box_coords = numpy.column_stack([boxX, boxY])

        # Alternate the colors
        position.add_patch(Polygon(box_coords, facecolor=box_colors[i % 2]))

        # Now draw the median lines back over what we just filled in
        med = boxplot['medians'][i]
        # med = boxplot['averages'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            position.plot(medianX, medianY, 'k')
        medians[i] = medianY[0]
        means[i] = numpy.average(datasets[i])

        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box, for the case I want to see the outliers
        position.plot(numpy.average(med.get_xdata()), means[i],
                      color=box_colors[2], marker='x', markeredgewidth=2, markersize=5, markeredgecolor='k')

    # Set the axes labels
    position.set_xticklabels(numpy.repeat(trials_numbers, 2), rotation=45, fontsize=8)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in means across the samples. Add upper
    # X-axis tick labels with the sample means to aid in comparison
    # (just use two decimal places of precision)
    # Only for the plot with outliers, because we will plot two charts in one space
    # if showfliersvalue == 0:
    #     pos = numpy.arange(num_boxes) + 1
    #     # upper_labels = [str(numpy.round(s, 2)) for s in medians]
    #     upper_labels = [str(numpy.round(s, 2)) for s in medians]
    #     for tick, label in zip(range(num_boxes), position.get_xticklabels()):
    #         k = tick % 2
    #         position.text(pos[tick], .95, upper_labels[tick],
    #                       transform=position.get_xaxis_transform(),
    #                       horizontalalignment='center', size='large',
    #                       weight='bold', color=box_colors[k])
    #
    #     # # Finally, add a basic legend for medians
    #     # figures.text(0.80, 0.05, '00.00', color='black', weight='roman', size='medium')
    #     # figures.text(0.85, 0.05, 'Medians Values', color='black', weight='roman',
    #     #              size='x-small')

    # if showfliersvalue == 1:
    #     pos = numpy.arange(num_boxes) + 1
    #     # upper_labels = [str(numpy.round(s, 2)) for s in medians]
    #     upper_labels = [str(numpy.round(s, 2)) for s in means]
    #     for tick, label in zip(range(num_boxes), position.get_xticklabels()):
    #         k = tick % 2
    #         position.text(pos[tick], .95, upper_labels[tick],
    #                       transform=position.get_xaxis_transform(),
    #                       horizontalalignment='center', size='large',
    #                       weight='bold', color='black')

    #     # Finally, add a basic legend for means
    #     figures.text(0.80, 0.05, '00.00', color='black', weight='roman', size='medium')
    #     figures.text(0.85, 0.05, 'Mean Values', color='black', weight='roman',
    #                  size='x-small')
    #     figures.text(0.80, 0.026, 'x', color='black', weight='roman', size='large')
    #     figures.text(0.815, 0.026, 'Mean Positions', color='black', weight='roman',
    #                  size='x-small')
    #


def runbars(feature, showfliersvalue, notchvalue, datasets):
    # datasets = [pandas.DataFrame(), pandas.DataFrame(), pandas.DataFrame(), pandas.DataFrame()]

    # datasets = [df31[feature], df34[feature], df13[feature], df14[feature]]  # , df5[feature], df6[feature],
    # df7[feature], df8[feature], df9[feature], df10[feature], df11[feature], df12[feature]]

    # Return evenly spaced values within a given interval.
    trials = numpy.arange(1, 7)
    # for i in range(trials*2):
    #     datasets = numpy.empty('df'+i+'[feature]')
    xdata = []
    x = numpy.arange(len(datasets))
    for i in range(len(datasets)):
        xdata.append(numpy.round(numpy.average(datasets[i]), 2))
    print xdata

    plot.bar(x, height=xdata, color=[box_colors[0], box_colors[1], box_colors[0], box_colors[1]])
    plot.xticks(x, (numpy.repeat(trials, 2)))
    plot.xticks(rotation=70)
    plot.title('Mean ' + feature.title() + ' Distribution')
    plot.xlabel('Trials')
    plot.ylabel('Bytes')

    plot.text(3, 30, 'lwm2m / coap / udp',
              backgroundcolor=box_colors[0], color='white', weight='roman',
              size='x-small')
    plot.text(3, 0, 'ul / http / tcp',
              backgroundcolor=box_colors[1],
              color='white', weight='roman', size='x-small')

    # means0 = numpy.round(numpy.average(datasets[0]), 2)
    # means1 = numpy.round(numpy.average(datasets[1]), 2)
    # plot.ylabel('Bytes')
    # axs[0].hist(means0, bins=n_bins)
    # axs[1].hist(means1, bins=n_bins)
