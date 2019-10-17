import pandas


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
    df = pandas.DataFrame()
    if protocol == 'lwm2m':
        df = pandas.read_csv(dataset, usecols=['Length', 'Time since previous frame', 'Code', 'Type'])
        #df = pandas.read_json(dataset, usecols=['Length', 'Time since previous frame', 'Code', 'Type'])
        df.rename(columns={'Time since previous frame': 'delay'}, inplace=True)
        df.rename(columns={'Length': 'length'}, inplace=True)
        # Replace NaN values by empty values in two columns
        df['Code'] = df['Code'].fillna('')
        df['Type'] = df['Type'].fillna('')

        # Eliminate packets that typically do not carry sensing values
        undesired_codes = ["GET", "DELETE", "POST"]
        mask_codes = df['Code'].str.contains(r'\b(?:{})\b'.format('|'.join(undesired_codes)))
        df = df[~mask_codes]

        undesired_types = ["Acknowledgement"]
        mask_types = df['Type'].str.contains(r'\b(?:{})\b'.format('|'.join(undesired_types)))
        df = df[~mask_types]

        df = df[df['delay'] > 0]  # => typically reconnection Frame

    if protocol == 'json':
        df = pandas.read_csv(dataset, usecols=['Length', 'Time since previous frame in this TCP stream',
                                               'Request Method', 'This frame is a (suspected) retransmission'])
        df.rename(columns={'This frame is a (suspected) retransmission': 'retransmission'}, inplace=True)
        df.rename(columns={'Time since previous frame in this TCP stream': 'delay'}, inplace=True)
        df.rename(columns={'Length': 'length'}, inplace=True)
        df.rename(columns={'Request Method': 'request'}, inplace=True)
        df['retransmission'] = df['retransmission'].fillna('no')
        df['request'] = df['request'].fillna('')

        # Import only Post messages and do not import retransmission messages
        df = df[df['request'].str.contains('POST')]
        df = df[df['retransmission'].str.contains('no')]

    # include only the columns we want to plot
    df = df[df.columns[df.columns.isin(['length', 'delay'])]]

    # format the values
    df = formatting(df, trial)
    return df
