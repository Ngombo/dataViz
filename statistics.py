import numpy
import pandas
import re
import matplotlib.pyplot as plot;
from variables import box_colors2, box_colors, number_trials, root_url

plot.rcdefaults()

# Stats
dfstats_occupancy = []
dfstats_occup_lw = []
dfstats_occup_ul = []
dfstats_delay_lw = []
dfstats_delay_end_lw = []
dfstats_delay_end_ul = []
dfstats_delay_net_lw = []
dfstats_delay_net_ul = []
columns = ['client', 'trial', 'scope', 'protocol', 'feature', 'mean', 'median', 'mode', 'total bw']


def stats(df, label, label2):
    # Declaration of variables
    trial = re.split(' ', label)[0]
    client = re.split('/', re.split(' ', label)[2])[1]
    scope = re.split(' ', label)[3]
    protocol = re.split(' ', label)[4]
    feature = re.split(' ', label)[6]
    total = 'n/a'

    # sentframes = 0
    # receivedframes = 0
    # frameloss = 0
    #
    # if label2 == 'lw':
    #     sentframes = 26
    #     receivedframes = len(df)
    #     frameloss = numpy.round((1 - (receivedframes / float(sentframes))) * 100, 2)
    # if label2 == 'ul':
    #     sentframes = 25
    #     receivedframes = len(df)
    #     frameloss = numpy.round((1 - (receivedframes / float(sentframes))) * 100, 2)
    mean = numpy.round(df.mean(), 2)
    median = numpy.round(df.median(), 2)
    mode = numpy.round(df.mode()[0], 2)
    if feature == 'occupancy':
        total = df.sum()

    # initialise data of lists
    # data = {'client': [client], 'trial': [trial], 'scope': [scope], 'protocol': [protocol], 'feature': [feature],
    #         'mean': [mean], 'median': [median], 'mode': [mode], 'total': [total]}

    # Creates pandas DataFrame.
    # dfstats = pandas.DataFrame(data)
    # print '\nTrial # ' + label
    # if label2 == 'lw' or label2 == 'ul':
    #     print 'Sent Frames: ' + str(sentframes)
    #     print 'Received Frames: ' + str(receivedframes)
    #     print 'Frame Loss: ' + str(frameloss)
    # print 'mean: ' + str(mean)
    # print 'median: ' + str(median)
    # print 'mode: ' + str(mode)
    # print 'total: ' + str(total) + '\n'
    # print dfstats_mobile_lw
    # return dfstat

    # Delay dataframe
    if scope == 'end' and feature == 'delay' and protocol == 'lw':
        dfstats_delay_end_lw.append([client, trial, scope, protocol, feature, mean, median, mode, total])
        dfdelay = pandas.DataFrame(dfstats_delay_end_lw, columns=columns)
        # print dfdelay[['trial', 'scope', 'protocol', 'feature', 'mean', 'median', 'mode']]
        # Export [['trial', 'total bw']] to .csv
        dfdelay[['trial', 'mean', 'median', 'mode']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)
    if scope == 'end' and feature == 'delay' and protocol == 'ul':
        dfstats_delay_end_ul.append([client, trial, scope, protocol, feature, mean, median, mode, total])
        dfdelay = pandas.DataFrame(dfstats_delay_end_ul, columns=columns)
        # print dfdelay[['trial', 'scope', 'protocol', 'feature', 'mean', 'median', 'mode']]
        # Export [['trial', 'total bw']] to .csv
        dfdelay[['trial', 'mean', 'median', 'mode']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)
    if scope == 'network' and feature == 'delay' and protocol == 'lw':
        dfstats_delay_net_lw.append([client, trial, scope, protocol, feature, mean, median, mode, total])
        dfdelay = pandas.DataFrame(dfstats_delay_net_lw, columns=columns)
        # print dfdelay[['trial', 'scope', 'protocol', 'feature', 'mean', 'median', 'mode']]
        # Export [['trial', 'total bw']] to .csv
        dfdelay[['trial', 'mean', 'median', 'mode']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)
    if scope == 'network' and feature == 'delay' and protocol == 'ul':
        dfstats_delay_net_ul.append([client, trial, scope, protocol, feature, mean, median, mode, total])
        dfdelay = pandas.DataFrame(dfstats_delay_net_ul, columns=columns)
        # print dfdelay[['trial', 'scope', 'protocol', 'feature', 'mean', 'median', 'mode']]
        # Export [['trial', 'total bw']] to .csv
        dfdelay[['trial', 'mean', 'median', 'mode']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)

    # BW Occupancy LW dataframe
    if scope == 'network' and feature == 'occupancy' and protocol == 'lw' and total != 'n/a':
        dfstats_occup_lw.append([client, trial, scope, protocol, feature, mean, median, mode, total])
        dflw = pandas.DataFrame(dfstats_occup_lw, columns=columns)
        # print dflw[['trial', 'total bw']]
        # Export [['trial', 'total bw']] to .csv
        dflw[['trial', 'total bw']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)
    # BW Occupancy UK dataframe
    if scope == 'network' and feature == 'occupancy' and protocol == 'ul' and total != 'n/a':
        dfstats_occup_ul.append([client, trial, scope, protocol, feature, mean, median, mode, total])
        dful = pandas.DataFrame(dfstats_occup_ul, columns=columns)
        # print dful[['trial', 'total bw']]
        dful[['trial', 'total bw']].to_csv(
            root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
            index=False)

    if scope == 'network' and feature == 'occupancy' and total != 'n/a':
        dfstats_occupancy.append([client, trial, scope, protocol, feature, mean, median, mode, total])
        df1 = pandas.DataFrame(dfstats_occupancy, columns=columns)
        # barplot(df1, client)
        # print df1[['trial', 'total bw']]

    # return df1


def exportcsv(df, label, mean, median, mode):
    trial = re.split(' ', label)[0]
    client = re.split('/', re.split(' ', label)[2])[1]
    scope = re.split(' ', label)[3]
    protocol = re.split(' ', label)[4]
    feature = re.split(' ', label)[6]
    total = 'n/a'

    df.append([client, trial, scope, protocol, feature, mean, median, mode, total])
    df1 = pandas.DataFrame(df, columns=columns)
    # print dfdelay[['trial', 'scope', 'protocol', 'feature', 'mean', 'median', 'mode']]
    # Export [['trial', 'total bw']] to .csv
    df1[['trial', 'mean', 'median', 'mode']].to_csv(
        root_url + re.split(' ', label)[2] + "/" + scope + feature + "_" + protocol + ".csv",
        index=False)


def barplot(df, client):
    # Adapt the color box to the client
    if client == 'box':
        colors = box_colors
    if client == 'mobile':
        colors = box_colors2

    # create plot
    objects = df['trial']
    y_pos = numpy.arange(len(objects))
    observed_feature = df['total bw'].astype(float)
    plot.bar(y_pos, observed_feature, align='center', alpha=0.5, color=[colors[0], colors[1]])
    plot.xticks(y_pos, objects)
    plot.xlabel('Sample Frequency (ms)')
    plot.ylabel('Bytes')
    plot.title('Total Bandwidth Occupancy')
    plot.xticks(rotation=70)
