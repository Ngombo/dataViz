import pandas
import numpy
import re
from statistics import stats


# Eliminate the unnecessary data
def filter_end_delays(df):
    df.rename(columns={'json.value.string': 'Read Epoch'}, inplace=True)
    df.rename(columns={'frame.time_epoch': 'Arrive Epoch'}, inplace=True)

    # Drop columns with NAN values in Request Method
    df.dropna(subset=['http.request.method'], inplace=True)

    # In the column 'raw', extract single 19 digits in the strings => nanoseconds epoch
    df['Read Epoch'] = df['Read Epoch'].str.extract('(\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d)', expand=True)
    # Drop columns with NAN values in Read Epoch
    df.dropna(subset=['Read Epoch'], inplace=True)
    # Prevent pandas converting large numbers to exponential
    df['Arrive Epoch'] = df['Arrive Epoch'].apply(lambda x: '{:.3f}'.format(x))

    # remove the . from the values
    df['Arrive Epoch'] = df['Arrive Epoch'].apply(str)
    df['Arrive Epoch'] = df['Arrive Epoch'].str.replace(r'\D', '')

    # insert new column delay that is the difference between the received and sent epoch times
    precision = 1000000  # eliminate the nanosecond scale because, js do not provide epoch to this level
    df['delay'] = df['Arrive Epoch'].astype(float) / precision - df['Read Epoch'].astype(float) / precision

    # include only the columns we want to plot
    df = df[df.columns[df.columns.isin(['delay'])]]
    return df


# Eliminate the unnecessary data
def filter_network_data(dataorigin, dataend, label):
    df = pandas.DataFrame()
    # Insert new columns named 'delay' which values are the differences on epoch times
    # in milliseconds => nano/10^6 and rounded to two decimals
    delay_value = (helper(dataend)['epoch'] - helper(dataorigin)['epoch']) / 1000000
    df['delay'] = numpy.round(delay_value, 2)

    # Add new columns in df to enable a fusioned max columns between lenghts
    df['length origin'] = helper2(dataorigin)['length']
    df['length end'] = helper2(dataend)['length']

    # Select the bigger number between the two values to feed the new column 'max length'
    df['max length'] = df[["length origin", "length end"]].max(axis=1)

    # include only the columns we want to plot
    df = df[df.columns[df.columns.isin(['delay', 'max length'])]]

    # Drop columns with NAN values in delay for the case the number of received packets is not the same as the sent one
    df.dropna(subset=['delay'], inplace=True)

    # print 'dataorigin\n', frame

    # Compute Stats results
    stats(df['max length'], label)

    print 'Delta delays between for ' + label + '\n', df
    return df


# Eliminate the unnecessary data and format the values
def helper(dfin):
    df = pandas.DataFrame(dfin[['frame.time_epoch']])  # , 'frame.number']])

    # rename columns
    df.rename(columns={'frame.time_epoch': 'epoch'}, inplace=True)

    # Prevent pandas converting large numbers to exponential
    # power_scale = '9'  # nanoseconds
    # df['epoch'] = df['epoch'].apply(lambda x: '{:.'+power_scale+'f}'.format(x))
    #df['epoch'] = df['epoch'].apply(lambda x: '{:.9f}'.format(x))

    # remove the . from the values so that we have it epoch in nanoseconds
    df['epoch'] = df['epoch'].str.replace(r'\D', '').astype(long)

    # convert the values into numbers for computing purposes later on
    df['epoch'] = df['epoch'].astype(long)

    #print 'helped delay  DataFrame\n', df
    return df


def helper2(dfin):
    df = pandas.DataFrame(dfin[['frame.cap_len']])

    # rename columns
    df.rename(columns={'frame.cap_len': 'length'}, inplace=True)

    # convert the values into numbers for computing purposes later on
    df['length'] = df['length'].astype(long)

    # print 'helped length DataFrame\n', df
    return df
