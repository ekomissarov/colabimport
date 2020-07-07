import pandas as pd
import matplotlib as mpl


def cry_qkrq():
    print("qkrq!")
    return "qkrq!"


def scale_plot_size(x, y):
    #default_figsize = mpl.rcParamsDefault['figure.figsize']
    mpl.rcParams['figure.figsize'] = [x, y]


def calc_additive_values(df):
    # приводим метрики к аддитивным величинам для расчетов взвешенным значениям сводных таблицах
    # https://support.google.com/google-ads/answer/7501826?hl=en
    # https://support.google.com/google-ads/answer/2497703?hl=en
    df["eligible_impressions"] = df["impressions"]/(df['search_impression_share']/100)
    df["search_abs_top_is"] *= df["eligible_impressions"]/100
    df["search_top_is"] *= df["eligible_impressions"]/100
    # https://yandex.ru/dev/direct/doc/reports/report-format-docpage/
    df['avg_impression_pos'] *= df["impressions"]
    df['avg_traffic_vol'] *= df["impressions"]
    df['avg_click_pos'] *= df["clicks"]
    return df


def calc_base_values(tt):
    tt['cost'] /= 1000000

    tt['events'] = tt['total_events'] + tt['total_events_app']
    tt['ads'] = tt['total_b2bevents'] + tt['total_b2bevents_app']
    tt['ipotek'] = tt['uniq_ipotek_events'] + tt['uniq_ipotek_events_app']

    tt['cpa'] = tt['cost'] / tt['events']
    tt['cpad'] = tt['cost'] / tt['ads']
    tt['cpa_ipotek'] = tt['cost'] / tt['ipotek']

    tt['cpc'] = tt['cost'] / tt['clicks']
    tt['ctr'] = tt['clicks'] / tt['impressions']

    tt['conv_ev'] = tt['clicks'] / (tt['total_events'] + tt['total_events_app'])
    tt['conv_ad'] = tt['clicks'] / (tt['total_b2bevents'] + tt['total_b2bevents_app'])
    tt['conv_ipotek'] = tt['clicks'] / (tt['uniq_ipotek_events'] + tt['uniq_ipotek_events_app'])
    return tt


def plot_basic_dynamics(df, region_filters=None, campaign_filters=None, system_filters=None):
    grp = ['date']

    if region_filters:
        df = df[df.region.isin(region_filters)]

    if system_filters:
        df = df[df.system.isin(system_filters)]

    if campaign_filters:
        campaign_mask = pd.Series(False, index=df.index)
        for i in campaign_filters:
            campaign_mask = campaign_mask | (df.campaignname.str.contains(i))
        df = df[campaign_mask]

    df = df.groupby(grp)
    tt = df[['cost',
             'impressions', 'clicks',
             'total_events', 'total_events_app',
             'total_b2bevents', 'total_b2bevents_app',
             'uniq_ipotek_events', 'uniq_ipotek_events_app', ]].sum()
    tt = calc_base_values(tt)

    scale_plot_size(12, 12)
    plots = ["events", "cpa"]
    tt.loc[:, plots].plot(subplots=True)
    plots = ["ads", "cpad"]
    tt.loc[:, plots].plot(subplots=True)
    plots = ["ipotek", "cpa_ipotek"]
    tt.loc[:, plots].plot(subplots=True)
    plots = ["cost", "cpc", "ctr", "clicks"]
    tt.loc[:, plots].plot(subplots=True)


def plot_avg_position_yandex(df, region_filters=None, campaign_filters=None):
    grp = ['date']
    df = df[df.system == "y"]

    if region_filters:
        df = df[df.region.isin(region_filters)]

    if campaign_filters:
        campaign_mask = pd.Series(False, index=df.index)
        for i in campaign_filters:
            campaign_mask = campaign_mask | (df.campaignname.str.contains(i))
        df = df[campaign_mask]

    tt = df.groupby(grp).aggregate({'impressions': 'sum', 'clicks': 'sum',
                                    'avg_impression_pos': 'sum', 'avg_click_pos': 'sum',
                                    'avg_traffic_vol': 'sum'})
    tt = tt.apply(pd.to_numeric)  # Decimal to float
    tt['impr_pos'] = tt['avg_impression_pos'] / tt['impressions']
    tt['click_pos'] = tt['avg_click_pos'] / tt['clicks']
    tt['traffic_vol'] = tt['avg_traffic_vol'] / tt['impressions']

    scale_plot_size(12, 12)
    plots = ["impr_pos", "click_pos", "traffic_vol"]
    tt.loc[:, plots].plot(subplots=True)


def plot_top_is_position_google(df, region_filters=None, campaign_filters=None):
    grp = ['date']
    df = df[df.system == "g"]

    if region_filters:
        df = df[df.region.isin(region_filters)]

    if campaign_filters:
        campaign_mask = pd.Series(False, index=df.index)
        for i in campaign_filters:
            campaign_mask = campaign_mask | (df.campaignname.str.contains(i))
        df = df[campaign_mask]

    tt = df.groupby(grp).aggregate({'search_abs_top_is': 'sum', 'search_top_is': 'sum',
                                    'eligible_impressions': 'sum'})
    tt = tt.apply(pd.to_numeric)  # Decimal to float
    tt['top_is'] = tt['search_top_is'] / tt['eligible_impressions']
    tt['abstop_is'] = tt['search_abs_top_is'] / tt['eligible_impressions']

    scale_plot_size(12, 12)
    plots = ["top_is", "abstop_is"]
    tt.loc[:, plots].plot(subplots=True)
