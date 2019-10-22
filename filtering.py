import pandas
import numpy
import re

from statistics import stats
from variables import files_location


# Format the values of the dataset
def formatting(df, trial):
    prefix = 1000  # milli
    # Eliminate the Source SamplingFrequency and transform the values into milliseconds

    # For these two trials, samplingFrequency = 1 second
    if trial == '1' or trial == '4':
        df['delay'] = (df['delay'] - 1) * prefix

    # For these two trials, samplingFrequency = 5 seconds
    elif trial == '2' or trial == '5':
        df['delay'] = (df['delay'] - 5) * prefix

    # For these two trials, samplingFrequency = 10 seconds
    elif trial == '3' or trial == '6':
        df['delay'] = (df['delay'] - 10) * prefix
    return df


# Eliminate the unnecessary data
def runfilter(dataset, trial, protocol):
    # df = pandas.DataFrame()
    # if protocol == 'lwm2m':
    # df = pandas.read_csv(dataset, usecols=['Length', 'Time since previous frame', 'Code', 'Type'])
    df = pandas.read_csv(dataset, usecols=['Length', 'String value', 'Epoch Time', 'Request Method'])
    # df.rename(columns={'Time since previous frame': 'delay'}, inplace=True)
    df.rename(columns={'String value': 'Read Epoch'}, inplace=True)
    df.rename(columns={'Epoch Time': 'Arrive Epoch'}, inplace=True)
    df.rename(columns={'Length': 'length'}, inplace=True)
    # Drop columns with NAN values in Request Method
    ##df['Request Method'].str.contains('POST')
    df.dropna(subset=['Request Method'], inplace=True)

    # convert column to string
    ##data['Order_Date'] = data['Shipment ID'].str[:13]
    # In the column 'raw', extract single 13 digits in the strings
    df['Read Epoch'] = df['Read Epoch'].str.extract('(\d\d\d\d\d\d\d\d\d\d\d\d\d)', expand=True)
    # Drop columns with NAN values in Read Epoch
    df.dropna(subset=['Read Epoch'], inplace=True)
    # Prevent pandas converting large numbers to exponential
    df['Arrive Epoch'] = df['Arrive Epoch'].apply(lambda x: '{:.3f}'.format(x))

    # remove the . from the values
    df['Arrive Epoch'] = df['Arrive Epoch'].apply(str)
    df['Arrive Epoch'] = df['Arrive Epoch'].str.replace(r'\D', '')

    # insert new column delay that is the difference between the received and sent epoch times
    df['delay'] = df['Arrive Epoch'].astype(float) - df['Read Epoch'].astype(float)

    # Fetch only the 3 first numbers that represent the milliseconds in epoch
    # df['Arrival Time'] = df['Arrival Time'].str[:3]

    # df['Epoch'] = df[['Epoch Time', 'Arrival Time']].apply(lambda x: ''.join(x), axis=1)

    # Replace NaN values by empty values in two columns
    # df['Code'] = df['Code'].fillna('')
    # df['Type'] = df['Type'].fillna('')

    # Eliminate packets that typically do not carry sensing values
    ##df = df['Request Method'].str.contains('POST')
    ## df= df[df['String value'].str.contains(r'\bUPDATEE\b')]

    # undesired_codes = ["GET", "DELETE", "POST"]
    # mask_codes = df['Code'].str.contains(r'\b(?:{})\b'.format('|'.join(undesired_codes)))
    # df = df[~mask_codes]

    # undesired_types = ["Acknowledgement"]
    # mask_types = df['Type'].str.contains(r'\b(?:{})\b'.format('|'.join(undesired_types)))
    # df = df[~mask_types]

    # df = df[df['delay'] > 0]  # => typically reconnection Frame

    # insert new column delay that is the difference between the receivedand sent epoch times
    ##df['delay'] = df['Epoch Time'.replace('.', '').str[:13]] - df['String value'.split(',')[5].split('.'[1])]

    # if protocol == 'json':
    #     df = pandas.read_csv(dataset, usecols=['Length', 'Time since previous frame in this TCP stream',
    #                                            'Request Method', 'This frame is a (suspected) retransmission'])
    #     df.rename(columns={'This frame is a (suspected) retransmission': 'retransmission'}, inplace=True)
    #     df.rename(columns={'Time since previous frame in this TCP stream': 'delay'}, inplace=True)
    #     df.rename(columns={'Length': 'length'}, inplace=True)
    #     df.rename(columns={'Request Method': 'request'}, inplace=True)
    #     df['retransmission'] = df['retransmission'].fillna('no')
    #     df['request'] = df['request'].fillna('')
    #
    #     # Import only Post messages and do not import retransmission messages
    #     df = df[df['request'].str.contains('POST')]
    #     df = df[df['retransmission'].str.contains('no')]

    # include only the columns we want to plot
    df = df[df.columns[df.columns.isin(['length', 'delay'])]]
    # df[df.columns[df.columns.isin(['Epoch Time', 'Arrival Time'])]]

    # format the values
    # df = formatting(df, trial)
    return df


# Eliminate the unnecessary data
def runfilter2(dataorigin, dataend, labelorigin, labelend, protocol):
    df = pandas.DataFrame()
    # if protocol == 'lw':

    # #1 Insert new columns into the dataframe which values are data from origin and end
    # df['origin'] = helper(dataorigin)['epoch']
    # df['end'] = helper(dataend)['epoch']
    #
    # #2 insert new columns named 'delay' which values are the differences on epoch times
    # df['delay'] = df['origin'] - df['end']

    # 1 and 2 into one in milliseconds => nano/10^6
    df['delay'] = (helper(dataorigin)['epoch'] - helper(dataend)['epoch'])/1000000

    #Add new columns in df to enable a fusioned max columns between lenghts
    df['length origin'] = helper2(dataorigin)['length']
    df['length end'] = helper2(dataend)['length']

    df['max length'] = df[["length origin", "length end"]].max(axis=1)

    # include only the columns we want to plot
    df = df[df.columns[df.columns.isin(['delay', 'max length'])]]
    # frame = pandas.DataFrame()
    # frame= frame[[dataorigin['Length'].astype(float), dataend['Length'].astype(float)]]
    #
    # print 'dataorigin\n', frame
    # # compute the Bw occupancy
    stats(df['max length'],protocol)
    average_lengths = df['max length'].mean()
    sum_lengths = df['max length'].sum()

    print 'Delta delays between' + labelorigin + ' and ' + labelend + ' DataFrame\n', df
    return df


# Eliminate the unnecessary data and format the values
def helper(dfin):
    df = pandas.DataFrame(dfin[['Epoch Time']])

    # rename columns
    df.rename(columns={'Epoch Time': 'epoch'}, inplace=True)

    # Prevent pandas converting large numbers to exponential
    # power_scale = '9'  # nanoseconds
    # df['epoch'] = df['epoch'].apply(lambda x: '{:.'+power_scale+'f}'.format(x))
    df['epoch'] = df['epoch'].apply(lambda x: '{:.9f}'.format(x))

    # remove the . from the values so that we have it epoch in nanoseconds
    df['epoch'] = df['epoch'].str.replace(r'\D', '').astype(long)
    # convert the values into numbers for computing purposes later on
    df['epoch'] = df['epoch'].astype(long)

    #print 'helped delay  DataFrame\n', df
    return df

def helper2(dfin):
    df = pandas.DataFrame(dfin[['Length']])

    # rename columns
    df.rename(columns={'Length': 'length'}, inplace=True)

    # convert the values into numbers for computing purposes later on
    df['length'] = df['length'].astype(long)

    #print 'helped length DataFrame\n', df
    return df
