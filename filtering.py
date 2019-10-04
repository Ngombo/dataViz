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
    if protocol == 'lwm2m':
        df = pandas.read_csv(dataset, usecols=['Length', 'Time since previous frame'])
        df.rename(columns={'Time since previous frame': 'delay'}, inplace=True)
        df.rename(columns={'Length': 'length'}, inplace=True)
        df = formatting(df, trial)
        return df
    else:
        df = pandas.read_csv(dataset, usecols=['Length', 'Time since previous frame in this TCP stream',
                                               'Request Method', 'This frame is a (suspected) retransmission'])
        df.rename(columns={'This frame is a (suspected) retransmission': 'retransmission'}, inplace=True)
        df.rename(columns={'Time since previous frame in this TCP stream': 'delay'}, inplace=True)
        df.rename(columns={'Length': 'length'}, inplace=True)
        df.rename(columns={'Request Method': 'request'}, inplace=True)

        # Import only Post messages and Do not import retransmission messages
        df1 = df[df['request'].str.contains("POST") & df['retransmission'].str.contains(" ")]
        df1 = formatting(df1, trial)
        return df1


