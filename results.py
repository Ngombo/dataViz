import pandas
import numpy
import matplotlib.pyplot as plot
from matplotlib.patches import Polygon
from filtering import filter_end_delays, filter_network_data
from variables import root_url, number_trials
from variables import box_colors, box_colors2

# Declare dataset arrays
datasets_sep_endtoend = []
datasets_sep_network = []
datasets_sep_processing = []


# Array to feed the Ylabels
trials_numbers = []


# Helper method to import csv files
def run_import(gathering, trial_num, myfile):
    df = pandas.read_csv(root_url + gathering + '/' + str(trial_num) + '/' + myfile + '.csv',
                         dtype={"frame.time_epoch": "string"})
    # print myfile + ' DataFrame\n', df
    return df


def fill_array(gathering, array, feature, scope):
    for x in range(0, number_trials):
        # Import and load the datasets into dataframes, and append them into the dataset array
        ## data measured in the endpoints of the communications

        stats_label = str(x + 1) + ' : ' + gathering + ' ' + scope
        if scope == 'end':
            array.append(
                filter_end_delays(run_import(gathering, x + 1, gathering.split("/")[1] + 'idaslwm2morion'),
                                  stats_label + ' lw traffic')[feature])
            array.append(
                filter_end_delays(run_import(gathering, x + 1, gathering.split("/")[1] + 'idasulorion'),
                                  stats_label + ' ul traffic')[
                    feature])

        ## data measured in at in and outbounds of the devices
        if scope == 'network':
            origin_meas_data_lw = run_import(gathering, x + 1, gathering.split("/")[1] + 'idaslwm2mtrace')
            end_meas_data_lw = run_import(gathering, x + 1, gathering.split("/")[1] + 'idaslwm2m')
            origin_meas_data_ul = run_import(gathering, x + 1, gathering.split("/")[1] + 'idasultrace')
            end_meas_data_ul = run_import(gathering, x + 1, gathering.split("/")[1] + 'idasul')

            array.append(
                filter_network_data(origin_meas_data_lw, end_meas_data_lw, stats_label + ' lw traffic')[feature])

            array.append(
                filter_network_data(origin_meas_data_ul, end_meas_data_ul, stats_label + ' ul traffic')[feature])

        # fill the ylabel array
        trials_numbers.append(x + 1)


# Main function to run the plots and tha charts
def main_run(client, feature, showfliersvalue, draw_notches):
    # Adapt the color box to the client
    if client == 'box':
        colors = box_colors
    if client == 'mobile':
        colors = box_colors2

    # Prepare the files
    fill_array('separate/' + client, datasets_sep_endtoend, feature, 'end')
    fill_array('separate/' + client, datasets_sep_network, feature, 'network')

    # Declare the subplots Sharing the same X Axis
    number_plots = 2
    figures, (above, below) = plot.subplots(number_plots, sharex=True)

    # Adjust the plots on the screen
    figures.subplots_adjust(left=0.085, right=0.95, top=0.95, bottom=0.1)

    # Legends

    # figures.text(0.515, 0.6, 'Sample Frequency (ms)', ha='center', va='center', rotation='horizontal')
    size = 'large'
    above.set_title('(a) End-to-End Traffic', size=size, ha='center')
    below.set_title('(b) Network Traffic', size=size)

    figures.text(0.05, 0.53, 'Packet Delay (ms)', ha='center', va='center', rotation='vertical')
    figures.text(0.515, 0.03, 'Sample Frequency (s)', ha='center', va='center', rotation='horizontal')

    figures.text(0.91, 0.03, 'LWM2M',
                 backgroundcolor=colors[0], color='white', weight='roman',
                 size='x-small')
    figures.text(0.94, 0.03, 'UL',
                 backgroundcolor=colors[1],
                 color='black', weight='roman', size='x-small')

    # Set up the boxplots
    pltbox(above, datasets_sep_endtoend, showfliersvalue, draw_notches, colors)
    pltbox(below, datasets_sep_network, showfliersvalue, draw_notches, colors)


def pltbox(position, datasets, showfliersvalue, draw_notches, colors):
    boxplot = position.boxplot(datasets, notch=draw_notches, showfliers=showfliersvalue, sym='o', vert=1, whis=1.5)

    # Customize the characteristics of the boxplot
    plot.setp(boxplot['boxes'], color=colors[2])
    plot.setp(boxplot['whiskers'], color=colors[2])
    plot.setp(boxplot['medians'], color=colors[2])
    plot.setp(boxplot['fliers'], color=colors[2], marker='.')

    # Add a horizontal grid to the plot, but make it very light in color
    position.yaxis.grid(True, linestyle='-', which='major', color=colors[3], alpha=0.5)

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
        position.add_patch(Polygon(box_coords, facecolor=colors[i % 2]))

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
                      color=colors[2], marker='x', markeredgewidth=2, markersize=5, markeredgecolor='k')

    # Set the axes labels
    position.set_xticklabels(numpy.repeat(trials_numbers, 2), rotation=45, fontsize=8)