import pandas as pd
import matplotlib as mpl
from colabimport.colab import mediaplan

def scale_plot_size(x, y):
    #default_figsize = mpl.rcParamsDefault['figure.figsize']
    mpl.rcParams['figure.figsize'] = [x, y]


def calc_additive_values(df):
    for i in ("search_abs_top_is", "search_top_is", "search_impression_share",
              "avg_impression_pos", "avg_traffic_vol", "avg_click_pos"):
        df[i] = df[i].apply(pd.to_numeric)

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
    tt['ct'] = tt['total_ct_events'] + 0

    tt['cpa'] = tt['cost'] / tt['events']
    tt['cpad'] = tt['cost'] / tt['ads']
    tt['cpa_ipotek'] = tt['cost'] / tt['ipotek']
    tt['cpa_ct'] = tt['cost'] / tt['total_ct_events']

    tt['cpc'] = tt['cost'] / tt['clicks']
    tt['ctr'] = tt['clicks'] / tt['impressions']

    tt['ev_per_click'] = (tt['total_events'] + tt['total_events_app']) / tt['clicks']
    tt['ad_per_click'] = (tt['total_b2bevents'] + tt['total_b2bevents_app']) / tt['clicks']
    tt['ipotek_per_click'] = (tt['uniq_ipotek_events'] + tt['uniq_ipotek_events_app']) / tt['clicks']
    tt['ct_per_click'] = tt['total_ct_events'] / tt['clicks']
    return tt


def plot_basic_dynamics(df, what=None, region_filters=None, campaign_filters=None, system_filters=None):
    grp = ['date']
    if what == None:
        what = {"events", "ads", "ipotek", "ct", "common"}

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
             'uniq_ipotek_events', 'uniq_ipotek_events_app',
             'total_ct_events']].sum()
    tt = calc_base_values(tt)

    scale_plot_size(12, 12)
    if "events" in what:
        plots = ["events", "cpa"]
        tt.loc[:, plots].plot(subplots=True)
    if "ads" in what:
        plots = ["ads", "cpad"]
        tt.loc[:, plots].plot(subplots=True)
    if "ipotek" in what:
        plots = ["ipotek", "cpa_ipotek"]
        tt.loc[:, plots].plot(subplots=True)
    if "ct" in what:
        plots = ["ct", "cpa_ct"]
        tt.loc[:, plots].plot(subplots=True)
    if "common" in what:
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


def plot_compare_base(df, y_value='ad_per_click', group_by_plot='regclass', plot_set=['msk', 'spb', 'p4c', '18reg'],
                 region_filters=None, campaign_filters=None, system_filters=None):
    regions_map = mediaplan.GroupsRegions()
    reg_classes = pd.DataFrame([{"campaignname": i, "regclass": regions_map[i]} for i in set(df.campaignname.unique())])
    data = pd.merge(df, reg_classes)

    if region_filters:
        df = df[df.region.isin(region_filters)]

    if system_filters:
        df = df[df.system.isin(system_filters)]

    if campaign_filters:
        campaign_mask = pd.Series(False, index=df.index)
        for i in campaign_filters:
            campaign_mask = campaign_mask | (df.campaignname.str.contains(i))
        df = df[campaign_mask]

    tt = data.groupby([group_by_plot] + ['date']).sum()
    tt = sunset.calc_base_values(tt)

    plotdata = pd.DataFrame({i: tt.loc[i][y_value] for i in plot_set})
    for i in plotdata:
        plt.plot(plotdata.index, plotdata[i], label="{}: {}".format(group_by_plot, i))

    plt.plot()

    plt.xlabel("дата")
    plt.ylabel(y_value)
    plt.title("график сравнение")
    plt.legend()
    plt.show()
