import numpy
import pandas
import re
import matplotlib.pyplot as plt;

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

# Stats
dfstats_mobile_lw = []


# print dfstats_mobile_lw


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
    data = {'client': [client], 'trial': [trial], 'scope': [scope], 'protocol': [protocol], 'feature': [feature],
            'mean': [mean], 'median': [median], 'mode': [mode], 'total': [total]}

    # Creates pandas DataFrame.
    # dfstats = pandas.DataFrame(data)

    dfstats_mobile_lw.append([client, trial, scope, protocol, feature, mean, median, mode, total])

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

    columns = ['client', 'trial', 'scope', 'protocol', 'feature', 'mean', 'median', 'mode', 'total bw']
    # dfstats_mobile_lw = pandas.DataFrame(columns=columns)
    df1 = pandas.DataFrame(dfstats_mobile_lw, columns=columns)

    if scope == 'network' and protocol == 'ul' and feature == 'occupancy':
        objects = df1['trial']
        y_pos = np.arange(len(objects))
        performance = df1['mean']

        plt.bar(y_pos, performance, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('mean ul bw occupancy ')
        plt.title('Trials')
    # print df1
    # return df1
