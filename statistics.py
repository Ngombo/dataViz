import numpy
import pandas
import re
import matplotlib.pyplot as plot;

from variables import box_colors2, box_colors, number_trials, root_url

plot.rcdefaults()

# Stats
dfstats_occupancy = []
dfstats_arrival = []
dfstats_occup_lw = []
dfstats_occup_ul = []
dfstats_delay_lw = []
dfstats_delay_end_lw = []
dfstats_delay_end_ul = []
dfstats_delay_net_lw = []
dfstats_delay_net_ul = []
sent_values = []
columns = ['client', 'trial', 'scope', 'protocol', 'feature', 'arrival rate', 'mean', 'median', 'mode', 'total bw']


def stats(df, label):
    # Declaration of variables
    trial = re.split(' ', label)[0]
    client = re.split('/', re.split(' ', label)[2])[1]
    scope = re.split(' ', label)[3]
    protocol = re.split(' ', label)[4]
    feature = re.split(' ', label)[6]
    total_bw = 'n/a'
    arrival_rate = 'n/a'

    receivedReadings = len(df)

    if protocol == 'lw' and client == 'box':
        sentReadings = 26
    else:
        sentReadings = 25

    if scope == 'end':
        if (numpy.round((receivedReadings / float(sentReadings)) * 100, 2)) > 100:
            arrival_rate = 100 # To be stabilized in the proper version of the data collection
        else:
            arrival_rate = numpy.round((receivedReadings / float(sentReadings)) * 100, 2)
        # loss = numpy.round((1 - (receivedReadings / float(sentReadings))) * 100, 2)

    mean = numpy.round(df.mean(), 2)
    median = numpy.round(df.median(), 2)
    mode = numpy.round(df.mode()[0], 2)
    if feature == 'occupancy':
        total_bw = df.sum()

    # Delay dataframe
    if scope == 'end' and feature == 'delay' and protocol == 'lw':
        dfstats_delay_end_lw.append(
            [client, trial, scope, protocol, feature, arrival_rate, mean, median, mode, total_bw])
        dfdelay = pandas.DataFrame(dfstats_delay_end_lw, columns=columns)
        # print dfdelay[['trial', 'scope', 'protocol', 'feature', 'mean', 'median', 'mode']]
        # Export  the following columns to .csv
        # print dfdelay
        dfdelay[['trial', 'arrival rate', 'mean', 'median', 'mode']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)
        # print dfdelay['arrival rate']

    if scope == 'end' and feature == 'delay' and protocol == 'ul':
        dfstats_delay_end_ul.append(
            [client, trial, scope, protocol, feature, arrival_rate, mean, median, mode, total_bw])
        dfdelay = pandas.DataFrame(dfstats_delay_end_ul, columns=columns)
        # print dfdelay[['trial', 'scope', 'protocol', 'feature', 'mean', 'median', 'mode']]
        # Export [['trial', 'total bw']] to .csv
        # print dfdelay
        dfdelay[['trial', 'arrival rate', 'mean', 'median', 'mode']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)

    if scope == 'end' and feature == 'delay':
        dfstats_arrival.append(
            [client, trial, scope, protocol, feature, arrival_rate, mean, median, mode, total_bw])
        dfdelay = pandas.DataFrame(dfstats_arrival, columns=columns)
        barplot(dfdelay, dfdelay, 'Percentage of Arrived Readings', 'arrival rate', "%", client)
       # barplot(dfdelay, dfdelay, 'Most Frequent Values of Delays', 'mode', "ms", client)

    if scope == 'network' and feature == 'delay' and protocol == 'lw':
        dfstats_delay_net_lw.append(
            [client, trial, scope, protocol, feature, arrival_rate, mean, median, mode, total_bw])
        dfdelay = pandas.DataFrame(dfstats_delay_net_lw, columns=columns)
        # print dfdelay[['trial', 'scope', 'protocol', 'feature', 'mean', 'median', 'mode']]
        # Export [['trial', 'total bw']] to .csv
        dfdelay[['trial', 'mean', 'median', 'mode']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)
    if scope == 'network' and feature == 'delay' and protocol == 'ul':
        dfstats_delay_net_ul.append(
            [client, trial, scope, protocol, feature, arrival_rate, mean, median, mode, total_bw])
        dfdelay = pandas.DataFrame(dfstats_delay_net_ul, columns=columns)
        # print dfdelay[['trial', 'scope', 'protocol', 'feature', 'mean', 'median', 'mode']]
        # Export [['trial', 'total bw']] to .csv
        dfdelay[['trial', 'mean', 'median', 'mode']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)

    # BW Occupancy LW dataframe
    if scope == 'network' and feature == 'occupancy' and protocol == 'lw' and total_bw != 'n/a':
        dfstats_occup_lw.append([client, trial, scope, protocol, feature, arrival_rate, mean, median, mode, total_bw])
        dflw = pandas.DataFrame(dfstats_occup_lw, columns=columns)
        # print dflw[['trial', 'total bw']]
        # Export [['trial', 'total bw']] to .csv
        dflw[['trial', 'total bw']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)
    # BW Occupancy UK dataframe
    if scope == 'network' and feature == 'occupancy' and protocol == 'ul' and total_bw != 'n/a':
        dfstats_occup_ul.append([client, trial, scope, protocol, feature, arrival_rate, mean, median, mode, total_bw])
        dful = pandas.DataFrame(dfstats_occup_ul, columns=columns)
        # print dful[['trial', 'total bw']]
        dful[['trial', 'total bw']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)

    if scope == 'network' and feature == 'occupancy' and total_bw != 'n/a':
        dfstats_occupancy.append([client, trial, scope, protocol, feature, arrival_rate, mean, median, mode, total_bw])
        df1 = pandas.DataFrame(dfstats_occupancy, columns=columns)
        dful = df1.loc[df1['protocol'] == 'ul', ['trial', 'protocol', 'total bw']]
        dlw = df1.loc[df1['protocol'] == 'lw', ['trial', 'protocol', 'total bw']]
        # print df2[['trial', 'protocol', 'total bw']]
        # print df1
        #barplot(df1, df1, 'Total Bandwidth Occupancy','total bw', 'KBytes',  client)

    # return df1

    # Creates pandas DataFrame.
    # dfstats = pandas.DataFrame(data)
    # print '\nTrial # ' + label
    # if label2 == 'lw' or label2 == 'ul':
    #     print 'Sent Frames: ' + str(sentframes)
    #     print 'Received Frames: ' + str(receivedframes)
    #     print 'Frame Loss: ' + str(frameloss)

    # exportcsv(dfstats_delay_end_lw, label, client, trial, scope, protocol, feature,arrival rate, mean, median, mode, total)
    # exportcsv(dfstats_delay_end_ul,label, client, trial, scope, protocol, feature, frameloss,mean, median, mode, total)
    # exportcsv(dfstats_delay_net_lw, label, client, trial, scope, protocol, feature, frameloss, mean, median, mode, total)
    # exportcsv(dfstats_delay_net_ul,label,  client, trial, scope, protocol, feature, mean,frameloss, median, mode, total)
    # exportcsv(dfstats_occup_lw, label,client, trial, scope, protocol, feature, mean,frameloss, median, mode, total)
    # exportcsv(dfstats_occup_ul, label,client, trial, scope, protocol, feature, mean,frameloss, median, mode, total)


def lineplot():
    df = pandas.read_csv(root_url + 'separate/mobile/enddelay_lw.csv')
    df1 = pandas.read_csv(root_url + 'separate/mobile/enddelay_ul.csv')
    x = df1['trial']
    y1 = df['arrival rate']
    y2 = df1['arrival rate']
    plot.plot(x, y1, "r--", label="LWM2M")
    plot.plot(x, y2, "b:o", label="UL")
    plot.legend()


def barplot(df1, df2, title, observed_values, ylabel, client):
    # Adapt the color box to the client
    if client == 'box':
        colors = box_colors
    if client == 'mobile':
        colors = box_colors2

    # create plot
    objects = df1['trial']
    y_pos = numpy.arange(len(objects))

    # observed_feature1 = df['total bw'].astype(float)
    # extract columns value based on another column pandas dataframe
    # df1 = df1.loc[df1['protocol'] == 'ul', ['trial', 'protocol', 'total bw']]
    # print df1
    # df2 = df1['total bw']
    # print df2
    dful = df1.loc[df1['protocol'] == 'ul', ['trial', 'protocol', 'total bw']]
    # print dful['total bw']
    x1 = df1[observed_values].astype(float)
    x2 = df2[observed_values].astype(float)
    plot.bar(y_pos, x1, align='center', alpha=0.5, color=[colors[0], colors[1]])
    # plot.plot(y_pos, x1, "r--", label="UL")
    # plot.plot(y_pos, x2, "b:o", label="LWM2M")
    # plot.legend()
    plot.xticks(y_pos, objects)
    plot.xlabel('Sample Frequency (s)')
    plot.ylabel(ylabel)
    plot.title(title)

    # set individual bar labels above list
    for i, v in enumerate(x1):
        plot.text(y_pos[i] - 0.25, v + 0.01, str(numpy.round(v, 2)))

    plot.xticks(rotation=70)


def exportcsv(df, label, client, trial, scope, protocol, feature, arrival_rate, mean, median, mode, total):
    df.append([client, trial, scope, protocol, feature, mean, median, arrival_rate, mode, total])

    if feature == 'delay':
        df1 = pandas.DataFrame(df, columns=columns)
        # print dfdelay[['trial', 'scope', 'protocol', 'feature', frameloss,'mean', 'median', 'mode']]
        # Export [['trial', 'total bw']] to .csv
        df1[['trial', 'mean', 'median', 'mode']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)

    if feature == 'occupancy' and total != 'n/a':
        df1 = pandas.DataFrame(df, columns=columns)
        # print df1[['trial', 'total bw']]
        # Export [['trial', 'total bw']] to .csv
        df1[['trial', 'total bw']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)
