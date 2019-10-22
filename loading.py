import pandas

from filtering import runfilter2
from variables import files_location


def run_import(myfile):
    df = pandas.read_csv(files_location + myfile + '.csv')
    #print myfile + ' DataFrame\n', df
    return df


# Data
df3origin = run_import('3-boxidaslwm2mtrace')
df3end = run_import('3-boxidaslwm2m')
runfilter2(df3origin, df3end, '3-boxidaslwm2mtrace', '3-boxidaslwm2m', 'lw')