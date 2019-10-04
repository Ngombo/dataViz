import pandas
from filtering import runfilter


# Create DF sets, where to load the prepared dataFrame by the helper method

def load(traffic, trial, protocol):
    df = pandas.DataFrame(runfilter('C:/Users/X260/Desktop/raw/' + trial + '-' + traffic + '.csv', trial, protocol))
    return df
