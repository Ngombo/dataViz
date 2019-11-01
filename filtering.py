import re

import pandas
import numpy
from statistics import stats
from variables import precision_delay, precision_length


# Eliminate the unnecessary data
def filter_end_delays(df, stats_label):
    # df.rename(columns={'json.value.string': 'Read Epoch'}, inplace=True)
    # df.rename(columns={'frame.time_epoch': 'Arrive Epoch'}, inplace=True)
    df.rename(columns={'String value': 'Read Epoch'}, inplace=True)
    df.rename(columns={'Epoch Time': 'Arrive Epoch'}, inplace=True)
    # print 'Read Epoch' , df['Read Epoch']
    # Drop columns with NAN values in Request Method i.e, non POST requests
    df.dropna(subset=['Request Method'], inplace=True)

    # In the column 'Read Epoch', extract both the Reading number and the epoch value corresponding to it
    # First extract the x.x pattern in the string content of the cell
    ##df['Read Epoch'] = df['Read Epoch'].str.findall(r"\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d+")
    ##df['Read Epoch'] = re.split(',', df['Read Epoch'])[5]
    df['Read Epoch'] = df['Read Epoch'].str.findall(r"\d+\.\d+").str[0]

    # Extract both the Reading number
    df['Reading number'] = df['Read Epoch'].str.split('.').str[0]
    # Extract both the the epoch value i.e, the sensing value
    df['Read Epoch'] = df['Read Epoch'].str.split('.').str[1]

    # Drop columns with NAN values in Request Method
    # Due to the connect POST in the lwm2m that has no read value
    df.dropna(subset=['Read Epoch'], inplace=True)

    # print protocol + ' Reading number', df['Reading number']

    reading_number = []
    for x in range(0, len(df['Reading number'])):
        reading_number.append(df['Reading number'].iloc[x])

    # print 'len Reading number', len(df['Reading number'])
    # print 'reading_number', reading_number

    # Drop columns with NAN values in Read Epoch
    df.dropna(subset=['Read Epoch'], inplace=True)
    # Prevent pandas converting large numbers to exponential
    df['Arrive Epoch'] = df['Arrive Epoch'].apply(lambda x: '{:.9f}'.format(x))

    # remove the . from the values
    df['Arrive Epoch'] = df['Arrive Epoch'].str.replace(r'\D', '').astype(long)

    # insert new column delay that is the difference between the received and sent epoch times
    # eliminate the nanosecond scale because, all hosts rtc-OS do not provide epoch to this level
    df['delay'] = df['Arrive Epoch'].astype(float) / precision_delay - df['Read Epoch'].astype(float) / precision_delay

    # Compute Stats results
    stats(df['delay'], stats_label + ' delay')

    # include only the columns we want to plot
    df = df[df.columns[df.columns.isin(['delay'])]]
    # print df
    return df


# Eliminate the unnecessary data
def filter_network_data(dataorigin, dataend, stats_label):
    df = pandas.DataFrame()  # for delays / network and endToend
    df1 = pandas.DataFrame()  # for bw occupancy / network only

    # Insert new columns named 'delay' which values are the differences on epoch times
    # in milliseconds => nano/10^6 and rounded to two decimals
    delay_value = (helper(dataend, stats_label)['epoch'] - helper(dataorigin, stats_label)['epoch']) / precision_delay
    df['delay'] = numpy.round(delay_value, 2)
    # print 'df', df

    # Add new columns in df1 to enable a fusioned max columns between lenghts
    df1['length origin'] = helper2(dataorigin)['length']
    df1['length end'] = helper2(dataend)['length']
    # print 'df1', df1
    # Select the bigger number between the two values to feed the new column 'max length'
    df1['max length'] = df1[["length origin", "length end"]].max(axis=1)

    # include only the columns we want to plot for each DF
    # df = df[df.columns[df.columns.isin(['delay', 'max length'])]]
    df = df[df.columns[df.columns.isin(['delay'])]]
    df1 = df1[df1.columns[df1.columns.isin(['max length'])]]

    # Drop columns with NAN values for the case the number of received packets is not the same as the sent one
    df.dropna(subset=['delay'], inplace=True)
    df1.dropna(subset=['max length'], inplace=True)

    # print 'dataorigin\n', frame

    # Compute Stats results
    stats(df['delay'], stats_label + ' delay')
    stats(df1['max length'], stats_label + ' occupancy')

    # print 'Delta delays between for ' + label + '\n', df
    return df


# Eliminate the unnecessary data and format the values
def helper(dfin, label):
    df = pandas.DataFrame(dfin[['frame.time_epoch', 'http.request.method']])
    # Drop columns with NAN values in Request Method i.e, non POST requests
    if re.split(' ', label)[4] == 'ul':
        df.dropna(subset=['http.request.method'], inplace=True)

    # rename columns
    df.rename(columns={'frame.time_epoch': 'epoch'}, inplace=True)

    # Prevent pandas converting large numbers to exponential
    # power_scale = '9'  # nanoseconds
    # df['epoch'] = df['epoch'].apply(lambda x: '{:.'+power_scale+'f}'.format(x))
    # df['epoch'] = df['epoch'].apply(lambda x: '{:.9f}'.format(x))

    # remove the . from the values so that we have it epoch in nanoseconds
    df['epoch'] = df['epoch'].str.replace(r'\D', '').astype(long)

    # convert the values into numbers for computing purposes later on
    df['epoch'] = df['epoch'].astype(long)

    # print 'helped delay  DataFrame\n', df
    return df


def helper2(dfin):
    df = pandas.DataFrame(dfin[['frame.cap_len']])
    # rename columns
    df.rename(columns={'frame.cap_len': 'length'}, inplace=True)

    # convert the values into numbers for computing purposes later on
    df['length'] = df['length'].astype(long) / precision_length

    # print 'helped length DataFrame\n', df
    return df
