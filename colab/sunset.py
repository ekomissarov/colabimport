import pandas as pd
import matplotlib as mpl
import matplotlib.dates as mdates
import numpy as np
import matplotlib.pyplot as plt
from . import mediaplan

def scale_plot_size(x, y):
    #default_figsize = mpl.rcParamsDefault['figure.figsize']
    mpl.rcParams['figure.figsize'] = [x, y]


def calc_additive_values(df):
    # приводим метрики к аддитивным величинам для расчетов взвешенным значениям сводных таблицах
    # https://support.google.com/google-ads/answer/7501826?hl=en
    # https://support.google.com/google-ads/answer/2497703?hl=en
    for i in ('impr_top_percent', 'impr_abs_top_percent',
              'search_abs_top_is', 'search_top_is', 'search_impression_share',
              'avg_impression_pos', 'avg_traffic_vol', 'avg_click_pos'):
        if i in df.columns:
            df[i] = df[i].apply(pd.to_numeric)

    if 'search_impression_share' in df.columns:
        df["eligible_impressions"] = np.round(df["impressions"]/(df['search_impression_share'] / 100), 4)
        df["search_abs_top_is"] = np.round(df["search_abs_top_is"] * df["eligible_impressions"] / 100, 4)
        df["search_top_is"] = np.round(df["search_top_is"] * df["eligible_impressions"] / 100, 4)

    if 'impr_top_percent' in df.columns:
        df["impr_top_percent"] = np.round(df["impr_top_percent"] * df["impressions"] / 100, 4)
    if 'impr_abs_top_percent' in df.columns:
        df["impr_abs_top_percent"] = np.round(df["impr_abs_top_percent"] * df["impressions"] / 100, 4)

    # https://yandex.ru/dev/direct/doc/reports/report-format-docpage/
    df['avg_impression_pos'] = np.round(df['avg_impression_pos'] * df["impressions"], 4)
    df['avg_traffic_vol'] = np.round(df['avg_traffic_vol'] * df["impressions"], 4)
    df['avg_click_pos'] = np.round(df['avg_click_pos'] * df["clicks"], 4)
    return df


def calc_base_values(tt):
    tt['cost_rur'] = tt['cost'] / 1000000
    tt['cpc'] = np.round(tt['cost_rur'] / tt['clicks'], 2)
    tt['ctr'] = np.round(tt['clicks'] / tt['impressions'], 4)

    # конверсии объем
    tt['events'] = tt['total_events'] + tt['total_events_app']
    tt['events_fdv'] = tt['total_events_fdv'] + tt['total_events_app_fdv']
    tt['ads'] = tt['total_b2bevents'] + tt['total_b2bevents_app']
    tt['ipotek'] = tt['uniq_ipotek_events'] + tt['uniq_ipotek_events_app']
    tt['ct'] = tt['total_ct_events'] + 0

    # конверсии стоимости
    tt['cpa'] = np.round(tt['cost_rur'] / tt['events'], 2)
    tt['cpa_fdv'] = np.round(tt['cost_rur'] / tt['events_fdv'], 2)
    tt['cpad'] = np.round(tt['cost_rur'] / tt['ads'], 2)
    tt['cpa_ipotek'] = np.round(tt['cost_rur'] / tt['ipotek'], 2)
    tt['cpa_ct'] = np.round(tt['cost_rur'] / tt['ct'], 2)

    # %конверсии на клик
    tt['ev_per_click'] = np.round(tt['events'] / tt['clicks'], 4)
    tt['ev_fdv_per_click'] = np.round(tt['events_fdv'] / tt['clicks'], 4)
    tt['ad_per_click'] = np.round(tt['ads'] / tt['clicks'], 4)
    tt['ipotek_per_click'] = np.round(tt['ipotek'] / tt['clicks'], 4)
    tt['ct_per_click'] = np.round(tt['ct'] / tt['clicks'], 4)

    # %ассоциированные конверсии на клик
    tt['assisted_ev_per_click'] = np.round(tt['assisted_conv_phones'] / tt['clicks'], 4)
    tt['assisted_ad_per_click'] = np.round(tt['assisted_conv_ads'] / tt['clicks'], 4)
    tt['assisted_ipotek_per_click'] = np.round(tt['assisted_conv_mortgage'] / tt['clicks'], 4)
    tt['assisted_ct_per_click'] = np.round(tt['assisted_conv_ct'] / tt['clicks'], 4)

    # агрегаты: конверсии объем
    tt['conv_agg_full'] = tt['events'] + (8 * tt['ads']) + (500 * tt['ipotek']) + (500 * tt['ct'])

    # агрегаты: конверсии стоимости
    tt['cp_agg_full'] = np.round(tt['cost_rur'] / tt['conv_agg_full'], 2)

    # агрегаты: %конверсии на клик
    tt['agg_full_per_click'] = np.round(tt['conv_agg_full'] / tt['clicks'], 4)

    tt['cost_rur'] = tt['cost_rur'].astype(np.int64)
    return tt


def plot_basic_rolling(*lines, items=["events", "cpa"], line_colors=["darkblue", "orange"]):
    fig, axN = plt.subplots(len(lines), 1)

    for i, line in enumerate(lines):
        axN[i].plot(line.index, line['values'], '-', color=line_colors[i])
        axN[i].plot(line.index, line['rolling_mean'], '--', color='gray')
        axN[i].plot(line.index, line['rolling_std'], ':', color='gray')
        axN[i].lines[1].set_alpha(0.5)
        axN[i].lines[2].set_alpha(0.5)
        locator = mdates.AutoDateLocator(minticks=0, maxticks=3)
        formatter = mdates.ConciseDateFormatter(locator)
        axN[i].legend([items[i], 'rolling_mean', 'rolling_std'])
        axN[i].xaxis.set_major_locator(locator)
        axN[i].xaxis.set_major_formatter(formatter)

    locator = mdates.AutoDateLocator(minticks=5, maxticks=20)
    formatter = mdates.ConciseDateFormatter(locator)
    axN[i].xaxis.set_major_locator(locator)
    axN[i].xaxis.set_major_formatter(formatter)
    plt.show()


def plot_basic_dynamics(df, what=None, region_filters=None, campaign_filters=None, system_filters=None, plot_ev_per_click = False):
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

    tt = df.groupby(grp).sum()
    tt = calc_base_values(tt)
    tt.index = pd.to_datetime(tt.index)

    scale_plot_size(12, 14)
    if "events" in what:
        events = tt.loc[:, "events"]
        cpas = tt.loc[:, "cpa"]
        rolling_ev = events.rolling(7, center=True)
        rolling_cpas = cpas.rolling(7, center=True)
        events = pd.DataFrame({'values': events, 'rolling_mean': rolling_ev.mean(), 'rolling_std': rolling_ev.std()})
        cpas = pd.DataFrame({'values': cpas, 'rolling_mean': rolling_cpas.mean(), 'rolling_std': rolling_cpas.std()})
        if plot_ev_per_click:
            ev_per_click = tt.loc[:, "ev_per_click"]
            rolling_convsperclick = ev_per_click.rolling(7, center=True)
            ev_per_click = pd.DataFrame({'values': ev_per_click, 'rolling_mean': rolling_convsperclick.mean(), 'rolling_std': rolling_convsperclick.std()})
            plot_basic_rolling(events, cpas, ev_per_click, items=["phone events", "cpa", "conv%"],
                               line_colors=["darkblue", "orange", "darkgreen"])
        else:
            plot_basic_rolling(events, cpas, items=["phone events", "cpa"])
    if "ads" in what:
        events = tt.loc[:, "ads"]
        cpas = tt.loc[:, "cpad"]
        rolling_ev = events.rolling(7, center=True)
        rolling_cpas = cpas.rolling(7, center=True)
        events = pd.DataFrame({'values': events, 'rolling_mean': rolling_ev.mean(), 'rolling_std': rolling_ev.std()})
        cpas = pd.DataFrame({'values': cpas, 'rolling_mean': rolling_cpas.mean(), 'rolling_std': rolling_cpas.std()})
        if plot_ev_per_click:
            ev_per_click = tt.loc[:, "ad_per_click"]
            rolling_convsperclick = ev_per_click.rolling(7, center=True)
            ev_per_click = pd.DataFrame({'values': ev_per_click, 'rolling_mean': rolling_convsperclick.mean(), 'rolling_std': rolling_convsperclick.std()})
            plot_basic_rolling(events, cpas, ev_per_click, items=["ads", "cpad", "conv%"],
                               line_colors=["darkblue", "orange", "darkgreen"])
        else:
            plot_basic_rolling(events, cpas, items=["ads", "cpad"])
    if "ipotek" in what:
        events = tt.loc[:, "ipotek"]
        cpas = tt.loc[:, "cpa_ipotek"]
        rolling_ev = events.rolling(7, center=True)
        rolling_cpas = cpas.rolling(7, center=True)
        events = pd.DataFrame({'values': events, 'rolling_mean': rolling_ev.mean(), 'rolling_std': rolling_ev.std()})
        cpas = pd.DataFrame({'values': cpas, 'rolling_mean': rolling_cpas.mean(), 'rolling_std': rolling_cpas.std()})
        if plot_ev_per_click:
            ev_per_click = tt.loc[:, "ipotek_per_click"]
            rolling_convsperclick = ev_per_click.rolling(7, center=True)
            ev_per_click = pd.DataFrame({'values': ev_per_click, 'rolling_mean': rolling_convsperclick.mean(), 'rolling_std': rolling_convsperclick.std()})
            plot_basic_rolling(events, cpas, ev_per_click, items=["ipotek", "cpa_ipotek", "conv%"],
                               line_colors=["darkblue", "orange", "darkgreen"])
        else:
            plot_basic_rolling(events, cpas, items=["ipotek", "cpa_ipotek"])
    if "ct" in what:
        events = tt.loc[:, "ct"]
        cpas = tt.loc[:, "cpa_ct"]
        rolling_ev = events.rolling(7, center=True)
        rolling_cpas = cpas.rolling(7, center=True)
        events = pd.DataFrame({'values': events, 'rolling_mean': rolling_ev.mean(), 'rolling_std': rolling_ev.std()})
        cpas = pd.DataFrame({'values': cpas, 'rolling_mean': rolling_cpas.mean(), 'rolling_std': rolling_cpas.std()})
        if plot_ev_per_click:
            ev_per_click = tt.loc[:, "ct_per_click"]
            rolling_convsperclick = ev_per_click.rolling(7, center=True)
            ev_per_click = pd.DataFrame({'values': ev_per_click, 'rolling_mean': rolling_convsperclick.mean(), 'rolling_std': rolling_convsperclick.std()})
            plot_basic_rolling(events, cpas, ev_per_click, items=["ct", "cpa_ct", "conv%"],
                               line_colors=["darkblue", "orange", "darkgreen"])
        else:
            plot_basic_rolling(events, cpas, items=["ct", "cpa_ct"])
    if "common" in what:
        cost_rur = tt.loc[:, "cost_rur"]
        cpc = tt.loc[:, "cpc"]
        ctr = tt.loc[:, "ctr"]
        clicks = tt.loc[:, "clicks"]
        rolling_cost_rur = cost_rur.rolling(7, center=True)
        rolling_cpc = cpc.rolling(7, center=True)
        rolling_ctr = ctr.rolling(7, center=True)
        rolling_clicks = clicks.rolling(7, center=True)
        cost_rur = pd.DataFrame({'values': cost_rur, 'rolling_mean': rolling_cost_rur.mean(), 'rolling_std': rolling_cost_rur.std()})
        cpc = pd.DataFrame({'values': cpc, 'rolling_mean': rolling_cpc.mean(), 'rolling_std': rolling_cpc.std()})
        ctr = pd.DataFrame({'values': ctr, 'rolling_mean': rolling_ctr.mean(), 'rolling_std': rolling_ctr.std()})
        clicks = pd.DataFrame({'values': clicks, 'rolling_mean': rolling_clicks.mean(), 'rolling_std': rolling_clicks.std()})
        plot_basic_rolling(cost_rur, cpc, ctr, clicks,
                           items=["cost_rur", "cpc", "ctr", "clicks"],
                           line_colors=["darkblue", "orange", "green", "red"])


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
        data = data[data.region.isin(region_filters)]

    if system_filters:
        data = data[data.system.isin(system_filters)]

    if campaign_filters:
        campaign_mask = pd.Series(False, index=data.index)
        for i in campaign_filters:
            campaign_mask = campaign_mask | (data.campaignname.str.contains(i))
        data = data[campaign_mask]

    tt = data.groupby([group_by_plot] + ['date']).sum()
    tt = calc_base_values(tt)
    if system_filters and system_filters[0] == "y" and len(system_filters) == 1:
        tt['impr_pos'] = tt['avg_impression_pos'] / tt['impressions']
        tt['click_pos'] = tt['avg_click_pos'] / tt['clicks']
        tt['traffic_vol'] = tt['avg_traffic_vol'] / tt['impressions']
    elif system_filters and system_filters[0] == "g" and len(system_filters) == 1:
        tt['top_is'] = tt['search_top_is'] / tt['eligible_impressions']
        tt['abstop_is'] = tt['search_abs_top_is'] / tt['eligible_impressions']

    if type(y_value) is not list:
        y_value = [y_value]

    for j in y_value:
        plotdata = pd.DataFrame({i: tt.loc[i][j] for i in plot_set})
        for i in plotdata:
            plt.plot(plotdata.index, plotdata[i], label="{} {}: {}".format(j, group_by_plot, i))

    plt.plot()

    plt.xlabel("дата")
    plt.ylabel(", ".join(y_value))
    plt.title("график сравнение")
    plt.legend()
    plt.show()
