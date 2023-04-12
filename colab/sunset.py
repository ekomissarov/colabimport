import pandas as pd
import matplotlib as mpl
import matplotlib.dates as mdates
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import date

def scale_plot_size(x, y):
    #default_figsize = mpl.rcParamsDefault['figure.figsize']
    mpl.rcParams['figure.figsize'] = [x, y]


def concat_empty_columns(tt, cols):
    diff = set(cols) - set(tt.columns)
    if diff:
        new = pd.DataFrame(columns=list(diff))
        tt = pd.concat([tt, new], axis=1)
    return tt


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
        df = concat_empty_columns(df, ["eligible_impressions"])
        df["eligible_impressions"] = np.round(df["impressions"]/(df['search_impression_share'] / 100), 4)
        df["search_abs_top_is"] = np.round(df["search_abs_top_is"] * df["eligible_impressions"] / 100, 4)
        df["search_top_is"] = np.round(df["search_top_is"] * df["eligible_impressions"] / 100, 4)

    if 'impr_top_percent' in df.columns:
        df = concat_empty_columns(df, ["impr_top_percent",])
        df["impr_top_percent"] = np.round(df["impr_top_percent"] * df["impressions"] / 100, 4)
    if 'impr_abs_top_percent' in df.columns:
        df = concat_empty_columns(df, ["impr_abs_top_percent",])
        df["impr_abs_top_percent"] = np.round(df["impr_abs_top_percent"] * df["impressions"] / 100, 4)

    # https://yandex.ru/dev/direct/doc/reports/report-format-docpage/
    df['avg_impression_pos'] = np.round(df['avg_impression_pos'] * df["impressions"], 4)
    df['avg_traffic_vol'] = np.round(df['avg_traffic_vol'] * df["impressions"], 4)
    df['avg_click_pos'] = np.round(df['avg_click_pos'] * df["clicks"], 4)
    return df


def calc_base_values(tt):
    tt = concat_empty_columns(tt, [
        'cost_rur', 'cpc', 'cpm', 'cp_session', 'ctr', 'clicks_per_session',
        'events', 'chats', 'events_ss', 'events_fdv', 'events_commercial', 'events_salesub', 'events_rentsub',
        'events_saleflats', 'events_rentflats', 'events_applications', 'ads', 'ipotek', 'ct',

        'cpa', 'cp_chat', 'cpa_ss', 'cpa_fdv', 'cpa_commercial', 'cpa_salesub', 'cpa_rentsub',
        'cpa_saleflats', 'cpa_rentflats', 'cpa_applications', 'cpad', 'cpa_ipotek', 'cpa_ct',

        'ev_per_click', 'chats_per_click', 'ev_ss_per_click', 'ev_fdv_per_click', 'ev_commercial_per_click', 'ev_salesub_per_click',
        'ev_rentsub_per_click',
        'ev_saleflats_per_click', 'ev_rentflats_per_click', 'ev_applications_per_click', 'ad_per_click',
        'ipotek_per_click', 'ct_per_click',

        'assisted_ev_per_click', 'assisted_ss_per_click', 'assisted_reappl_per_click', 'assisted_ad_per_click',
        'assisted_ipotek_per_click', 'assisted_ct_per_click',

        'conv_agg_full', 'ev_contacts', 'conv_agg_owners', 'cp_agg_full', 'cp_contact', 'cp_agg_owners',
        'agg_full_per_click', 'contacts_per_click', 'agg_owners_per_click'
    ])

    tt['cost_rur'] = tt['cost'] / 1000000
    tt['cpc'] = np.round(tt['cost_rur'] / tt['clicks'], 2)
    tt['cpm'] = np.round(tt['cost_rur'] / (tt['impressions']/1000), 2)
    tt['cp_session'] = np.round(tt['cost_rur'] / tt['sessions'], 2)
    tt['ctr'] = np.round(tt['clicks'] / tt['impressions'], 4)
    tt['clicks_per_session'] = np.round(tt['clicks'] / tt['sessions'], 4)

    # конверсии объем
    tt['events'] = tt['total_events'] + tt['total_events_app']
    tt['chats'] = tt['total_chats'] + tt['total_chats_app']
    tt['events_ss'] = tt['uniq_ss_events'] + tt['uniq_ss_events_app']
    tt['events_fdv'] = tt['total_events_fdv'] + tt['total_events_app_fdv']
    tt['events_commercial'] = tt['total_events_commercial'] + tt['total_events_app_commercial']
    tt['events_salesub'] = tt['total_events_salesub'] + tt['total_events_app_salesub']
    tt['events_rentsub'] = tt['total_events_rentsub'] + tt['total_events_app_rentsub']

    tt['events_saleflats'] = tt['total_events_saleflats'] + tt['total_events_app_saleflats']
    tt['events_rentflats'] = tt['total_events_rentflats'] + tt['total_events_app_rentflats']
    tt['events_applications'] = tt['total_applications_re_events'] + tt['total_applications_re_events_app']
    tt['ads'] = tt['total_b2bevents'] + tt['total_b2bevents_app']
    tt['ipotek'] = tt['uniq_ipotek_events'] + tt['uniq_ipotek_events_app']
    tt['ct'] = tt['total_ct_events'] + tt['total_ct_events_app']

    # конверсии стоимости
    tt['cpa'] = np.round(tt['cost_rur'] / tt['events'], 2)
    tt['cp_chat'] = np.round(tt['cost_rur'] / tt['chats'], 2)
    tt['cpa_ss'] = np.round(tt['cost_rur'] / tt['events_ss'], 2)
    tt['cpa_fdv'] = np.round(tt['cost_rur'] / tt['events_fdv'], 2)
    tt['cpa_commercial'] = np.round(tt['cost_rur'] / tt['events_commercial'], 2)
    tt['cpa_salesub'] = np.round(tt['cost_rur'] / tt['events_salesub'], 2)
    tt['cpa_rentsub'] = np.round(tt['cost_rur'] / tt['events_rentsub'], 2)

    tt['cpa_saleflats'] = np.round(tt['cost_rur'] / tt['events_saleflats'], 2)
    tt['cpa_rentflats'] = np.round(tt['cost_rur'] / tt['events_rentflats'], 2)
    tt['cpa_applications'] = np.round(tt['cost_rur'] / tt['events_applications'], 2)
    tt['cpad'] = np.round(tt['cost_rur'] / tt['ads'], 2)
    tt['cpa_ipotek'] = np.round(tt['cost_rur'] / tt['ipotek'], 2)
    tt['cpa_ct'] = np.round(tt['cost_rur'] / tt['ct'], 2)

    # %конверсии на клик
    tt['ev_per_click'] = np.round(tt['events'] / tt['clicks'], 4)
    tt['chats_per_click'] = np.round(tt['chats'] / tt['clicks'], 4)
    tt['ev_ss_per_click'] = np.round(tt['events_ss'] / tt['clicks'], 4)
    tt['ev_fdv_per_click'] = np.round(tt['events_fdv'] / tt['clicks'], 4)
    tt['ev_commercial_per_click'] = np.round(tt['events_commercial'] / tt['clicks'], 4)
    tt['ev_salesub_per_click'] = np.round(tt['events_salesub'] / tt['clicks'], 4)
    tt['ev_rentsub_per_click'] = np.round(tt['events_rentsub'] / tt['clicks'], 4)

    tt['ev_saleflats_per_click'] = np.round(tt['events_saleflats'] / tt['clicks'], 4)
    tt['ev_rentflats_per_click'] = np.round(tt['events_rentflats'] / tt['clicks'], 4)
    tt['ev_applications_per_click'] = np.round(tt['events_applications'] / tt['clicks'], 4)
    tt['ad_per_click'] = np.round(tt['ads'] / tt['clicks'], 4)
    tt['ipotek_per_click'] = np.round(tt['ipotek'] / tt['clicks'], 4)
    tt['ct_per_click'] = np.round(tt['ct'] / tt['clicks'], 4)

    # %ассоциированные конверсии на клик
    tt['assisted_ev_per_click'] = np.round(tt['assisted_conv_phones'] / tt['clicks'], 4)
    tt['assisted_ss_per_click'] = np.round(tt['assisted_conv_ss'] / tt['clicks'], 4)
    tt['assisted_reappl_per_click'] = np.round(tt['assisted_conv_reappl'] / tt['clicks'], 4)
    tt['assisted_ad_per_click'] = np.round(tt['assisted_conv_ads'] / tt['clicks'], 4)
    tt['assisted_ipotek_per_click'] = np.round(tt['assisted_conv_mortgage'] / tt['clicks'], 4)
    tt['assisted_ct_per_click'] = np.round(tt['assisted_conv_ct'] / tt['clicks'], 4)

    # агрегаты: конверсии объем
    tt['conv_agg_full'] = tt['events'] + (8 * tt['ads']) + (500 * tt['ipotek']) + (500 * tt['ct']) + (8 * tt['events_applications']) + (10 * tt['events_ss'])
    tt['ev_contacts'] = tt['events'] + tt['chats']
    tt['conv_agg_owners'] = tt['ads'] + tt['events_applications'] + tt['events_ss']

    # агрегаты: конверсии стоимости
    tt['cp_agg_full'] = np.round(tt['cost_rur'] / tt['conv_agg_full'], 2)
    tt['cp_contact'] = np.round(tt['cost_rur'] / tt['ev_contacts'], 2)
    tt['cp_agg_owners'] = np.round(tt['cost_rur'] / tt['conv_agg_owners'], 2)

    # агрегаты: %конверсии на клик
    tt['agg_full_per_click'] = np.round(tt['conv_agg_full'] / tt['clicks'], 4)
    tt['contacts_per_click'] = np.round(tt['ev_contacts'] / tt['clicks'], 4)
    tt['agg_owners_per_click'] = np.round(tt['conv_agg_owners'] / tt['clicks'], 4)

    ##########################################
    tt['cost_rur'] = tt['cost_rur'].astype(np.int64)
    return tt.copy()


def calc_base_values_with_assisted(tt):
    tt = concat_empty_columns(tt, [
        'A_events', 'A_events_ss', 'A_events_fdv', 'A_events_commercial', 'A_events_salesub', 'A_events_rentsub',
        'A_events_saleflats', 'A_events_rentflats', 'A_events_applications', 'A_ads', 'A_ipotek', 'A_ct',

        'A_cpa', 'A_cpa_ss', 'A_cpa_fdv', 'A_cpa_commercial', 'A_cpa_salesub', 'A_cpa_rentsub',
        'A_cpa_saleflats', 'A_cpa_rentflats', 'A_cpa_applications', 'A_cpad', 'A_cpa_ipotek', 'A_cpa_ct',

        'A_ev_per_click', 'A_ev_ss_per_click', 'A_ev_fdv_per_click', 'A_ev_commercial_per_click', 'A_ev_salesub_per_click',
        'A_ev_rentsub_per_click',
        'A_ev_saleflats_per_click', 'A_ev_rentflats_per_click', 'A_ev_applications_per_click', 'A_ad_per_click',
        'A_ipotek_per_click', 'A_ct_per_click',

        'A_conv_agg_full', 'A_ev_contacts', 'A_conv_agg_owners', 'A_cp_agg_full', 'A_cp_contact', 'A_cp_agg_owners',
        'A_agg_full_per_click', 'contacts_per_click', 'A_agg_owners_per_click'
    ])

    # конверсии объем
    tt['A_events'] = tt['total_events'] + tt['total_events_app'] + tt['assisted_conv_phones']
    tt['A_events_ss'] = tt['uniq_ss_events'] + tt['uniq_ss_events_app'] + tt['assisted_conv_ss']
    tt['A_events_fdv'] = tt['total_events_fdv'] + tt['total_events_app_fdv'] + tt['assisted_conv_phones']
    tt['A_events_commercial'] = tt['total_events_commercial'] + tt['total_events_app_commercial'] + tt['assisted_conv_phones']
    tt['A_events_salesub'] = tt['total_events_salesub'] + tt['total_events_app_salesub'] + tt['assisted_conv_phones']
    tt['A_events_rentsub'] = tt['total_events_rentsub'] + tt['total_events_app_rentsub'] + tt['assisted_conv_phones']

    tt['A_events_saleflats'] = tt['total_events_saleflats'] + tt['total_events_app_saleflats'] + tt['assisted_conv_phones']
    tt['A_events_rentflats'] = tt['total_events_rentflats'] + tt['total_events_app_rentflats'] + tt['assisted_conv_phones']
    tt['A_events_applications'] = tt['total_applications_re_events'] + tt['total_applications_re_events_app'] + tt['assisted_conv_reappl']
    tt['A_ads'] = tt['total_b2bevents'] + tt['total_b2bevents_app'] + tt['assisted_conv_ads']
    tt['A_ipotek'] = tt['uniq_ipotek_events'] + tt['uniq_ipotek_events_app'] + tt['assisted_conv_mortgage']
    tt['A_ct'] = tt['total_ct_events'] + tt['total_ct_events_app'] + tt['assisted_conv_ct']

    # конверсии стоимости
    tt['A_cpa'] = np.round(tt['cost_rur'] / tt['A_events'], 2)
    tt['A_cpa_ss'] = np.round(tt['cost_rur'] / tt['A_events_ss'], 2)
    tt['A_cpa_fdv'] = np.round(tt['cost_rur'] / tt['A_events_fdv'], 2)
    tt['A_cpa_commercial'] = np.round(tt['cost_rur'] / tt['A_events_commercial'], 2)
    tt['A_cpa_salesub'] = np.round(tt['cost_rur'] / tt['A_events_salesub'], 2)
    tt['A_cpa_rentsub'] = np.round(tt['cost_rur'] / tt['A_events_rentsub'], 2)

    tt['A_cpa_saleflats'] = np.round(tt['cost_rur'] / tt['A_events_saleflats'], 2)
    tt['A_cpa_rentflats'] = np.round(tt['cost_rur'] / tt['A_events_rentflats'], 2)
    tt['A_cpa_applications'] = np.round(tt['cost_rur'] / tt['A_events_applications'], 2)
    tt['A_cpad'] = np.round(tt['cost_rur'] / tt['A_ads'], 2)
    tt['A_cpa_ipotek'] = np.round(tt['cost_rur'] / tt['A_ipotek'], 2)
    tt['A_cpa_ct'] = np.round(tt['cost_rur'] / tt['A_ct'], 2)

    # %конверсии на клик
    tt['A_ev_per_click'] = np.round(tt['A_events'] / tt['clicks'], 4)
    tt['A_ev_ss_per_click'] = np.round(tt['A_events_ss'] / tt['clicks'], 4)
    tt['A_ev_fdv_per_click'] = np.round(tt['A_events_fdv'] / tt['clicks'], 4)
    tt['A_ev_commercial_per_click'] = np.round(tt['A_events_commercial'] / tt['clicks'], 4)
    tt['A_ev_salesub_per_click'] = np.round(tt['A_events_salesub'] / tt['clicks'], 4)
    tt['A_ev_rentsub_per_click'] = np.round(tt['A_events_rentsub'] / tt['clicks'], 4)

    tt['A_ev_saleflats_per_click'] = np.round(tt['A_events_saleflats'] / tt['clicks'], 4)
    tt['A_ev_rentflats_per_click'] = np.round(tt['A_events_rentflats'] / tt['clicks'], 4)
    tt['A_ev_applications_per_click'] = np.round(tt['A_events_applications'] / tt['clicks'], 4)
    tt['A_ad_per_click'] = np.round(tt['A_ads'] / tt['clicks'], 4)
    tt['A_ipotek_per_click'] = np.round(tt['A_ipotek'] / tt['clicks'], 4)
    tt['A_ct_per_click'] = np.round(tt['A_ct'] / tt['clicks'], 4)

    # агрегаты: конверсии объем
    tt['A_conv_agg_full'] = tt['A_events'] + (8 * tt['A_ads']) + (500 * tt['A_ipotek']) + (500 * tt['A_ct']) + (8 * tt['A_events_applications']) + (10 * tt['A_events_ss'])
    tt['A_ev_contacts'] = tt['A_events'] + tt['chats']  # chats have no assisted convs now
    tt['A_conv_agg_owners'] = tt['A_ads'] + tt['A_events_applications'] + tt['A_events_ss']

    # агрегаты: конверсии стоимости
    tt['A_cp_agg_full'] = np.round(tt['cost_rur'] / tt['A_conv_agg_full'], 2)
    tt['A_cp_contact'] = np.round(tt['cost_rur'] / tt['A_ev_contacts'], 2)
    tt['A_cp_agg_owners'] = np.round(tt['cost_rur'] / tt['A_conv_agg_owners'], 2)

    # агрегаты: %конверсии на клик
    tt['A_agg_full_per_click'] = np.round(tt['A_conv_agg_full'] / tt['clicks'], 4)
    tt['A_contacts_per_click'] = np.round(tt['A_ev_contacts'] / tt['clicks'], 4)
    tt['A_agg_owners_per_click'] = np.round(tt['A_conv_agg_owners'] / tt['clicks'], 4)

    return tt.copy()


def triad(item):
    t = [
        {"vol": "clicks", "conv": "1", "cost_per": "cpc"},
        {"vol": "events", "conv": "ev_per_click", "cost_per": "cpa"},
        {"vol": "ev_contacts", "conv": "contacts_per_click", "cost_per": "cp_contact"},
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
        {"vol": "ev_contacts", "conv": "contacts_per_click", "cost_per": "cp_contact"},
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
    plotly_use = False
    def __init__(self, df, what, plot_ev_per_click, vert_lines):
        self.data = df
        self.what = what
        self.plot_ev_per_click = plot_ev_per_click
        self.vert_lines = vert_lines
        if what is None:
            self.what = {"events", "chats", "contacts", "events_ss", "events_fdv", "ads", "ipotek", "ct", "common",
                    "events_commercial", "events_salesub", "events_rentsub", "events_saleflats", "events_rentflats",
                    "events_applications",
                    "conv_agg_full", "conv_agg_owners",
                    "impressions"}

    def run_plot(self):
        if "events" in self.what:
            self._plt_basic_dyn(ev="events", cpa="cpa", ev_per_click="ev_per_click",
                                item_labels=["phone events", "cpa", "conv%"])
        if "chats" in self.what:
            self._plt_basic_dyn(ev="chats", cpa="cp_chat", ev_per_click="chats_per_click",
                                item_labels=["chats", "cpa", "conv%"])
        if "contacts" in self.what:
            self._plt_basic_dyn(ev="ev_contacts", cpa="cp_contact", ev_per_click="contacts_per_click",
                                item_labels=["contacts", "cpa", "conv%"])
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
            if self.plotly_use:
                self.plot_plotly_rolling(cost_rur, cpc, ctr, clicks,
                                        items=["cost_rur", "cpc", "ctr", "clicks"],
                                        line_colors=["darkblue", "orange", "green", "red"])
            else:
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
            if self.plotly_use:
                self.plot_plotly_rolling(events, cpas, ev_per_click, items=item_labels,
                                        line_colors=["darkblue", "orange", "darkgreen"])
            else:
                self.plot_basic_rolling(events, cpas, ev_per_click, items=item_labels,
                                        line_colors=["darkblue", "orange", "darkgreen"])
        else:
            if self.plotly_use:
                self.plot_plotly_rolling(events, cpas, items=item_labels[:-1],
                                        line_colors=["darkblue", "orange"])
            else:
                self.plot_basic_rolling(events, cpas, items=item_labels[:-1],
                                        line_colors=["darkblue", "orange"])

    def plot_basic_rolling(self, *lines, items=["events", "cpa"], line_colors=["darkblue", "orange"]):
        fig, axN = plt.subplots(len(lines), 1)

        for i, line in enumerate(lines):
            axN[i].plot(line.index, line['values'].to_numpy(), '-', color=line_colors[i])
            axN[i].plot(line.index, line['rolling_mean'].to_numpy(), '--', color='gray')
            axN[i].plot(line.index, line['rolling_std'].to_numpy(), ':', color='gray')
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

    def plot_plotly_rolling(self, *lines, items=["events", "cpa"], line_colors=["darkblue", "orange"]):
        fig = make_subplots(rows=len(lines), cols=1,
                            shared_xaxes=True, vertical_spacing=0.02,
                            subplot_titles=items)

        for i, line in enumerate(lines):

            fig.add_trace(
                go.Scatter(x=line.index, y=line['values'], mode='lines', line=dict(color=line_colors[i]),
                           name=items[i], opacity=1),
                row=i+1, col=1)
            fig.add_trace(
                go.Scatter(x=line.index, y=line['rolling_mean'], mode='lines', line=dict(color='gray', dash='dash'),
                           name='rolling_mean', opacity=0.5),
                row=i+1, col=1)
            # fig.add_trace(
            #     go.Scatter(x=line.index, y=line['rolling_std'], mode='lines', line=dict(color='gray', dash='dash'),
            #                name='rolling_std', opacity=0.5),
            #     row=i+1, col=1)


            if self.vert_lines:
                for j in self.vert_lines:
                    fig.add_vline(x=j, line_width=1, line_dash="longdash", line_color="darkgreen",)

        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=200*len(lines), width=1080, showlegend=False, ) #title_text="specs examples"
        fig.show()


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

    tt = tt.groupby('date').sum()
    tt = calc_base_values(tt)
    tt.index = pd.to_datetime(tt.index)
    basicdyn = BasicDynamics(tt, what, plot_ev_per_click, vert_lines)
    basicdyn.run_plot()

def plotly_avg_position_yandex(df, region_filters=None, campaign_filters=None, vert_lines=None):
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

    tt = concat_empty_columns(tt, ["impr_pos", "click_pos", "traffic_vol"])
    tt['impr_pos'] = tt['avg_impression_pos'] / tt['impressions']
    tt['click_pos'] = tt['avg_click_pos'] / tt['clicks']
    tt['traffic_vol'] = tt['avg_traffic_vol'] / tt['impressions']

    plots = ["impr_pos", "click_pos", "traffic_vol"]
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02, subplot_titles=plots)
    fig.add_trace(
        go.Scatter(x=tt.index, y=tt["impr_pos"], mode="lines", line=dict(color="darkblue"), name="impr_pos", opacity=1),
        row=1, col=1)
    fig.add_trace(
        go.Scatter(x=tt.index, y=tt["click_pos"], mode="lines", line=dict(color="orange"), name="click_pos", opacity=1),
        row=2, col=1)
    fig.add_trace(
        go.Scatter(x=tt.index, y=tt["traffic_vol"], mode="lines", line=dict(color="green"), name="traffic_vol", opacity=1),
        row=3, col=1)
    if vert_lines:
        for j in vert_lines:
            fig.add_vline(x=j, line_width=1, line_dash="longdash", line_color="darkgreen", )

    fig.update_xaxes(tickangle=45)
    fig.update_layout(height=200 * len(plots), width=1080, showlegend=False, )  # title_text="specs examples"
    fig.show()


def plotly_top_is_position_google(df, region_filters=None, campaign_filters=None, vert_lines=None):
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

    tt = concat_empty_columns(tt, ["top_is", "abstop_is", ])
    tt['top_is'] = tt['search_top_is'] / tt['eligible_impressions']
    tt['abstop_is'] = tt['search_abs_top_is'] / tt['eligible_impressions']

    plots = ["top_is", "abstop_is"]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, subplot_titles=plots)
    fig.add_trace(
        go.Scatter(x=tt.index, y=tt["top_is"], mode="lines", line=dict(color="darkblue"), name="top_is", opacity=1),
        row=1, col=1)
    fig.add_trace(
        go.Scatter(x=tt.index, y=tt["abstop_is"], mode="lines", line=dict(color="orange"), name="abstop_is", opacity=1),
        row=2, col=1)
    if vert_lines:
        for j in vert_lines:
            fig.add_vline(x=j, line_width=1, line_dash="longdash", line_color="darkgreen", )

    fig.update_xaxes(tickangle=45)
    fig.update_layout(height=200 * len(plots), width=1080, showlegend=False, )  # title_text="specs examples"
    fig.show()

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

    tt = concat_empty_columns(tt, ["impr_pos", "click_pos", "traffic_vol"])
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

    tt = concat_empty_columns(tt, ["top_is", "abstop_is", ])
    tt['top_is'] = tt['search_top_is'] / tt['eligible_impressions']
    tt['abstop_is'] = tt['search_abs_top_is'] / tt['eligible_impressions']

    plots = ["top_is", "abstop_is"]
    ax = tt.loc[:, plots].plot(subplots=True)
    if vert_lines:
        for i in ax:
            for j in vert_lines:
                i.axvline(x=j, color='gray')
    plt.show()


def plotly_compare_base(data, y_value, group_by_plot, plot_set,
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
        tt = concat_empty_columns(tt, ["impr_pos", "click_pos", "traffic_vol"])
        tt['impr_pos'] = tt['avg_impression_pos'] / tt['impressions']
        tt['click_pos'] = tt['avg_click_pos'] / tt['clicks']
        tt['traffic_vol'] = tt['avg_traffic_vol'] / tt['impressions']
    elif system_filters and system_filters[0] == "g" and len(system_filters) == 1:
        tt = concat_empty_columns(tt, ["top_is", "abstop_is", ])
        tt['top_is'] = tt['search_top_is'] / tt['eligible_impressions']
        tt['abstop_is'] = tt['search_abs_top_is'] / tt['eligible_impressions']

    for j in y_value:
        plotdata = pd.DataFrame({i: tt.loc[i][j] for i in plot_set})
        fig = px.line(plotdata, x=plotdata.index, y=list(plot_set), title=f'Сравнение {j}')
        if vert_lines:
            for i in vert_lines:
                fig.add_vline(x=j, line_width=1, line_dash="longdash", line_color="darkgreen", )
        fig.update_xaxes(tickangle=45)  # повернём подписи по оси X на 45 градусов
        fig.show()


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
        tt = concat_empty_columns(tt, ["impr_pos", "click_pos", "traffic_vol"])
        tt['impr_pos'] = tt['avg_impression_pos'] / tt['impressions']
        tt['click_pos'] = tt['avg_click_pos'] / tt['clicks']
        tt['traffic_vol'] = tt['avg_traffic_vol'] / tt['impressions']
    elif system_filters and system_filters[0] == "g" and len(system_filters) == 1:
        tt = concat_empty_columns(tt, ["top_is", "abstop_is", ])
        tt['top_is'] = tt['search_top_is'] / tt['eligible_impressions']
        tt['abstop_is'] = tt['search_abs_top_is'] / tt['eligible_impressions']

    for j in y_value:
        plotdata = pd.DataFrame({i: tt.loc[i][j] for i in plot_set})
        for i in plotdata:
            plotdata[i].plot(label="{} {}: {}".format(j, group_by_plot, i))

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
    for labels, data in df.groupby(dimension):
        data = data.groupby('date').sum().resample(resample_period).sum().reset_index()
        if type(labels) is not tuple:
            labels = [labels, ]
        if type(dimension) is not list:
            dimension = [dimension, ]
        for col, lbl in zip(dimension, labels):
            data[col] = lbl
        result = pd.concat([result, data])

    result = result.reset_index(drop=True)
    result = calc_base_values(result)
    result = calc_base_values_with_assisted(result)
    return result


def cell_plotly_dimension(df, metrics, dimension = 'vertical_class', exclude_graphs = None, vert_lines=None):
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
        plotly_compare_base(df,
            y_value = i,
            group_by_plot = dimension,
            plot_set = set(df[dimension].unique()) - plot_set_excl,
            vert_lines=vert_lines)

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