import re

import pandas
import numpy
from statistics import stats
from variables import precision_delay, precision_length


# Eliminate the unnecessary data
def filter_process_delays(df, scope):
    # Drop columns with NAN values in Request Method i.e, non POST requests
    df.dropna(subset=['Request Method'], inplace=True)

    if scope == 'client':
        # # For the time being the .csv of the endToend are generated directly from .pcap
        # # Hence, the columns have to the same names as the Ntwr .csvs
        df.rename(columns={'String value': 'frame.time_epoch'}, inplace=True)
        # In the column 'Read Epoch', extract both the Reading number and the epoch value corresponding to it
        # First extract the x.x pattern in the string content of the cell
        df['frame.time_epoch'] = df['frame.time_epoch'].str.findall(r"\d+\.\d+").str[0]

        # Extract the epoch value i.e, the sensing value
        df['frame.time_epoch'] = df['frame.time_epoch'].str.split('.').str[1]

        # Format the number to adjust to df3 and df4
        # Insert a "." after the first 10 numeric characters from the left
        df['frame.time_epoch'] = df['frame.time_epoch'].str.replace(r'^((?:\D*\d){10})(?=.+)', r'\1.')

        # Drop columns with NAN values in Read Epoch
        df.dropna(subset=['frame.time_epoch'], inplace=True)
    if scope == 'server':
        # # For the time being the .csv of the endToend are generated directly from .pcap
        # # Hence, the columns have to the same names as the Ntwr .csvs
        df.rename(columns={'Epoch Time': 'frame.time_epoch'}, inplace=True)



    # # For the time being the .csv of the endToend are generated directly from .pcap
    # # Hence, the columns have to the same names as the Ntwr .csvs
    df.rename(columns={'Request Method': 'http.request.method'}, inplace=True)
    df.rename(columns={'Length': 'frame.cap_len'}, inplace=True)
    df.rename(columns={'Request Method': 'http.request.method'}, inplace=True)
    return df

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
    ##df['Arrive Epoch'] = df['Arrive Epoch'].apply(lambda x: '{:.9f}'.format(x))


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
    #print 'Delay Network  ' + stats_label, df[['delay']]
   # print 'Delay Network  ' + stats_label, df

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
    protocol =re.split(' ', label)[4]

    # Drop columns with NAN values in Request Method i.e, non POST requests
    if protocol == 'ul':
        df.dropna(subset=['http.request.method'], inplace=True)

    # rename columns
    df.rename(columns={'frame.time_epoch': 'epoch'}, inplace=True)

    # remove the . from the values so that we have it epoch in nanoseconds
    df['epoch'] = df['epoch'].str.replace(r'\D', '').astype(long)

    # convert the values into numbers for computing purposes later on
    df['epoch'] = df['epoch'].astype(long)
    #
    # if protocol == 'lw':
    #     print 'Timestamp Network  ' + label, df[['delay']]
    return df


def helper2(dfin):
    df = pandas.DataFrame(dfin[['frame.cap_len']])
    # rename columns
    df.rename(columns={'frame.cap_len': 'length'}, inplace=True)

    # convert the values into numbers for computing purposes later on
    df['length'] = df['length'].astype(long) / precision_length

    # print 'helped length DataFrame\n', df
    return df
