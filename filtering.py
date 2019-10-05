import pandas


# Format the values of the dataset
def formatting(df, trial):
    # Eliminate the Source SamplingFrequency and transform the values into milliseconds
    if trial == '1':
        df['delay'] = (df['delay'] - 1) * 1000
    elif trial == '2':
        df['delay'] = (df['delay'] - 5) * 1000
    elif trial == '3':
        df['delay'] = (df['delay'] - 10) * 1000
    return df


# Eliminate the unnecessary data
def runfilter(dataset, trial, protocol):
    df = pandas.DataFrame()
    if protocol == 'lwm2m':
        df = pandas.read_csv(dataset, usecols=['Length', 'Time since previous frame'])
        df.rename(columns={'Time since previous frame': 'delay'}, inplace=True)
        df.rename(columns={'Length': 'length'}, inplace=True)
        df = formatting(df, trial)
        # return df
    if protocol == 'json':
        df = pandas.read_csv(dataset, usecols=['Length', 'Time since previous frame in this TCP stream',
                                               'Request Method', 'This frame is a (suspected) retransmission'])
        df.rename(columns={'This frame is a (suspected) retransmission': 'retransmission'}, inplace=True)
        df.rename(columns={'Time since previous frame in this TCP stream': 'delay'}, inplace=True)
        df.rename(columns={'Length': 'length'}, inplace=True)
        df.rename(columns={'Request Method': 'request'}, inplace=True)
        # Replace NaN values by empty values in two columns
        df['retransmission'] = df['retransmission'].fillna('no')
        df['request'] = df['request'].fillna('')

        # Import only Post messages and Do not import retransmission messages
        df = df[df['request'].str.contains("POST")]
        df = df[df['retransmission'].str.contains("no")]

        # include the columns we want
        df = df[df.columns[df.columns.isin(['length', 'delay'])]]

        df = formatting(df, trial)
    return df
