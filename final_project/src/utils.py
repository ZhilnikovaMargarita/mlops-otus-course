import pandas as pd

additional_columns = [
    'city_kazan',
    'city_moscow',
    'city_nnovgorod',
    'city_other',
    'city_spb',
    'city_voronezh',
    'cnts_60',
    'f_class_business',
    'f_class_econom',
    'f_class_vip',
    'is_airport',
    'is_train',
    's_class_business',
    's_class_econom',
    's_class_vip',
    't_class_business',
    't_class_econom',
    't_class_vip',
]

def get_city(df: pd.DataFrame):
    df['city'] = 'other'
    df.loc[
        df['lat'].between(59.4, 60.3)
        & df['lon'].between(29.23, 31.394),
        'city'
    ] = 'spb'
    
    df.loc[
        df['lat'].between(54.35, 56.7)
        & df['lon'].between(35.05, 39.86),
        'city'
    ] = 'moscow'
    
    df.loc[
        df['lat'].between(49.68, 52.03)
        & df['lon'].between(37.68, 43.35),
        'city'
    ] = 'voronezh'
    
    df.loc[
        df['lat'].between(55.95, 56.45)
        & df['lon'].between(43.38, 44.76),
        'city'
    ] = 'nnovgorod'
    
    df.loc[
        df['lat'].between(55.46, 55.94)
        & df['lon'].between(48.54, 50.06),
        'city'
    ] = 'kazan'
    
    df['location'] = ''
    
    df.loc[
        (df['lat'] == 55.414327)
        & (df['lon'] == 37.900470),
        'location'
    ] = 'dme_airport'
    
    df.loc[
        (df['lat'] == 55.962873)
        & (df['lon'] == 37.405977),
        'location'
    ] = 'svo_airport'
    
    df.loc[
        (df['lat'] == 55.963949)
        & (df['lon'] == 37.41688900000001),
        'location'
    ] = 'svo_d_airport'
    
    df.loc[
        (df['lat'] == 55.776507)
        & (df['lon'] == 37.581550),
        'location'
    ] = 'blr_railway'
    
    df.loc[
        (df['lat'] == 55.77688199999999)
        & (df['lon'] == 37.654808),
        'location'
    ] = 'leningr_railway'
    
    df.loc[
        (df['lat'] == 55.729802)
        & (df['lon'] == 37.64056),
        'location'
    ] = 'pav_railway'
    
    df.loc[
        (df['lat'] == 55.744632)
        & (df['lon'] == 37.566072),
        'location'
    ] = 'kyiv_railway'   
    
    df.loc[
        (df['lat'] == 55.754203)
        & (df['lon'] == 37.556388),
        'location'
    ] = 'itc_bc'
    
    df.loc[
        (df['lat'] == 55.774963)
        & (df['lon'] == 37.55045),
        'location'
    ] = 'begovaya_bc'
    
    df.loc[
        (df['lat'] == 55.973637)
        & (df['lon'] == 37.412352),
        'location'
    ] = 'svo__airport'
    
    df.loc[
        (df['lat'] == 55.973637)
        & (df['lon'] == 37.412352),
        'location'
    ] = 'svo__airport'
    
    df.loc[
        (df['lat'] == 55.773089)
        & (df['lon'] == 37.656532),
        'location'
    ] = 'kazan_railway'
    
    df.loc[
        (df['lat'] == 55.415283)
        & (df['lon'] == 37.896275),
        'location'
    ] = 'dme_airport'
    
    df.loc[
        (df['lat'] == 55.80664599999999)
        & (df['lon'] == 37.542958),
        'location'
    ] = 'hse'
    
    df.loc[
        (df['lat'] == 55.806241)
        & (df['lon'] == 37.545294),
        'location'
    ] = 'hse_bc'
    
    df.loc[
        (df['lat'] == 55.757399)
        & (df['lon'] == 37.660853),
        'location'
    ] = 'kur_railway'
    
    df.loc[
        (df['lat'] == 55.75131)
        & (df['lon'] == 37.584613),
        'location'
    ] = 'lotte_bc'
    
    df.loc[
        (df['lat'] == 55.963833)
        & (df['lon'] == 37.415685),
        'location'
    ] = 'svo_e_airport'
    
    df.loc[
        (df['lat'] == 55.605439)
        & (df['lon'] == 37.286732),
        'location'
    ] = 'vko_airport'
    
    df.loc[
        (df['lat'] == 55.747728)
        & (df['lon'] == 37.538871),
        'location'
    ] = 'msk_city_bc'
    
    df.loc[
        (df['lat'] == 55.757222)
        & (df['lon'] == 37.659075),
        'location'
    ] = 'kur_railway_'
    
    df.loc[
        (df['lat'] == 55.797154000000006)
        & (df['lon'] == 37.520707),
        'location'
    ] = 'tr_palace'
    

    df.loc[
        (df['lat'] == 55.74674)
        & (df['lon'] == 37.537461),
        'location'
    ] = 'msk_city_bc_'
    
    
    df.loc[
        (df['lat'] == 55.595348)
        & (df['lon'] == 37.268819),
        'location'
    ] = 'vko__airport'
    
    df.loc[
        (df['lat'] == 55.731713)
        & (df['lon'] == 37.48735300000001),
        'location'
    ] = 'kut_tc'
    
    df.loc[
        (df['lat'] == 55.755353)
        & (df['lon'] == 37.560071),
        'location'
    ] = 'tec_n7'
    
    df.loc[
        (df['lat'] == 59.798037)
        & (df['lon'] == 30.271182),
        'location'
    ] = 'pulkovo_airport'
    
    df.loc[
        (df['lat'] == 59.92978100000001)
        & (df['lon'] == 30.362203000000004),
        'location'
    ] = 'mosk_railway_spb'
    
    df.loc[
        (df['lat'] == 56.32192)
        & (df['lon'] == 43.946006),
        'location'
    ] = 'mosk_railway_nn'
    
    df.loc[
        (df['lat'] == 55.606438)
        & (df['lon'] == 49.302227),
        'location'
    ] = 'kzn_airport'

    return df


def get_time_feats(df, hdays):
    df['wday'] = df['datetime'].dt.weekday
    df['isweekend'] = df['wday'].isin([5, 6])
    df['isfriday'] = df['wday'] == 4

    df['month'] = df['datetime'].dt.month
    
    df['minutes'] = df['datetime'].dt.minute
    df['hours'] = df['datetime'].dt.hour
    df['minutes'] += 60 * df['hours']
    
    df['date'] = df['datetime'].dt.date
    
    df['isholiday'] = df['date'].apply(lambda x: x in hdays)

    
    df['morning'] = (df['hours'] >= 6) & (df['hours'] < 12)
    df['afternoon'] = (df['hours'] >= 12) & (df['hours'] < 18)
    df['evening'] = (df['hours'] >= 18) & (df['hours'] < 24)
    df['night'] = (df['hours'] >= 0) & (df['hours'] < 6)
        
    # Понедельник после праздников
    df['is_day_after'] = (
        ((df['month'] == 2) & (df['datetime'].dt.day == 24))
        | ((df['month'] == 3) & (df['datetime'].dt.day == 10))
    ).astype(int)
    
    return df


def get_cnts(df: pd.DataFrame, roll_periods=[60]):
    data = df.sort_values('datetime')
    data = data.assign(is_call=1)
    data['datetime'] = data['datetime'].round('min')
    data = data.set_index('datetime').resample('1T')['is_call'].sum()
    
    out_dict = {} 
    # можно считать для разных периодов, но лучше всего работает 60
    for period in roll_periods:
        out_dict[period] = data.rolling(period).sum()    
    data = data.reset_index()
    for period in roll_periods:
        data[f'cnts_{period}'] = out_dict[period].values

    data = data.drop(columns=['is_call'])
    data['datetime'] = pd.to_datetime(data['datetime'])
    
    return pd.merge(df, data, on=['datetime'], how='left')