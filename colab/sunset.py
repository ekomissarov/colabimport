import pandas as pd
import matplotlib as mpl
import matplotlib.dates as mdates
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

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
    def do_calculations(x):
        x['cost_rur'] = x['cost'] / 1000000
        x['cpc'] = np.round(x['cost_rur'] / x['clicks'], 2)
        x['cpm'] = np.round(x['cost_rur'] / (x['impressions']/1000), 2)
        x['cp_session'] = np.round(x['cost_rur'] / x['sessions'], 2)
        x['ctr'] = np.round(x['clicks'] / x['impressions'], 4)
        x['clicks_per_session'] = np.round(x['clicks'] / x['sessions'], 4)

        # конверсии объем
        print("DEBUG", x)
        x['events'] = x['total_events'] + x['total_events_app']
        x['events_ss'] = x['uniq_ss_events'] + x['uniq_ss_events_app']
        x['events_fdv'] = x['total_events_fdv'] + x['total_events_app_fdv']
        x['events_commercial'] = x['total_events_commercial'] + x['total_events_app_commercial']
        x['events_salesub'] = x['total_events_salesub'] + x['total_events_app_salesub']
        x['events_rentsub'] = x['total_events_rentsub'] + x['total_events_app_rentsub']
        x['events_saleflats'] = x['total_events_saleflats'] + x['total_events_app_saleflats']
        x['events_rentflats'] = x['total_events_rentflats'] + x['total_events_app_rentflats']
        x['events_applications'] = x['total_applications_re_events'] + x['total_applications_re_events_app']
        x['ads'] = x['total_b2bevents'] + x['total_b2bevents_app']
        x['ipotek'] = x['uniq_ipotek_events'] + x['uniq_ipotek_events_app']
        x['ct'] = x['total_ct_events'] + x['total_ct_events_app']

        # конверсии стоимости
        x['cpa'] = np.round(x['cost_rur'] / x['events'], 2)
        x['cpa_ss'] = np.round(x['cost_rur'] / x['events_ss'], 2)
        x['cpa_fdv'] = np.round(x['cost_rur'] / x['events_fdv'], 2)
        x['cpa_commercial'] = np.round(x['cost_rur'] / x['events_commercial'], 2)
        x['cpa_salesub'] = np.round(x['cost_rur'] / x['events_salesub'], 2)
        x['cpa_rentsub'] = np.round(x['cost_rur'] / x['events_rentsub'], 2)
        x['cpa_saleflats'] = np.round(x['cost_rur'] / x['events_saleflats'], 2)
        x['cpa_rentflats'] = np.round(x['cost_rur'] / x['events_rentflats'], 2)
        x['cpa_applications'] = np.round(x['cost_rur'] / x['events_applications'], 2)
        x['cpad'] = np.round(x['cost_rur'] / x['ads'], 2)
        x['cpa_ipotek'] = np.round(x['cost_rur'] / x['ipotek'], 2)
        x['cpa_ct'] = np.round(x['cost_rur'] / x['ct'], 2)

        # %конверсии на клик
        x['ev_per_click'] = np.round(x['events'] / x['clicks'], 4)
        x['ev_ss_per_click'] = np.round(x['events_ss'] / x['clicks'], 4)
        x['ev_fdv_per_click'] = np.round(x['events_fdv'] / x['clicks'], 4)
        x['ev_commercial_per_click'] = np.round(x['events_commercial'] / x['clicks'], 4)
        x['ev_salesub_per_click'] = np.round(x['events_salesub'] / x['clicks'], 4)
        x['ev_rentsub_per_click'] = np.round(x['events_rentsub'] / x['clicks'], 4)
        x['ev_saleflats_per_click'] = np.round(x['events_saleflats'] / x['clicks'], 4)
        x['ev_rentflats_per_click'] = np.round(x['events_rentflats'] / x['clicks'], 4)
        x['ev_applications_per_click'] = np.round(x['events_applications'] / x['clicks'], 4)
        x['ad_per_click'] = np.round(x['ads'] / x['clicks'], 4)
        x['ipotek_per_click'] = np.round(x['ipotek'] / x['clicks'], 4)
        x['ct_per_click'] = np.round(x['ct'] / x['clicks'], 4)

        # %ассоциированные конверсии на клик
        x['assisted_ev_per_click'] = np.round(x['assisted_conv_phones'] / x['clicks'], 4)
        x['assisted_ss_per_click'] = np.round(x['assisted_conv_ss'] / x['clicks'], 4)
        x['assisted_reappl_per_click'] = np.round(x['assisted_conv_reappl'] / x['clicks'], 4)
        x['assisted_ad_per_click'] = np.round(x['assisted_conv_ads'] / x['clicks'], 4)
        x['assisted_ipotek_per_click'] = np.round(x['assisted_conv_mortgage'] / x['clicks'], 4)
        x['assisted_ct_per_click'] = np.round(x['assisted_conv_ct'] / x['clicks'], 4)

        # агрегаты: конверсии объем
        x['conv_agg_full'] = x['events'] + (8 * x['ads']) + (500 * x['ipotek']) + (500 * x['ct']) + (8 * x['events_applications']) + (10 * x['events_ss'])
        x['conv_agg_base'] = x['events'] + (2 * x['ads']) + (5 * x['ipotek']) + (2 * x['events_applications'])
        x['conv_agg_owners'] = x['ads'] + x['events_applications'] + x['events_ss']

        # агрегаты: конверсии стоимости
        x['cp_agg_full'] = np.round(x['cost_rur'] / x['conv_agg_full'], 2)
        x['cp_agg_base'] = np.round(x['cost_rur'] / x['conv_agg_base'], 2)
        x['cp_agg_owners'] = np.round(x['cost_rur'] / x['conv_agg_owners'], 2)

        # агрегаты: %конверсии на клик
        x['agg_full_per_click'] = np.round(x['conv_agg_full'] / x['clicks'], 4)
        x['agg_base_per_click'] = np.round(x['conv_agg_base'] / x['clicks'], 4)
        x['agg_owners_per_click'] = np.round(x['conv_agg_owners'] / x['clicks'], 4)

        ##########################################
        x['cost_rur'] = x['cost_rur'].astype(np.int64)
        return x
    tt = tt.apply(do_calculations, axis=1)


def calc_base_values_with_assisted(tt):
    def do_calculations(x):
        # конверсии объем
        x['A_events'] = x['total_events'] + x['total_events_app'] + x['assisted_conv_phones']
        x['A_events_ss'] = x['uniq_ss_events'] + x['uniq_ss_events_app'] + x['assisted_conv_ss']
        x['A_events_fdv'] = x['total_events_fdv'] + x['total_events_app_fdv'] + x['assisted_conv_phones']
        x['A_events_commercial'] = x['total_events_commercial'] + x['total_events_app_commercial'] + x['assisted_conv_phones']
        x['A_events_salesub'] = x['total_events_salesub'] + x['total_events_app_salesub'] + x['assisted_conv_phones']
        x['A_events_rentsub'] = x['total_events_rentsub'] + x['total_events_app_rentsub'] + x['assisted_conv_phones']
        x['A_events_saleflats'] = x['total_events_saleflats'] + x['total_events_app_saleflats'] + x['assisted_conv_phones']
        x['A_events_rentflats'] = x['total_events_rentflats'] + x['total_events_app_rentflats'] + x['assisted_conv_phones']
        x['A_events_applications'] = x['total_applications_re_events'] + x['total_applications_re_events_app'] + x['assisted_conv_reappl']
        x['A_ads'] = x['total_b2bevents'] + x['total_b2bevents_app'] + x['assisted_conv_ads']
        x['A_ipotek'] = x['uniq_ipotek_events'] + x['uniq_ipotek_events_app'] + x['assisted_conv_mortgage']
        x['A_ct'] = x['total_ct_events'] + x['total_ct_events_app'] + x['assisted_conv_ct']

        # конверсии стоимости
        x['A_cpa'] = np.round(x['cost_rur'] / x['A_events'], 2)
        x['A_cpa_ss'] = np.round(x['cost_rur'] / x['A_events_ss'], 2)
        x['A_cpa_fdv'] = np.round(x['cost_rur'] / x['A_events_fdv'], 2)
        x['A_cpa_commercial'] = np.round(x['cost_rur'] / x['A_events_commercial'], 2)
        x['A_cpa_salesub'] = np.round(x['cost_rur'] / x['A_events_salesub'], 2)
        x['A_cpa_rentsub'] = np.round(x['cost_rur'] / x['A_events_rentsub'], 2)
        x['A_cpa_saleflats'] = np.round(x['cost_rur'] / x['A_events_saleflats'], 2)
        x['A_cpa_rentflats'] = np.round(x['cost_rur'] / x['A_events_rentflats'], 2)
        x['A_cpa_applications'] = np.round(x['cost_rur'] / x['A_events_applications'], 2)
        x['A_cpad'] = np.round(x['cost_rur'] / x['A_ads'], 2)
        x['A_cpa_ipotek'] = np.round(x['cost_rur'] / x['A_ipotek'], 2)
        x['A_cpa_ct'] = np.round(x['cost_rur'] / x['A_ct'], 2)

        # %конверсии на клик
        x['A_ev_per_click'] = np.round(x['A_events'] / x['clicks'], 4)
        x['A_ev_ss_per_click'] = np.round(x['A_events_ss'] / x['clicks'], 4)
        x['A_ev_fdv_per_click'] = np.round(x['A_events_fdv'] / x['clicks'], 4)
        x['A_ev_commercial_per_click'] = np.round(x['A_events_commercial'] / x['clicks'], 4)
        x['A_ev_salesub_per_click'] = np.round(x['A_events_salesub'] / x['clicks'], 4)
        x['A_ev_rentsub_per_click'] = np.round(x['A_events_rentsub'] / x['clicks'], 4)
        x['A_ev_saleflats_per_click'] = np.round(x['A_events_saleflats'] / x['clicks'], 4)
        x['A_ev_rentflats_per_click'] = np.round(x['A_events_rentflats'] / x['clicks'], 4)
        x['A_ev_applications_per_click'] = np.round(x['A_events_applications'] / x['clicks'], 4)
        x['A_ad_per_click'] = np.round(x['A_ads'] / x['clicks'], 4)
        x['A_ipotek_per_click'] = np.round(x['A_ipotek'] / x['clicks'], 4)
        x['A_ct_per_click'] = np.round(x['A_ct'] / x['clicks'], 4)
        x = x.copy()
        # агрегаты: конверсии объем
        x['A_conv_agg_full'] = x['A_events'] + (8 * x['A_ads']) + (500 * x['A_ipotek']) + (500 * x['A_ct']) + (8 * x['A_events_applications']) + (10 * x['A_events_ss'])
        x['A_conv_agg_base'] = x['A_events'] + (2 * x['A_ads']) + (5 * x['A_ipotek']) + (2 * x['A_events_applications'])
        x['A_conv_agg_owners'] = x['A_ads'] + x['A_events_applications'] + x['A_events_ss']

        # агрегаты: конверсии стоимости
        x['A_cp_agg_full'] = np.round(x['cost_rur'] / x['A_conv_agg_full'], 2)
        x['A_cp_agg_base'] = np.round(x['cost_rur'] / x['A_conv_agg_base'], 2)
        x['A_cp_agg_owners'] = np.round(x['cost_rur'] / x['A_conv_agg_owners'], 2)

        # агрегаты: %конверсии на клик
        x['A_agg_full_per_click'] = np.round(x['A_conv_agg_full'] / x['clicks'], 4)
        x['A_agg_base_per_click'] = np.round(x['A_conv_agg_base'] / x['clicks'], 4)
        x['A_agg_owners_per_click'] = np.round(x['A_conv_agg_owners'] / x['clicks'], 4)
        return x
    tt = tt.apply(do_calculations, axis=1)


def triad(item):
    t = [
        {"vol": "clicks", "conv": "1", "cost_per": "cpc"},
        {"vol": "events", "conv": "ev_per_click", "cost_per": "cpa"},
        {"vol": "events_ss", "conv": "ev_ss_per_click", "cost_per": "cpa_ss"},
        {"vol": "events_fdv", "conv": "ev_fdv_per_click", "cost_per": "cpa_fdv"},
        {"vol": "events_commercial", "conv": "ev_commercial_per_click", "cost_per": "cpa_commercial"},
        {"vol": "events_salesub", "conv": "ev_salesub_per_click", "cost_per": "cpa_salesub"},
        {"vol": "events_rentsub", "conv": "ev_rentsub_per_click", "cost_per": "cpa_rentsub"},
        {"vol": "events_saleflats", "conv": "ev_saleflats_per_click", "cost_per": "cpa_saleflats"},
        {"vol": "events_rentflats", "conv": "ev_applications_per_click", "cost_per": "cpa_rentflats"},
        {"vol": "events_applications", "conv": "ev_applications_per_click", "cost_per": "cpa_applications"},
        {"vol": "ads", "conv": "ad_per_click", "cost_per": "cpad"},
        {"vol": "ipotek", "conv": "ipotek_per_click", "cost_per": "cpa_ipotek"},
        {"vol": "ct", "conv": "ct_per_click", "cost_per": "cpa_ct"},

        {"vol": "assisted_conv_phones", "conv": "", "cost_per": "assisted_ev_per_click"},
        {"vol": "assisted_conv_ss", "conv": "", "cost_per": "assisted_ss_per_click"},
        {"vol": "assisted_conv_reappl", "conv": "", "cost_per": "assisted_reappl_per_click"},
        {"vol": "assisted_conv_ads", "conv": "", "cost_per": "assisted_ad_per_click"},
        {"vol": "assisted_conv_mortgage", "conv": "", "cost_per": "assisted_ipotek_per_click"},
        {"vol": "assisted_conv_ct", "conv": "", "cost_per": "assisted_ct_per_click"},

        {"vol": "conv_agg_full", "conv": "agg_full_per_click", "cost_per": "cp_agg_full"},
        {"vol": "conv_agg_base", "conv": "agg_base_per_click", "cost_per": "cp_agg_base"},
        {"vol": "conv_agg_owners", "conv": "agg_owners_per_click", "cost_per": "cp_agg_owners"},
    ]
    a_flag = ""
    if item.startswith("A_"):
        a_flag = "A_"
        item = item.replace("A_", "")

    for i in t:
        if item in set(i.values()):
            return {k[0]: f"{a_flag}{k[1]}" for k in i.items()}


class BasicDynamics:
    def __init__(self, df, what, plot_ev_per_click, vert_lines):
        self.data = df
        self.what = what
        self.plot_ev_per_click = plot_ev_per_click
        self.vert_lines = vert_lines
        if what is None:
            self.what = {"events", "events_ss", "events_fdv", "ads", "ipotek", "ct", "common",
                    "events_commercial", "events_salesub", "events_rentsub", "events_saleflats", "events_rentflats",
                    "events_applications",
                    "conv_agg_full", "conv_agg_owners",
                    "impressions"}

    def run_plot(self):
        if "events" in self.what:
            self._plt_basic_dyn(ev="events", cpa="cpa", ev_per_click="ev_per_click",
                                item_labels=["phone events", "cpa", "conv%"])
        if "events_ss" in self.what:
            self._plt_basic_dyn(ev="events_ss", cpa="cpa_ss", ev_per_click="ev_ss_per_click",
                                item_labels=["ss uniq events", "cpa_ss", "conv%"])
        if "events_fdv" in self.what:
            self._plt_basic_dyn(ev="events_fdv", cpa="cpa_fdv", ev_per_click="ev_fdv_per_click",
                                item_labels=["fdv phone events", "cpa_fdv", "conv%"])
        if "events_commercial" in self.what:
            self._plt_basic_dyn(ev="events_commercial", cpa="cpa_commercial", ev_per_click="ev_commercial_per_click",
                                item_labels=["commercial phone events", "cpa_commercial", "conv%"])
        if "events_salesub" in self.what:
            self._plt_basic_dyn(ev="events_salesub", cpa="cpa_salesub", ev_per_click="ev_salesub_per_click",
                                item_labels=["salesub phone events", "cpa_salesub", "conv%"])
        if "events_rentsub" in self.what:
            self._plt_basic_dyn(ev="events_rentsub", cpa="cpa_rentsub", ev_per_click="ev_rentsub_per_click",
                                item_labels=["rentsub phone events", "cpa_rentsub", "conv%"])
        if "events_saleflats" in self.what:
            self._plt_basic_dyn(ev="events_saleflats", cpa="cpa_saleflats", ev_per_click="ev_saleflats_per_click",
                                item_labels=["saleflats phone events", "cpa_saleflats", "conv%"])
        if "events_rentflats" in self.what:
            self._plt_basic_dyn(ev="events_rentflats", cpa="cpa_rentflats", ev_per_click="ev_rentflats_per_click",
                                item_labels=["rentflats phone events", "cpa_rentflats", "conv%"])
        if "events_applications" in self.what:
            self._plt_basic_dyn(ev="events_applications", cpa="cpa_applications", ev_per_click="ev_applications_per_click",
                                item_labels=["applications realtors events", "cpa_applications", "conv%"])
        if "ads" in self.what:
            self._plt_basic_dyn(ev="ads", cpa="cpad", ev_per_click="ad_per_click",
                           item_labels=["ads", "cpad", "conv%"])
        if "conv_agg_owners" in self.what:
            self._plt_basic_dyn(ev="conv_agg_owners", cpa="cp_agg_owners", ev_per_click="agg_owners_per_click",
                           item_labels=["ads+appl", "cpad", "conv%"])
        if "ipotek" in self.what:
            self._plt_basic_dyn(ev="ipotek", cpa="cpa_ipotek", ev_per_click="ipotek_per_click",
                           item_labels=["ipotek", "cpa_ipotek", "conv%"])
        if "ct" in self.what:
            self._plt_basic_dyn(ev="ct", cpa="cpa_ct", ev_per_click="ct_per_click",
                           item_labels=["ct", "cpa_ct", "conv%"])
        if "conv_agg_full" in self.what:
            self._plt_basic_dyn(ev="conv_agg_full", cpa="cp_agg_full", ev_per_click="agg_full_per_click",
                           item_labels=["aggregate", "cpa", "conv%"])

        if "impressions" in self.what:
            self._plt_basic_dyn(ev="impressions", cpa="cpm", ev_per_click="ctr",
                           item_labels=["impressions", "cpm", "ctr"])

        if "common" in self.what:
            cost_rur = self.data.loc[:, "cost_rur"]
            cpc = self.data.loc[:, "cpc"]
            ctr = self.data.loc[:, "ctr"]
            clicks = self.data.loc[:, "clicks"]
            rolling_cost_rur = cost_rur.rolling(7, center=True)
            rolling_cpc = cpc.rolling(7, center=True)
            rolling_ctr = ctr.rolling(7, center=True)
            rolling_clicks = clicks.rolling(7, center=True)
            cost_rur = pd.DataFrame({'values': cost_rur, 'rolling_mean': rolling_cost_rur.mean(), 'rolling_std': rolling_cost_rur.std()})
            cpc = pd.DataFrame({'values': cpc, 'rolling_mean': rolling_cpc.mean(), 'rolling_std': rolling_cpc.std()})
            ctr = pd.DataFrame({'values': ctr, 'rolling_mean': rolling_ctr.mean(), 'rolling_std': rolling_ctr.std()})
            clicks = pd.DataFrame({'values': clicks, 'rolling_mean': rolling_clicks.mean(), 'rolling_std': rolling_clicks.std()})
            self.plot_basic_rolling(cost_rur, cpc, ctr, clicks,
                                    items=["cost_rur", "cpc", "ctr", "clicks"],
                                    line_colors=["darkblue", "orange", "green", "red"])

    def _plt_basic_dyn(self, ev, cpa, ev_per_click, item_labels):
        events = self.data.loc[:, ev]
        cpas = self.data.loc[:, cpa]
        rolling_ev = events.rolling(7, center=True)
        rolling_cpas = cpas.rolling(7, center=True)
        events = pd.DataFrame({'values': events, 'rolling_mean': rolling_ev.mean(), 'rolling_std': rolling_ev.std()})
        cpas = pd.DataFrame({'values': cpas, 'rolling_mean': rolling_cpas.mean(), 'rolling_std': rolling_cpas.std()})
        if np.isinf(cpas.iloc[0]['values']):
            cpas.iloc[0]['values'] = 0
        if self.plot_ev_per_click:
            ev_per_click = self.data.loc[:, ev_per_click]
            rolling_convsperclick = ev_per_click.rolling(7, center=True)
            ev_per_click = pd.DataFrame({'values': ev_per_click, 'rolling_mean': rolling_convsperclick.mean(),
                                         'rolling_std': rolling_convsperclick.std()})
            self.plot_basic_rolling(events, cpas, ev_per_click, items=item_labels,
                                    line_colors=["darkblue", "orange", "darkgreen"])
        else:
            self.plot_basic_rolling(events, cpas, items=item_labels[:-1],
                                    line_colors=["darkblue", "orange"])

    def plot_basic_rolling(self, *lines, items=["events", "cpa"], line_colors=["darkblue", "orange"]):
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
            if self.vert_lines:
                for j in self.vert_lines:
                    axN[i].axvline(x=j, color='gray')

        locator = mdates.AutoDateLocator(minticks=5, maxticks=20)
        formatter = mdates.ConciseDateFormatter(locator)
        axN[i].xaxis.set_major_locator(locator)
        axN[i].xaxis.set_major_formatter(formatter)
        plt.show()


def plot_basic_dynamics(df, what=None,
                        region_filters=None, campaign_filters=None, system_filters=None,
                        plot_ev_per_click = False, vert_lines=None):
    tt = df.copy()
    if region_filters:
        tt = tt[tt.region.isin(region_filters)]

    if system_filters:
        tt = tt[tt.system.isin(system_filters)]

    if campaign_filters:
        campaign_mask = pd.Series(False, index=tt.index)
        for i in campaign_filters:
            campaign_mask = campaign_mask | (tt.campaignname.str.contains(i))
        tt = tt[campaign_mask]

    tt = tt.groupby(['date']).sum()
    tt = calc_base_values(tt)
    tt.index = pd.to_datetime(tt.index)
    basicdyn = BasicDynamics(tt, what, plot_ev_per_click, vert_lines)
    basicdyn.run_plot()

def plot_avg_position_yandex(df, region_filters=None, campaign_filters=None, vert_lines=None):
    grp = ['date']
    df = df[(df.system == "y") & (df.campaignname.str.contains("_search"))]

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

    plots = ["impr_pos", "click_pos", "traffic_vol"]
    ax = tt.loc[:, plots].plot(subplots=True)
    if vert_lines:
        for i in ax:
            for j in vert_lines:
                i.axvline(x=j, color='gray')
    plt.show()


def plot_top_is_position_google(df, region_filters=None, campaign_filters=None, vert_lines=None):
    grp = ['date']
    df = df[(df.system == "g") & (df.campaignname.str.contains("_search"))]

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

    plots = ["top_is", "abstop_is"]
    ax = tt.loc[:, plots].plot(subplots=True)
    if vert_lines:
        for i in ax:
            for j in vert_lines:
                i.axvline(x=j, color='gray')
    plt.show()


def plot_compare_base(data, y_value, group_by_plot, plot_set,
                      region_filters=None, campaign_filters=None, system_filters=None,
                      ymax=None, vert_lines=None):

    if type(y_value) is not list:
        y_value = [y_value]

    if {'impr_pos', 'click_pos', 'traffic_vol', 'top_is', 'abstop_is'} & set(y_value):
        data = data[data.campaignname.str.contains("_search")]

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
    tt = calc_base_values_with_assisted(tt)
    if system_filters and system_filters[0] == "y" and len(system_filters) == 1:
        tt['impr_pos'] = tt['avg_impression_pos'] / tt['impressions']
        tt['click_pos'] = tt['avg_click_pos'] / tt['clicks']
        tt['traffic_vol'] = tt['avg_traffic_vol'] / tt['impressions']
    elif system_filters and system_filters[0] == "g" and len(system_filters) == 1:
        tt['top_is'] = tt['search_top_is'] / tt['eligible_impressions']
        tt['abstop_is'] = tt['search_abs_top_is'] / tt['eligible_impressions']

    for j in y_value:
        plotdata = pd.DataFrame({i: tt.loc[i][j] for i in plot_set})
        for i in plotdata:
            plt.plot(plotdata.index, plotdata[i], label="{} {}: {}".format(j, group_by_plot, i))

    if ymax is not None:
        #plt.xlim(right=xmax)  # xmax is your value
        #plt.xlim(left=xmin)  # xmin is your value
        plt.ylim(top=ymax[1])  # ymax is your value
        plt.ylim(bottom=ymax[0])  # ymin is your value
    if vert_lines:
        for i in vert_lines:
            plt.axvline(x=i, color='gray')

    plt.plot()

    plt.xlabel("дата")
    plt.ylabel(", ".join(y_value))
    plt.title("график сравнение")
    plt.legend()
    plt.show()


def resample_df(df, dimension="campaignname", resample_period="M"):
    df['date'] = pd.to_datetime(df['date'])
    result = pd.DataFrame()
    for i in df[dimension].unique():
        tmp = df[df[dimension] == i].copy()
        tmp = tmp.groupby(['date']).sum()
        tmp = tmp.resample(resample_period).sum().reset_index()
        tmp[dimension] = i
        result = pd.concat([result, tmp])

    result = calc_base_values(result)
    result = calc_base_values_with_assisted(result)
    return result

def cell_dimension(df, metrics, dimension = 'vertical_class', exclude_graphs = None, vert_lines=None):
    """
    metrics example: ["cpa", "events"]
    exclude_graphs example: {"cpa": {"ipoteka", "Undefined"}
    """
    if vert_lines is None:
        vert_lines = [date(*date.today().timetuple()[0:2], 1)]
    df.loc[df[dimension]==False, dimension] = "Undefined"
    for i in metrics:
        plot_set_excl = set()
        if exclude_graphs and i in exclude_graphs:
            plot_set_excl = exclude_graphs[i]
        plot_compare_base(df,
            y_value = i,
            group_by_plot = dimension,
            plot_set = set(df[dimension].unique()) - plot_set_excl,
            vert_lines=vert_lines)