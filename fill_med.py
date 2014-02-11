#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pandas as pd


def get_medidores(df):
    """Return the list of the meters"""
    medidores = df[0]

    return medidores.drop_duplicates()


def create_time_s(df, medidor, freq='15T'):
    """Create Time Series Complete for each meter(??)
    and merge with the data input"""
    dates_complete = pd.date_range('1/18/2013', '02/09/2014', freq='15T')
    # this dates take them from the file
    my_complete_series = pd.Series(dates_complete)
    frame1 = my_complete_series.to_frame()
    frame1.columns = ['key']
    merged = pd.merge(frame1, df, on='key', how='outer')
    merged = merged.sort('key')
    # fill the merged file with the number of the meter
    merged['medidor'].fillna(medidor, inplace=True)

    return merged


def clean_file(df):
    """Remove duplicates and zero values"""
    df_clean = df.drop_duplicates()
    df_no_zeros = df_clean[df_clean[2] != 0]
    df_sorted = df_no_zeros.sort()

    return df_sorted


def main():

    df = pd.read_csv("Data/medidas.txt", header=None,
                     parse_dates=[1], keep_date_col=True)
    df_clean = clean_file(df)
    medidores = get_medidores(df_clean)
    df_clean.columns = ['medidor', 'key', 'value']
    merged_med = map(lambda med: create_time_s(
                     df_clean[df_clean['medidor'] == med], med), medidores)
    interpolated = map(lambda merg: merg.interpolate(), merged_med)

    for i in range(len(interpolated)):
        print "Data number before %d and after %d in meter %d." % (merged_med[i]['value'].count(), 
                                                                   interpolated[i]['value'].count(),
                                                                   medidores.iloc[i])

if __name__ == '__main__':
    main()
