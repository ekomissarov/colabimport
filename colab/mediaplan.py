import re
import pandas as pd


def concat_empty_columns(tt, cols):
    diff = set(cols) - set(tt.columns)
    if diff:
        new = pd.DataFrame(columns=list(diff))
        tt = pd.concat([tt, new], axis=1)
    return tt


class MP:
    filter_column = "campaignname"
    classificator_column_name = "budget_class"
    tags = [
        ######################################################################################
        # Пакет: test ########################################################################
        ######################################################################################
        #{"descr": 'test_bdg', "fltrs": ["_mobapptest_", "_test_"]},
        # {"descr": 'special_project_bdg', "fltrs": ["_specproj"]},
        # {"descr": 'testa_yndxbeta_bdg', "fltrs": ["_yndxbeta1"]},
        # {"descr": 'testb_yndxbeta_bdg', "fltrs": ["_yndxbeta2"]},
        # {"descr": 'test_group_bdg', "fltrs": ["_testgrp"]},
        # {"descr": 'media_banner_bdg', "fltrs": ["_media_", "_banner_"]},

        {"descr": 'all_other_realweb_bdg', "fltrs": ["_search_rw", "_network_rw" ]},
        {"descr": 'all_dailyrent_bdg', "fltrs": ["daily", ]},
        {"descr": 'rf_multiapp_mkb_network_bdg', "fltrs": ["_mkb_.*multiapp", ]},
        {"descr": 'rf_multiapp_network_bdg', "fltrs": ["_multiapp", ]},

        ######################################################################################
        # Пакет: brand_cian ##################################################################
        ######################################################################################
        {"descr": 'msk_brand_cian_bdg', "fltrs": ["b2c_(dmo|bmo|mo|msk)_brand_cian_all_mix_search", ]},
        {"descr": 'spb_brand_cian_bdg', "fltrs": ["b2c_spb_brand_cian_all_mix_search", ]},
        {"descr": 'ekb_brand_cian_bdg', "fltrs": ["b2c_ekb_brand_cian_all_mix_search", ]},
        {"descr": 'novosibirsk_brand_cian_bdg', "fltrs": ["b2c_novosibirsk_brand_cian_all_mix_search", ]},
        {"descr": 'omskcity_brand_cian_bdg', "fltrs": ["b2c_omsk_brand_cian_all_mix_search", ]},
        {"descr": 'krasnodar_brand_cian_bdg', "fltrs": ["b2c_krasnodar_brand_cian_all_mix_search", ]},
        {"descr": 'kazan_brand_cian_bdg', "fltrs": ["b2c_kazan_brand_cian_all_mix_search", ]},
        {"descr": 'nn_brand_cian_bdg', "fltrs": ["b2c_nn_brand_cian_all_mix_search", ]},
        {"descr": 'penza_brand_cian_bdg', "fltrs": ["b2c_penza_brand_cian_all_mix_search", ]},
        {"descr": 'ivanovo_brand_cian_bdg', "fltrs": ["b2c_ivanovo_brand_cian_all_mix_search", ]},
        {"descr": 'sochi_brand_cian_bdg', "fltrs": ["b2c_sochi_brand_cian_all_mix_search", ]},
        {"descr": 'regs_brand_cian_bdg', "fltrs": [
                                                    "b2c_krasnoyarsk_brand_cian_all_mix_search",
                                                    "b2c_voronezh_brand_cian_all_mix_search",
                                                    "b2c_chelyabinsk_brand_cian_all_mix_search",
                                                    "b2c_irkutsk_brand_cian_all_mix_search",
                                                    "b2c_kaliningrad_brand_cian_all_mix_search",
                                                    "b2c_kemerovo_brand_cian_all_mix_search",
                                                    "b2c_krasnodar_brand_cian_all_mix_search",
                                                    "b2c_perm_brand_cian_all_mix_search",
                                                    "b2c_rostov_brand_cian_all_mix_search",
                                                    "b2c_samara_brand_cian_all_mix_search",
                                                    "b2c_sevastopol_brand_cian_all_mix_search",  ###############################
                                                    "b2c_stavropol_brand_cian_all_mix_search",
                                                    "b2c_tyumen_brand_cian_all_mix_search",
                                                    "b2c_ufa_brand_cian_all_mix_search",
                                                    "b2c_volgograd_brand_cian_all_mix_search",
                                                    "b2c_yalta_brand_cian_all_mix_search",  ###############################
                                                    "b2c_simferopol_brand_cian_all_mix_search",  # рк к заведению ###############################
                                                    "b2c_ulyanovsk_brand_cian_all_mix_search",
                                                    "b2c_tomsk_brand_cian_all_mix_search",
                                                    "b2c_kaluga_brand_cian_all_mix_search",
                                                    "b2c_ryazan_brand_cian_all_mix_search",
                                                    "b2c_tula_brand_cian_all_mix_search",
                                                    "b2c_bryansk_brand_cian_all_mix_search",
                                                    "b2c_kostroma_brand_cian_all_mix_search",
                                                    "b2c_arhangelsk_brand_cian_all_mix_search",
                                                    "b2c_vologda_brand_cian_all_mix_search",  # рк к заведению
        ]},
        {"descr": 'oth_brand_cian_bdg', "fltrs": [
                                                    "b2c_astrahan_brand_cian_all_mix_search",
                                                    "b2c_barnaul_brand_cian_all_mix_search",
                                                    "b2c_belgorod_brand_cian_all_mix_search",
                                                    "b2c_cheboksary_brand_cian_all_mix_search",
                                                    "b2c_habarovsk_brand_cian_all_mix_search",
                                                    "b2c_izhevsk_brand_cian_all_mix_search",
                                                    "b2c_kirov_brand_cian_all_mix_search",
                                                    "b2c_kurgan_brand_cian_all_mix_search",
                                                    "b2c_kursk_brand_cian_all_mix_search",
                                                    "b2c_lipetsk_brand_cian_all_mix_search",
                                                    "b2c_mahachkala_brand_cian_all_mix_search",
                                                    "b2c_novgorod_brand_cian_all_mix_search",
                                                    "b2c_orel_brand_cian_all_mix_search",
                                                    "b2c_orenburg_brand_cian_all_mix_search",
                                                    "b2c_pskov_brand_cian_all_mix_search",
                                                    "b2c_saratov_brand_cian_all_mix_search",
                                                    "b2c_smolensk_brand_cian_all_mix_search",
                                                    "b2c_surgut_brand_cian_all_mix_search",
                                                    "b2c_tambov_brand_cian_all_mix_search",
                                                    "b2c_tver_brand_cian_all_mix_search",
                                                    "b2c_ulanude_brand_cian_all_mix_search",
                                                    "b2c_vladimir_brand_cian_all_mix_search",
                                                    "b2c_vladivostok_brand_cian_all_mix_search",
                                                    "b2c_yaroslavl_brand_cian_all_mix_search",
        ]},

        {"descr": 'msk_brand_cian_mob_bdg', "fltrs": ["b2c_(dmo|bmo|mo|msk)_brand_cian_all_mob_search", ]},
        {"descr": 'spb_brand_cian_mob_bdg', "fltrs": ["b2c_spb_brand_cian_all_mob_search", ]},
        {"descr": 'regs_brand_cian_mob_bdg', "fltrs": [
                                                        "b2c_kazan_brand_cian_all_mob_search",
                                                        "b2c_nn_brand_cian_all_mob_search",
                                                        "b2c_krasnoyarsk_brand_cian_all_mob_search",
                                                        "b2c_voronezh_brand_cian_all_mob_search",
                                                        "b2c_chelyabinsk_brand_cian_all_mob_search",
                                                        "b2c_ekb_brand_cian_all_mob_search",
                                                        "b2c_irkutsk_brand_cian_all_mob_search",
                                                        "b2c_kaliningrad_brand_cian_all_mob_search",
                                                        "b2c_kemerovo_brand_cian_all_mob_search",
                                                        "b2c_krasnodar_brand_cian_all_mob_search",
                                                        "b2c_novosibirsk_brand_cian_all_mob_search",
                                                        "b2c_omsk_brand_cian_all_mob_search",
                                                        "b2c_perm_brand_cian_all_mob_search",
                                                        "b2c_rostov_brand_cian_all_mob_search",
                                                        "b2c_samara_brand_cian_all_mob_search",
                                                        "b2c_sevastopol_brand_cian_all_mob_search",  ###############################
                                                        "b2c_stavropol_brand_cian_all_mob_search",
                                                        "b2c_tyumen_brand_cian_all_mob_search",
                                                        "b2c_ufa_brand_cian_all_mob_search",
                                                        "b2c_volgograd_brand_cian_all_mob_search",
                                                        "b2c_yalta_brand_cian_all_mob_search",  ###############################
                                                        "b2c_simferopol_brand_cian_all_mob_search",  # рк к заведению
                                                        "b2c_ulyanovsk_brand_cian_all_mob_search",
                                                        "b2c_tomsk_brand_cian_all_mob_search",
                                                        "b2c_kaluga_brand_cian_all_mob_search",
                                                        "b2c_ryazan_brand_cian_all_mob_search",
                                                        "b2c_tula_brand_cian_all_mob_search",
                                                        "b2c_bryansk_brand_cian_all_mob_search",
                                                        "b2c_kostroma_brand_cian_all_mob_search",
                                                        "b2c_ivanovo_brand_cian_all_mob_search",
                                                        "b2c_arhangelsk_brand_cian_all_mob_search",
                                                        "b2c_vologda_brand_cian_all_mob_search",  # рк к заведению
                                                        "b2c_sochi_brand_cian_all_mob_search",
        ]},
        {"descr": 'oth_brand_cian_mob_bdg', "fltrs": [
                                                    "b2c_astrahan_brand_cian_all_mob_search",
                                                    "b2c_barnaul_brand_cian_all_mob_search",
                                                    "b2c_belgorod_brand_cian_all_mob_search",
                                                    "b2c_cheboksary_brand_cian_all_mob_search",
                                                    "b2c_habarovsk_brand_cian_all_mob_search",
                                                    "b2c_izhevsk_brand_cian_all_mob_search",
                                                    "b2c_kirov_brand_cian_all_mob_search",
                                                    "b2c_kurgan_brand_cian_all_mob_search",
                                                    "b2c_kursk_brand_cian_all_mob_search",
                                                    "b2c_lipetsk_brand_cian_all_mob_search",
                                                    "b2c_mahachkala_brand_cian_all_mob_search",
                                                    "b2c_novgorod_brand_cian_all_mob_search",
                                                    "b2c_orel_brand_cian_all_mob_search",
                                                    "b2c_orenburg_brand_cian_all_mob_search",
                                                    "b2c_penza_brand_cian_all_mob_search",
                                                    "b2c_pskov_brand_cian_all_mob_search",
                                                    "b2c_saratov_brand_cian_all_mob_search",
                                                    "b2c_smolensk_brand_cian_all_mob_search",
                                                    "b2c_surgut_brand_cian_all_mob_search",
                                                    "b2c_tambov_brand_cian_all_mob_search",
                                                    "b2c_tver_brand_cian_all_mob_search",
                                                    "b2c_ulanude_brand_cian_all_mob_search",
                                                    "b2c_vladimir_brand_cian_all_mob_search",
                                                    "b2c_vladivostok_brand_cian_all_mob_search",
                                                    "b2c_yaroslavl_brand_cian_all_mob_search",
        ]},

        ######################################################################################
        # Пакет: competitors #################################################################
        ######################################################################################
        {"descr": 'msk_competitors_bdg', "fltrs": ["b2c_(bmo|dmo|msk)_compet_main_all_mix_search", ]},
        {"descr": 'spb_competitors_bdg', "fltrs": ["b2c_spb_compet_main_all_mix_search", ]},
        {"descr": 'ekb_competitors_bdg', "fltrs": ["b2c_ekb_compet_main_all_mix_search", ]},
        {"descr": 'novosibirsk_competitors_bdg', "fltrs": ["b2c_novosibirsk_compet_main_all_mix_search", ]},
        {"descr": 'omskcity_competitors_bdg', "fltrs": ["b2c_omsk_compet_main_all_mix_search", ]},
        {"descr": 'krasnodar_competitors_bdg', "fltrs": ["b2c_krasnodar_compet_main_all_mix_search", ]},
        {"descr": 'kazan_competitors_bdg', "fltrs": ["b2c_kazan_compet_main_all_mix_search", ]},
        {"descr": 'nn_competitors_bdg', "fltrs": ["b2c_nn_compet_main_all_mix_search", ]},
        {"descr": 'ivanovo_competitors_bdg', "fltrs": ["b2c_ivanovo_compet_main_all_mix_search", ]},
        {"descr": 'penza_competitors_bdg', "fltrs": ["b2c_penza_compet_main_all_mix_search", ]},
        {"descr": 'regs_competitors_bdg', "fltrs": [
                                                     "b2c_krasnoyarsk_compet_main_all_mix_search",
                                                     "b2c_voronezh_compet_main_all_mix_search",
                                                     "b2c_chelyabinsk_compet_main_all_mix_search",
                                                     "b2c_irkutsk_compet_main_all_mix_search",
                                                     "b2c_kaliningrad_compet_main_all_mix_search",
                                                     "b2c_kemerovo_compet_main_all_mix_search",
                                                     "b2c_perm_compet_main_all_mix_search",
                                                     "b2c_rostov_compet_main_all_mix_search",
                                                     "b2c_samara_compet_main_all_mix_search",
                                                     "b2c_sevastopol_compet_main_all_mix_search",  ###############################
                                                     "b2c_stavropol_compet_main_all_mix_search",
                                                     "b2c_tyumen_compet_main_all_mix_search",
                                                     "b2c_ufa_compet_main_all_mix_search",
                                                     "b2c_volgograd_compet_main_all_mix_search",
                                                     "b2c_yalta_compet_main_all_mix_search",  ###############################
                                                     "b2c_simferopol_compet_main_all_mix_search",  # рк к заведению  ###############################
                                                     "b2c_ulyanovsk_compet_main_all_mix_search",
                                                     "b2c_tomsk_compet_main_all_mix_search",
                                                     "b2c_kaluga_compet_main_all_mix_search",
                                                     "b2c_ryazan_compet_main_all_mix_search",
                                                     "b2c_tula_compet_main_all_mix_search",
                                                     "b2c_bryansk_compet_main_all_mix_search",
                                                     "b2c_kostroma_compet_main_all_mix_search",
                                                     "b2c_arhangelsk_compet_main_all_mix_search",
                                                     "b2c_vologda_compet_main_all_mix_search",  # рк к заведению
                                                     "b2c_sochi_compet_main_all_mix_search",
        ]},
        {"descr": 'oth_competitors_bdg', "fltrs": [
                                                    "b2c_astrahan_compet_main_all_mix_search",
                                                    "b2c_barnaul_compet_main_all_mix_search",
                                                    "b2c_belgorod_compet_main_all_mix_search",
                                                    "b2c_cheboksary_compet_main_all_mix_search",
                                                    "b2c_habarovsk_compet_main_all_mix_search",
                                                    "b2c_izhevsk_compet_main_all_mix_search",
                                                    "b2c_kirov_compet_main_all_mix_search",
                                                    "b2c_kurgan_compet_main_all_mix_search",
                                                    "b2c_kursk_compet_main_all_mix_search",
                                                    "b2c_lipetsk_compet_main_all_mix_search",
                                                    "b2c_mahachkala_compet_main_all_mix_search",
                                                    "b2c_novgorod_compet_main_all_mix_search",
                                                    "b2c_orel_compet_main_all_mix_search",
                                                    "b2c_orenburg_compet_main_all_mix_search",
                                                    "b2c_pskov_compet_main_all_mix_search",
                                                    "b2c_saratov_compet_main_all_mix_search",
                                                    "b2c_smolensk_compet_main_all_mix_search",
                                                    "b2c_surgut_compet_main_all_mix_search",
                                                    "b2c_tambov_compet_main_all_mix_search",
                                                    "b2c_tver_compet_main_all_mix_search",
                                                    "b2c_ulanude_compet_main_all_mix_search",
                                                    "b2c_vladimir_compet_main_all_mix_search",
                                                    "b2c_vladivostok_compet_main_all_mix_search",
                                                    "b2c_yaroslavl_compet_main_all_mix_search",
        ]},

        {"descr": 'msk_brand_network_bdg', "fltrs": ["b2c_(mo|msk)_(brand_main|rsya_brand)_all_mix_network", ]},
        {"descr": 'spb_brand_network_bdg', "fltrs": ["b2c_spb_(brand_main|rsya_brand)_all_mix_network", ]},
        {"descr": 'ekb_brand_network_bdg', "fltrs": ["b2c_ekb_(brand_main|rsya_brand)_all_mix_network", ]},
        {"descr": 'novosibirsk_brand_network_bdg', "fltrs": ["b2c_novosibirsk_(brand_main|rsya_brand)_all_mix_network", ]},
        {"descr": 'omskcity_brand_network_bdg', "fltrs": ["b2c_omsk_(brand_main|rsya_brand)_all_mix_network", ]},
        {"descr": 'krasnodar_brand_network_bdg', "fltrs": ["b2c_krasnodar_(brand_main|rsya_brand)_all_mix_network", ]},

        {"descr": 'msk_compet_network_bdg', "fltrs": ["b2c_(mo|msk)_(compet_main|rsya_compet)_all_mix_network", ]},
        {"descr": 'spb_compet_network_bdg', "fltrs": ["b2c_spb_(compet_main|rsya_compet)_all_mix_network", ]},
        {"descr": 'ekb_compet_network_bdg', "fltrs": ["b2c_ekb_(compet_main|rsya_compet)_all_mix_network", ]},
        {"descr": 'novosibirsk_compet_network_bdg', "fltrs": ["b2c_novosibirsk_(compet_main|rsya_compet)_all_mix_network", ]},
        {"descr": 'omskcity_compet_network_bdg', "fltrs": ["b2c_omsk_(compet_main|rsya_compet)_all_mix_network", ]},
        {"descr": 'krasnodar_compet_network_bdg', "fltrs": ["b2c_krasnodar_(compet_main|rsya_compet)_all_mix_network", ]},

        {"descr": 'msk_general_network_bdg', "fltrs": ["b2c_msk_rsya_general_all_mix_network", ]},

        ######################################################################################
        # Пакет: rentsec #######################################################################
        ######################################################################################
        {"descr": 'msk_rentsec_qeepmetro_search_bdg', "fltrs": ["b2c_msk_general_metro_rentsec_mix_search_qeep", ]},
        {"descr": 'msk_rentsec_qeepstreets_search_bdg', "fltrs": ["b2c_msk_general_streets_rentsec_mix_search_qeep", ]},
        {"descr": 'msk_rentsec_qeepmoreg_search_bdg', "fltrs": ["b2c_msk_general_subreg_rentsec_mix_search_qeep", ]},
        {"descr": 'msk_rentsec_mix_search_bdg', "fltrs": ["b2c_(dmo|bmo|msk)_general_(null|geo|subreg)_rentsec_mix_search", ]},
        {"descr": 'msk_rentsec_tovarnaya_network_bdg', "fltrs": ["b2c_msk_tovarnaya_subreg_rentsec_mix_network", ]},

        {"descr": 'spb_rentsec_mix_search_bdg', "fltrs": ["b2c_spb_general_(null|subreg)_rentsec_mix_search", ]},
        {"descr": 'ekb_rentsec_mix_search_bdg', "fltrs": ["b2c_ekb_general_null_rentsec_mix_search", ]},
        {"descr": 'novosibirsk_rentsec_mix_search_bdg', "fltrs": ["b2c_novosibirsk_general_null_rentsec_mix_search", ]},
        {"descr": 'omskcity_rentsec_mix_search_bdg', "fltrs": ["b2c_omsk_general_null_rentsec_mix_search", ]},
        {"descr": 'krasnodar_rentsec_mix_search_bdg', "fltrs": ["b2c_krasnodar_general_null_rentsec_mix_search", ]},
        {"descr": 'kazan_rentsec_mix_search_bdg', "fltrs": ["b2c_kazan_general_null_rentsec_mix_search", ]},
        {"descr": 'nn_rentsec_mix_search_bdg', "fltrs": ["b2c_nn_general_null_rentsec_mix_search", ]},
        {"descr": 'ivanovo_rentsec_mix_search_bdg', "fltrs": ["b2c_ivanovo_general_null_rentsec_mix_search", ]},
        {"descr": 'penza_rentsec_mix_search_bdg', "fltrs": ["b2c_penza_general_null_rentsec_mix_search", ]},
        {"descr": 'sochi_rentsec_mix_search_bdg', "fltrs": ["b2c_sochi_general_null_rentsec_mix_search", ]},


        {"descr": 'regs_rentsec_mix_search_bdg', "fltrs": [
                                                            "b2c_krasnoyarsk_general_null_rentsec_mix_search",
                                                            "b2c_voronezh_general_null_rentsec_mix_search",
                                                            "b2c_chelyabinsk_general_null_rentsec_mix_search",
                                                            "b2c_irkutsk_general_null_rentsec_mix_search",
                                                            "b2c_kaliningrad_general_null_rentsec_mix_search",
                                                            "b2c_kemerovo_general_null_rentsec_mix_search",
                                                            "b2c_perm_general_null_rentsec_mix_search",
                                                            "b2c_rostov_general_null_rentsec_mix_search",
                                                            "b2c_samara_general_null_rentsec_mix_search",
                                                            "b2c_sevastopol_general_null_rentsec_mix_search",  ###############################
                                                            "b2c_stavropol_general_null_rentsec_mix_search",
                                                            "b2c_tyumen_general_null_rentsec_mix_search",
                                                            "b2c_ufa_general_null_rentsec_mix_search",
                                                            "b2c_volgograd_general_null_rentsec_mix_search",
                                                            "b2c_yalta_general_null_rentsec_mix_search",  ###############################
                                                            "b2c_simferopol_general_null_rentsec_mix_search",  # рк к заведению  ###############################
                                                            "b2c_ulyanovsk_general_null_rentsec_mix_search",
                                                            "b2c_tomsk_general_null_rentsec_mix_search",
                                                            "b2c_kaluga_general_null_rentsec_mix_search",
                                                            "b2c_ryazan_general_null_rentsec_mix_search",
                                                            "b2c_tula_general_null_rentsec_mix_search",
                                                            "b2c_bryansk_general_null_rentsec_mix_search",
                                                            "b2c_kostroma_general_null_rentsec_mix_search",
                                                            "b2c_arhangelsk_general_null_rentsec_mix_search",
                                                            "b2c_vologda_general_null_rentsec_mix_search",  # рк к заведению
        ]},
        {"descr": 'oth_rentsec_mix_search_bdg', "fltrs": [
                                                            "b2c_astrahan_general_null_rentsec_mix_search",
                                                            "b2c_barnaul_general_null_rentsec_mix_search",
                                                            "b2c_belgorod_general_null_rentsec_mix_search",
                                                            "b2c_cheboksary_general_null_rentsec_mix_search",
                                                            "b2c_habarovsk_general_null_rentsec_mix_search",
                                                            "b2c_izhevsk_general_null_rentsec_mix_search",
                                                            "b2c_kirov_general_null_rentsec_mix_search",
                                                            "b2c_kurgan_general_null_rentsec_mix_search",
                                                            "b2c_kursk_general_null_rentsec_mix_search",
                                                            "b2c_lipetsk_general_null_rentsec_mix_search",
                                                            "b2c_mahachkala_general_null_rentsec_mix_search",
                                                            "b2c_novgorod_general_null_rentsec_mix_search",
                                                            "b2c_orel_general_null_rentsec_mix_search",
                                                            "b2c_orenburg_general_null_rentsec_mix_search",
                                                            "b2c_pskov_general_null_rentsec_mix_search",
                                                            "b2c_saratov_general_null_rentsec_mix_search",
                                                            "b2c_smolensk_general_null_rentsec_mix_search",
                                                            "b2c_surgut_general_null_rentsec_mix_search",
                                                            "b2c_tambov_general_null_rentsec_mix_search",
                                                            "b2c_tver_general_null_rentsec_mix_search",
                                                            "b2c_ulanude_general_null_rentsec_mix_search",
                                                            "b2c_vladimir_general_null_rentsec_mix_search",
                                                            "b2c_vladivostok_general_null_rentsec_mix_search",
                                                            "b2c_yaroslavl_general_null_rentsec_mix_search",
        ]},

        {"descr": 'msk_dsa_rentsec_mix_search_bdg', "fltrs": ["b2c_(mo|msk)_dsa_subreg_rentsec_mix_search", ]},
        {"descr": 'spb_dsa_rentsec_mix_search_bdg', "fltrs": ["b2c_spb_dsa_subreg_rentsec_mix_search", ]},
        {"descr": 'regs_dsa_rentsec_mix_search_bdg', "fltrs": ["b2c_krasnodar_dsa_subreg_rentsec_mix_search", ]},

        {"descr": 'msk_rentsec_merchand_network_bdg', "fltrs": ["b2c_msk_merchand_feed_rentsec_mix_network", ]},
        {"descr": 'spb_rentsec_merchand_network_bdg', "fltrs": ["b2c_spb_merchand_feed_rentsec_mix_network", ]},
        {"descr": 'ekb_rentsec_merchand_network_bdg', "fltrs": ["b2c_ekb_merchand_feed_rentsec_mix_network", ]},
        {"descr": 'novosibirsk_rentsec_merchand_network_bdg', "fltrs": ["b2c_novosibirsk_merchand_feed_rentsec_mix_network", ]},
        {"descr": 'omskcity_rentsec_merchand_network_bdg', "fltrs": ["b2c_omsk_merchand_feed_rentsec_mix_network", ]},

        {"descr": 'msk_rentsec_network_bdg', "fltrs": ["b2c_(mo|msk)_(ci|general|rsya)_main_rentsec_mix_network", ]},
        {"descr": 'spb_rentsec_network_bdg', "fltrs": ["b2c_spb_(ci|general|rsya)_main_rentsec_mix_network", ]},
        {"descr": 'ekb_rentsec_network_bdg', "fltrs": ["b2c_ekb_(ci|general|rsya)_main_rentsec_mix_network", ]},
        {"descr": 'novosibirsk_rentsec_network_bdg', "fltrs": ["b2c_novosibirsk_(ci|general|rsya)_main_rentsec_mix_network", ]},
        {"descr": 'omskcity_rentsec_network_bdg', "fltrs": ["b2c_omsk_(ci|general|rsya)_main_rentsec_mix_network", ]},
        {"descr": 'krasnodar_rentsec_network_bdg', "fltrs": ["b2c_krasnodar_(ci|general|rsya)_main_rentsec_mix_network", ]},


        ######################################################################################
        # Пакет: salesec #######################################################################
        ######################################################################################
        {"descr": 'msk_salesec_info_search_bdg', "fltrs": ["b2c_msk_general_info_salesec_mix_search", ]},
        {"descr": 'msk_salesec_rlsainfo_search_bdg', "fltrs": ["b2c_msk_rlsa_info_salesec_mix_search", ]},
        {"descr": 'msk_salesec_qeepmetro_search_bdg', "fltrs": ["b2c_msk_general_metro_salesec_mix_search_qeep", ]},
        {"descr": 'msk_salesec_qeepstreets_search_bdg', "fltrs": ["b2c_msk_general_streets_salesec_mix_search_qeep", ]},
        {"descr": 'msk_salesec_qeepmoreg_search_bdg', "fltrs": ["b2c_msk_general_subreg_salesec_mix_search_qeep", ]},
        {"descr": 'msk_salesec_mix_search_bdg', "fltrs": ["b2c_(bmo|dmo|msk)_general_(null|geo|subreg)_salesec_mix_search", ]},
        {"descr": 'msk_salesec_tovarnaya_network_bdg', "fltrs": ["b2c_msk_tovarnaya_subreg_salesec_mix_network", ]},

        {"descr": 'spb_salesec_mix_search_bdg', "fltrs": ["b2c_spb_general_null_salesec_mix_search", ]},
        {"descr": 'ekb_salesec_mix_search_bdg', "fltrs": ["b2c_ekb_general_null_salesec_mix_search", ]},
        {"descr": 'novosibirsk_salesec_mix_search_bdg', "fltrs": ["b2c_novosibirsk_general_null_salesec_mix_search", ]},
        {"descr": 'omskcity_salesec_mix_search_bdg', "fltrs": ["b2c_omsk_general_null_salesec_mix_search", ]},
        {"descr": 'krasnodar_salesec_mix_search_bdg', "fltrs": ["b2c_krasnodar_general_null_salesec_mix_search", ]},
        {"descr": 'kazan_salesec_mix_search_bdg', "fltrs": ["b2c_kazan_general_null_salesec_mix_search", ]},
        {"descr": 'nn_salesec_mix_search_bdg', "fltrs": ["b2c_nn_general_null_salesec_mix_search", ]},
        {"descr": 'ivanovo_salesec_mix_search_bdg', "fltrs": ["b2c_ivanovo_general_null_salesec_mix_search", ]},
        {"descr": 'penza_salesec_mix_search_bdg', "fltrs": ["b2c_penza_general_null_salesec_mix_search", ]},
        {"descr": 'sochi_salesec_mix_search_bdg', "fltrs": ["b2c_sochi_general_null_salesec_mix_search", ]},
        {"descr": 'regs_salesec_mix_search_bdg', "fltrs": [
                                                           "b2c_krasnoyarsk_general_null_salesec_mix_search",
                                                           "b2c_voronezh_general_null_salesec_mix_search",
                                                           "b2c_chelyabinsk_general_null_salesec_mix_search",
                                                           "b2c_irkutsk_general_null_salesec_mix_search",
                                                           "b2c_kaliningrad_general_null_salesec_mix_search",
                                                           "b2c_kemerovo_general_null_salesec_mix_search",
                                                           "b2c_perm_general_null_salesec_mix_search",
                                                           "b2c_rostov_general_null_salesec_mix_search",
                                                           "b2c_samara_general_null_salesec_mix_search",
                                                           "b2c_sevastopol_general_null_salesec_mix_search",  ###############################
                                                           "b2c_stavropol_general_null_salesec_mix_search",
                                                           "b2c_tyumen_general_null_salesec_mix_search",
                                                           "b2c_ufa_general_null_salesec_mix_search",
                                                           "b2c_volgograd_general_null_salesec_mix_search",
                                                           "b2c_yalta_general_null_salesec_mix_search", ###############################
                                                           "b2c_simferopol_general_null_salesec_mix_search",  # рк к заведению ###############################
                                                           "b2c_ulyanovsk_general_null_salesec_mix_search",
                                                           "b2c_tomsk_general_null_salesec_mix_search",
                                                           "b2c_kaluga_general_null_salesec_mix_search",
                                                           "b2c_ryazan_general_null_salesec_mix_search",
                                                           "b2c_tula_general_null_salesec_mix_search",
                                                           "b2c_bryansk_general_null_salesec_mix_search",
                                                           "b2c_kostroma_general_null_salesec_mix_search",
                                                           "b2c_arhangelsk_general_null_salesec_mix_search",
                                                           "b2c_vologda_general_null_salesec_mix_search",  # рк к заведению
        ]},
        {"descr": 'oth_salesec_mix_search_bdg', "fltrs": [
                                                            "b2c_astrahan_general_null_salesec_mix_search",
                                                            "b2c_barnaul_general_null_salesec_mix_search",
                                                            "b2c_belgorod_general_null_salesec_mix_search",
                                                            "b2c_cheboksary_general_null_salesec_mix_search",
                                                            "b2c_habarovsk_general_null_salesec_mix_search",
                                                            "b2c_izhevsk_general_null_salesec_mix_search",
                                                            "b2c_kirov_general_null_salesec_mix_search",
                                                            "b2c_kurgan_general_null_salesec_mix_search",
                                                            "b2c_kursk_general_null_salesec_mix_search",
                                                            "b2c_lipetsk_general_null_salesec_mix_search",
                                                            "b2c_mahachkala_general_null_salesec_mix_search",
                                                            "b2c_novgorod_general_null_salesec_mix_search",
                                                            "b2c_orel_general_null_salesec_mix_search",
                                                            "b2c_orenburg_general_null_salesec_mix_search",
                                                            "b2c_pskov_general_null_salesec_mix_search",
                                                            "b2c_saratov_general_null_salesec_mix_search",
                                                            "b2c_smolensk_general_null_salesec_mix_search",
                                                            "b2c_surgut_general_null_salesec_mix_search",
                                                            "b2c_tambov_general_null_salesec_mix_search",
                                                            "b2c_tver_general_null_salesec_mix_search",
                                                            "b2c_ulanude_general_null_salesec_mix_search",
                                                            "b2c_vladimir_general_null_salesec_mix_search",
                                                            "b2c_vladivostok_general_null_salesec_mix_search",
                                                            "b2c_yaroslavl_general_null_salesec_mix_search",
        ]},

        {"descr": 'msk_dsa_salesec_mix_search_bdg', "fltrs": ["b2c_(mo|msk)_dsa_subreg_salesec_mix_search",
                                                              "b2c_msk_dsa_adfeed_salesec_mix_search",
                                                              ]},
        {"descr": 'spb_dsa_salesec_mix_search_bdg', "fltrs": ["b2c_spb_dsa_subreg_salesec_mix_search",
                                                              "b2c_spb_dsa_adfeed_salesec_mix_search",
                                                              ]},
        {"descr": 'regs_dsa_salesec_mix_search_bdg', "fltrs": ["b2c_krasnodar_dsa_subreg_salesec_mix_search",
                                                               "b2c_krasnodar_dsa_adfeed_salesec_mix_search",
                                                               ]},

        {"descr": 'msk_salesec_merchand_network_bdg', "fltrs": ["b2c_msk_merchand_feed_salesec_mix_network", ]},
        {"descr": 'spb_salesec_merchand_network_bdg', "fltrs": ["b2c_spb_merchand_feed_salesec_mix_network", ]},
        {"descr": 'ekb_salesec_merchand_network_bdg', "fltrs": ["b2c_ekb_merchand_feed_salesec_mix_network", ]},
        {"descr": 'novosibirsk_salesec_merchand_network_bdg', "fltrs": ["b2c_novosibirsk_merchand_feed_salesec_mix_network", ]},
        {"descr": 'omskcity_salesec_merchand_network_bdg', "fltrs": ["b2c_omsk_merchand_feed_salesec_mix_network", ]},

        {"descr": 'msk_salesec_network_bdg', "fltrs": ["b2c_(mo|msk)_(ci|general|rsya)_main_salesec_mix_network", ]},
        {"descr": 'spb_salesec_network_bdg', "fltrs": ["b2c_spb_(ci|general|rsya)_main_salesec_mix_network", ]},
        {"descr": 'novosibirsk_salesec_network_bdg', "fltrs": ["b2c_novosibirsk_(ci|general|rsya)_main_salesec_mix_network", ]},
        {"descr": 'ekb_salesec_network_bdg', "fltrs": ["b2c_ekb_(ci|general|rsya)_main_salesec_mix_network", ]},
        {"descr": 'omskcity_salesec_network_bdg', "fltrs": ["b2c_omsk_(ci|general|rsya)_main_salesec_mix_network", ]},
        {"descr": 'krasnodar_salesec_network_bdg', "fltrs": ["b2c_krasnodar_(ci|general|rsya)_main_salesec_mix_network", ]},


        {"descr": 'b2c_msk_discovery_main_salesec_mix_network', "fltrs": ["(b2c|b2b)_(mo|msk)_discovery_main_salesec_mix_network", ]},
        {"descr": 'b2c_spb_discovery_main_salesec_mix_network', "fltrs": ["(b2c|b2b)_spb_discovery_main_salesec_mix_network", ]},
        {"descr": 'b2c_22reg_discovery_main_salesec_mix_network', "fltrs": ["(b2c|b2b)_22reg_discovery_main_salesec_mix_network", ]},

        {"descr": 'msk_salesec_mk_network_bdg', "fltrs": ["b2c_msk_mk_general_salesec_mix_network", ]},

        ######################################################################################
        # Пакет: sub #########################################################################
        ######################################################################################
        {"descr": 'msk_rentsub_mix_search_bdg', "fltrs": ["b2c_(bmo|dmo|msk)_general_null_rentsub_mix_search", ]},
        {"descr": 'spb_rentsub_mix_search_bdg', "fltrs": ["b2c_spb_general_null_rentsub_mix_search", ]},
        {"descr": 'ekb_rentsub_mix_search_bdg', "fltrs": ["b2c_ekb_general_null_rentsub_mix_search", ]},
        {"descr": 'novosibirsk_rentsub_mix_search_bdg', "fltrs": ["b2c_novosibirsk_general_null_rentsub_mix_search", ]},
        {"descr": 'omskcity_rentsub_mix_search_bdg', "fltrs": ["b2c_omsk_general_null_rentsub_mix_search", ]},
        {"descr": 'krasnodar_rentsub_mix_search_bdg', "fltrs": ["b2c_krasnodar_general_null_rentsub_mix_search", ]},
        {"descr": 'kazan_rentsub_mix_search_bdg', "fltrs": ["b2c_kazan_general_null_rentsub_mix_search", ]},
        {"descr": 'nn_rentsub_mix_search_bdg', "fltrs": ["b2c_nn_general_null_rentsub_mix_search", ]},
        {"descr": 'ivanovo_rentsub_mix_search_bdg', "fltrs": ["b2c_ivanovo_general_null_rentsub_mix_search", ]},
        {"descr": 'penza_rentsub_mix_search_bdg', "fltrs": ["b2c_penza_general_null_rentsub_mix_search", ]},
        {"descr": 'penza_rentsub_mix_search_bdg', "fltrs": ["b2c_penza_general_null_rentsub_mix_search", ]},
        {"descr": 'sochi_rentsub_mix_search_bdg', "fltrs": ["b2c_sochi_general_null_rentsub_mix_search", ]},
        {"descr": 'regs_rentsub_mix_search_bdg', "fltrs": [
                                                               "b2c_krasnoyarsk_general_null_rentsub_mix_search",
                                                               "b2c_voronezh_general_null_rentsub_mix_search",
                                                               "b2c_chelyabinsk_general_null_rentsub_mix_search",
                                                               "b2c_irkutsk_general_null_rentsub_mix_search",
                                                               "b2c_kaliningrad_general_null_rentsub_mix_search",
                                                               "b2c_kemerovo_general_null_rentsub_mix_search",
                                                               "b2c_perm_general_null_rentsub_mix_search",
                                                               "b2c_rostov_general_null_rentsub_mix_search",
                                                               "b2c_samara_general_null_rentsub_mix_search",
                                                               "b2c_sevastopol_general_null_rentsub_mix_search",  ###############################
                                                               "b2c_stavropol_general_null_rentsub_mix_search",
                                                               "b2c_tyumen_general_null_rentsub_mix_search",
                                                               "b2c_ufa_general_null_rentsub_mix_search",
                                                               "b2c_volgograd_general_null_rentsub_mix_search",
                                                               "b2c_yalta_general_null_rentsub_mix_search",  ###############################
                                                               "b2c_simferopol_general_null_rentsub_mix_search",  # рк к заведению  ###############################
                                                               "b2c_ulyanovsk_general_null_rentsub_mix_search",
                                                               "b2c_tomsk_general_null_rentsub_mix_search",
                                                               "b2c_kaluga_general_null_rentsub_mix_search",
                                                               "b2c_ryazan_general_null_rentsub_mix_search",
                                                               "b2c_tula_general_null_rentsub_mix_search",
                                                               "b2c_bryansk_general_null_rentsub_mix_search",
                                                               "b2c_kostroma_general_null_rentsub_mix_search",
                                                               "b2c_arhangelsk_general_null_rentsub_mix_search",
                                                               "b2c_vologda_general_null_rentsub_mix_search",  # рк к заведению
        ]},

        {"descr": 'msk_rentsub_merchand_network_bdg', "fltrs": ["b2c_msk_merchand_feed_rentsub_mix_network", ]},
        {"descr": 'spb_rentsub_merchand_network_bdg', "fltrs": ["b2c_spb_merchand_feed_rentsub_mix_network", ]},
        {"descr": 'ekb_rentsub_merchand_network_bdg', "fltrs": ["b2c_ekb_merchand_feed_rentsub_mix_network", ]},
        {"descr": 'novosibirsk_rentsub_merchand_network_bdg', "fltrs": ["b2c_novosibirsk_merchand_feed_rentsub_mix_network", ]},
        {"descr": 'omskcity_rentsub_merchand_network_bdg', "fltrs": ["b2c_omsk_merchand_feed_rentsub_mix_network", ]},

        {"descr": 'msk_salesub_qeepmoreg_search_bdg', "fltrs": ["b2c_msk_general_subreg_salesub_mix_search_qeep", ]},
        {"descr": 'msk_salesub_mix_search_bdg', "fltrs": ["b2c_(bmo|dmo|msk)_general_(null_salesub|geo_sub)_mix_search", ]},
        {"descr": 'spb_salesub_mix_search_bdg', "fltrs": ["b2c_spb_general_null_salesub_mix_search", ]},
        {"descr": 'ekb_salesub_mix_search_bdg', "fltrs": ["b2c_ekb_general_null_salesub_mix_search", ]},
        {"descr": 'novosibirsk_salesub_mix_search_bdg', "fltrs": ["b2c_novosibirsk_general_null_salesub_mix_search", ]},
        {"descr": 'omskcity_salesub_mix_search_bdg', "fltrs": ["b2c_omsk_general_null_salesub_mix_search", ]},
        {"descr": 'krasnodar_salesub_mix_search_bdg', "fltrs": ["b2c_krasnodar_general_null_salesub_mix_search", ]},
        {"descr": 'kazan_salesub_mix_search_bdg', "fltrs": ["b2c_kazan_general_null_salesub_mix_search", ]},
        {"descr": 'nn_salesub_mix_search_bdg', "fltrs": ["b2c_nn_general_null_salesub_mix_search", ]},
        {"descr": 'ivanovo_salesub_mix_search_bdg', "fltrs": ["b2c_ivanovo_general_null_salesub_mix_search", ]},
        {"descr": 'penza_salesub_mix_search_bdg', "fltrs": ["b2c_penza_general_null_salesub_mix_search", ]},
        {"descr": 'sochi_salesub_mix_search_bdg', "fltrs": ["b2c_sochi_general_null_salesub_mix_search", ]},
        {"descr": 'regs_salesub_mix_search_bdg', "fltrs": [
                                                            "b2c_krasnoyarsk_general_null_salesub_mix_search",
                                                            "b2c_voronezh_general_null_salesub_mix_search",
                                                            "b2c_chelyabinsk_general_null_salesub_mix_search",
                                                            "b2c_irkutsk_general_null_salesub_mix_search",
                                                            "b2c_kaliningrad_general_null_salesub_mix_search",
                                                            "b2c_kemerovo_general_null_salesub_mix_search",
                                                            "b2c_perm_general_null_salesub_mix_search",
                                                            "b2c_rostov_general_null_salesub_mix_search",
                                                            "b2c_samara_general_null_salesub_mix_search",
                                                            "b2c_sevastopol_general_null_salesub_mix_search",  ###############################
                                                            "b2c_stavropol_general_null_salesub_mix_search",
                                                            "b2c_tyumen_general_null_salesub_mix_search",
                                                            "b2c_ufa_general_null_salesub_mix_search",
                                                            "b2c_volgograd_general_null_salesub_mix_search",
                                                            "b2c_yalta_general_null_salesub_mix_search",  ###############################
                                                            "b2c_simferopol_general_null_salesub_mix_search",  # рк к заведению  ###############################
                                                            "b2c_ulyanovsk_general_null_salesub_mix_search",
                                                            "b2c_tomsk_general_null_salesub_mix_search",
                                                            "b2c_kaluga_general_null_salesub_mix_search",
                                                            "b2c_ryazan_general_null_salesub_mix_search",
                                                            "b2c_tula_general_null_salesub_mix_search",
                                                            "b2c_bryansk_general_null_salesub_mix_search",
                                                            "b2c_kostroma_general_null_salesub_mix_search",
                                                            "b2c_arhangelsk_general_null_salesub_mix_search",
                                                            "b2c_vologda_general_null_salesub_mix_search",  # рк к заведению
        ]},

        {"descr": 'msk_salesub_merchand_network_bdg', "fltrs": ["b2c_msk_merchand_feed_salesub_mix_network", ]},
        {"descr": 'spb_salesub_merchand_network_bdg', "fltrs": ["b2c_spb_merchand_feed_salesub_mix_network", ]},
        {"descr": 'ekb_salesub_merchand_network_bdg', "fltrs": ["b2c_ekb_merchand_feed_salesub_mix_network", ]},
        {"descr": 'novosibirsk_salesub_merchand_network_bdg', "fltrs": ["b2c_novosibirsk_merchand_feed_salesub_mix_network", ]},
        {"descr": 'omskcity_salesub_merchand_network_bdg', "fltrs": ["b2c_omsk_merchand_feed_salesub_mix_network", ]},


        {"descr": 'msk_dsa_sub_mix_search_bdg', "fltrs": ["b2c_(mo|msk)_dsa_subreg_sub_mix_search", ]},
        {"descr": 'spb_dsa_sub_mix_search_bdg', "fltrs": ["b2c_spb_dsa_subreg_sub_mix_search", ]},
        {"descr": 'novosibirsk_dsa_sub_mix_search_bdg', "fltrs": ["b2c_novosibirsk_dsa_subreg_sub_mix_search", ]},
        {"descr": 'omskcity_dsa_sub_mix_search_bdg', "fltrs": ["b2c_omsk_dsa_subreg_sub_mix_search", ]},
        {"descr": 'ekb_dsa_sub_mix_search_bdg', "fltrs": ["b2c_ekb_dsa_subreg_sub_mix_search", ]},


        {"descr": 'msk_salesub_rtg_network_bdg', "fltrs": ["b2c_msk_rtg_site_salesub_mix_network",
                                                           "b2c_msk_rtg_withoutlead_salesub_mix_network",
                                                           "b2c_msk_rtg_withlead_salesub_mix_network"]},
        {"descr": 'msk_rentsub_rtg_network_bdg', "fltrs": ["b2c_msk_rtg_site_rentsub_mix_network",
                                                           "b2c_msk_rtg_withoutlead_rentsub_mix_network",
                                                           "b2c_msk_rtg_withlead_rentsub_mix_network"
                                                           ]},
        {"descr": 'spb_salesub_rtg_network_bdg', "fltrs": ["b2c_spb_rtg_site_salesub_mix_network",
                                                           "b2c_spb_rtg_withoutlead_salesub_mix_network",
                                                           "b2c_spb_rtg_withlead_salesub_mix_network"
                                                           ]},
        {"descr": 'spb_rentsub_rtg_network_bdg', "fltrs": ["b2c_spb_rtg_site_rentsub_mix_network",
                                                           "b2c_spb_rtg_withoutlead_rentsub_mix_network",
                                                           "b2c_spb_rtg_withlead_rentsub_mix_network"
                                                           ]},


        {"descr": 'msk_sub_network_bdg', "fltrs": ["b2c_msk_general_null_sub_mix_network", ]},
        {"descr": 'spb_sub_network_bdg', "fltrs": ["b2c_spb_general_null_sub_mix_network", ]},
        {"descr": 'novosibirsk_sub_network_bdg', "fltrs": ["b2c_novosibirsk_general_null_sub_mix_network", ]},
        {"descr": 'omskcity_sub_network_bdg', "fltrs": ["b2c_omsk_general_null_sub_mix_network", ]},
        {"descr": 'ekb_sub_network_bdg', "fltrs": ["b2c_ekb_general_null_sub_mix_network", ]},
        {"descr": 'krasnodar_sub_network_bdg', "fltrs": ["b2c_krasnodar_general_null_sub_mix_network", ]},


        {"descr": 'msk_sub_mkb_search_bdg', "fltrs": ["b2c_msk_general_mkb_sub_mix_search", ]},
        {"descr": 'spb_sub_mkb_search_bdg', "fltrs": ["b2c_spb_general_mkb_sub_mix_search", ]},
        {"descr": 'novosibirsk_sub_mkb_search_bdg', "fltrs": ["b2c_novosibirsk_general_mkb_sub_mix_search", ]},
        {"descr": 'omskcity_sub_mkb_search_bdg', "fltrs": ["b2c_omsk_general_mkb_sub_mix_search", ]},
        {"descr": 'ekb_sub_mkb_search_bdg', "fltrs": ["b2c_ekb_general_mkb_sub_mix_search", ]},
        {"descr": 'krasnodar_sub_mkb_search_bdg', "fltrs": ["b2c_krasnodar_general_mkb_sub_mix_search", ]},


        {"descr": 'msk_sub_mk_media_network_bdg', "fltrs": ["b2c_msk_media_null_sub_mix_network", ]},
        {"descr": 'spb_sub_mk_media_network_bdg', "fltrs": ["b2c_spb_media_null_sub_mix_network", ]},
        {"descr": 'novosibirsk_sub_mk_media_network_bdg', "fltrs": ["b2c_novosibirsk_media_null_sub_mix_network", ]},
        {"descr": 'omskcity_sub_mk_media_network_bdg', "fltrs": ["b2c_omsk_media_null_sub_mix_network", ]},
        {"descr": 'ekb_sub_mk_media_network_bdg', "fltrs": ["b2c_ekb_media_null_sub_mix_network", ]},
        {"descr": 'krasnodar_sub_mk_media_network_bdg', "fltrs": ["b2c_krasnodar_media_null_sub_mix_network", ]},
        {"descr": 'sochi_sub_mk_media_network_bdg', "fltrs": ["b2c_sochi_media_null_sub_mix_network", ]},

        ######################################################################################
        # Пакет: DRTG  #########################################################################
        ######################################################################################
        {"descr": 'msk_sbyndx_salesub_bdg', "fltrs": ["b2c_msk_rtg_smart_salesub_mix_network", ]},
        {"descr": 'msk_sbyndxlal_salesub_bdg', "fltrs": ["b2c_msk_rtg_smartlal_salesub_mix_network", ]},
        {"descr": 'spb_sbyndx_salesub_bdg', "fltrs": ["b2c_spb_rtg_smart_salesub_mix_network", ]},
        {"descr": 'spb_sbyndxlal_salesub_bdg', "fltrs": ["b2c_spb_rtg_smartlal_salesub_mix_network", ]},
        {"descr": 'novosibirsk_sbyndx_salesub_bdg', "fltrs": ["b2c_novosibirsk_rtg_smart_salesub_mix_network", ]},
        {"descr": 'novosibirsk_sbyndxlal_salesub_bdg', "fltrs": ["b2c_novosibirsk_rtg_smartlal_salesub_mix_network", ]},
        {"descr": 'omskcity_sbyndx_salesub_bdg', "fltrs": ["b2c_omsk_rtg_smart_salesub_mix_network", ]},
        {"descr": 'omskcity_sbyndxlal_salesub_bdg', "fltrs": ["b2c_omsk_rtg_smartlal_salesub_mix_network", ]},
        {"descr": 'ekb_sbyndx_salesub_bdg', "fltrs": ["b2c_ekb_rtg_smart_salesub_mix_network", ]},
        {"descr": 'ekb_sbyndxlal_salesub_bdg', "fltrs": ["b2c_ekb_rtg_smartlal_salesub_mix_network", ]},
        {"descr": 'krasnodar_sbyndx_salesub_bdg', "fltrs": ["b2c_krasnodar_rtg_smart_salesub_mix_network", ]},
        {"descr": 'krasnodar_sbyndxlal_salesub_bdg', "fltrs": ["b2c_krasnodar_rtg_smartlal_salesub_mix_network", ]},

        {"descr": 'msk_sbyndx_rentsec_bdg', "fltrs": ["b2c_msk_rtg_smart_rentsec_mix_network", ]},
        {"descr": 'msk_sbyndxlal_rentsec_bdg', "fltrs": ["b2c_msk_rtg_smartlal_rentsec_mix_network", ]},
        {"descr": 'spb_sbyndx_rentsec_bdg', "fltrs": ["b2c_spb_rtg_smart_rentsec_mix_network", ]},
        {"descr": 'spb_sbyndxlal_rentsec_bdg', "fltrs": ["b2c_spb_rtg_smartlal_rentsec_mix_network", ]},
        {"descr": 'novosibirsk_sbyndx_rentsec_bdg', "fltrs": ["b2c_novosibirsk_rtg_smart_rentsec_mix_network", ]},
        {"descr": 'novosibirsk_sbyndxlal_rentsec_bdg', "fltrs": ["b2c_novosibirsk_rtg_smartlal_rentsec_mix_network", ]},
        {"descr": 'omskcity_sbyndx_rentsec_bdg', "fltrs": ["b2c_omsk_rtg_smart_rentsec_mix_network", ]},
        {"descr": 'omskcity_sbyndxlal_rentsec_bdg', "fltrs": ["b2c_omsk_rtg_smartlal_rentsec_mix_network", ]},
        {"descr": 'ekb_sbyndx_rentsec_bdg', "fltrs": ["b2c_ekb_rtg_smart_rentsec_mix_network", ]},
        {"descr": 'ekb_sbyndxlal_rentsec_bdg', "fltrs": ["b2c_ekb_rtg_smartlal_rentsec_mix_network", ]},
        {"descr": 'krasnodar_sbyndx_rentsec_bdg', "fltrs": ["b2c_krasnodar_rtg_smart_rentsec_mix_network", ]},
        {"descr": 'krasnodar_sbyndxlal_rentsec_bdg', "fltrs": ["b2c_krasnodar_rtg_smartlal_rentsec_mix_network", ]},

        ######################################################################################
        # Пакет: DRTG salesec ################################################################
        ######################################################################################
        {"descr": 'msk_sbyndx_salesec_bdg', "fltrs": ["b2c_msk_rtg_smart_salesec_mix_network", ]},
        {"descr": 'msk_sbyndxlal_salesec_bdg', "fltrs": ["b2c_msk_rtg_smartlal_salesec_mix_network", ]},
        {"descr": 'spb_sbyndx_salesec_bdg', "fltrs": ["b2c_spb_rtg_smart_salesec_mix_network", ]},
        {"descr": 'spb_sbyndxlal_salesec_bdg', "fltrs": ["b2c_spb_rtg_smartlal_salesec_mix_network", ]},
        {"descr": 'novosibirsk_sbyndx_salesec_bdg', "fltrs": ["b2c_novosibirsk_rtg_smart_salesec_mix_network", ]},
        {"descr": 'novosibirsk_sbyndxlal_salesec_bdg', "fltrs": ["b2c_novosibirsk_rtg_smartlal_salesec_mix_network", ]},
        {"descr": 'omskcity_sbyndx_salesec_bdg', "fltrs": ["b2c_omsk_rtg_smart_salesec_mix_network", ]},
        {"descr": 'omskcity_sbyndxlal_salesec_bdg', "fltrs": ["b2c_omsk_rtg_smartlal_salesec_mix_network", ]},
        {"descr": 'ekb_sbyndx_salesec_bdg', "fltrs": ["b2c_ekb_rtg_smart_salesec_mix_network", ]},
        {"descr": 'ekb_sbyndxlal_salesec_bdg', "fltrs": ["b2c_ekb_rtg_smartlal_salesec_mix_network", ]},
        {"descr": 'krasnodar_sbyndx_salesec_bdg', "fltrs": ["b2c_krasnodar_rtg_smart_salesec_mix_network", ]},
        {"descr": 'krasnodar_sbyndxlal_salesec_bdg', "fltrs": ["b2c_krasnodar_rtg_smartlal_salesec_mix_network", ]},

        {"descr": 'msk_drtg_salesec_bdg', "fltrs": ["b2c_(mo|msk)_drtg_site_salesec_mix_network", ]},
        {"descr": 'spb_drtg_salesec_bdg', "fltrs": ["b2c_spb_drtg_site_salesec_mix_network", ]},
        {"descr": 'regs_drtg_salesec_bdg', "fltrs": [
                                                     "b2c_kazan_drtg_site_salesec_mix_network",
                                                     "b2c_nn_drtg_site_salesec_mix_network",
                                                     "b2c_krasnoyarsk_drtg_site_salesec_mix_network",
                                                     "b2c_voronezh_drtg_site_salesec_mix_network",
                                                     "b2c_chelyabinsk_drtg_site_salesec_mix_network",
                                                     "b2c_ekb_drtg_site_salesec_mix_network",
                                                     "b2c_irkutsk_drtg_site_salesec_mix_network",
                                                     "b2c_kaliningrad_drtg_site_salesec_mix_network",
                                                     "b2c_kemerovo_drtg_site_salesec_mix_network",
                                                     "b2c_krasnodar_drtg_site_salesec_mix_network",
                                                     "b2c_novosibirsk_drtg_site_salesec_mix_network",
                                                     "b2c_omsk_drtg_site_salesec_mix_network",
                                                     "b2c_perm_drtg_site_salesec_mix_network",
                                                     "b2c_rostov_drtg_site_salesec_mix_network",
                                                     "b2c_samara_drtg_site_salesec_mix_network",
                                                     "b2c_sevastopol_drtg_site_salesec_mix_network",  ###############################
                                                     "b2c_stavropol_drtg_site_salesec_mix_network",
                                                     "b2c_tyumen_drtg_site_salesec_mix_network",
                                                     "b2c_ufa_drtg_site_salesec_mix_network",
                                                     "b2c_volgograd_drtg_site_salesec_mix_network",
                                                     "b2c_yalta_drtg_site_salesec_mix_network",  ###############################
                                                     "b2c_simferopol_drtg_site_salesec_mix_network",  # рк к заведению  ###############################
                                                     "b2c_ulyanovsk_drtg_site_salesec_mix_network",
                                                     "b2c_tomsk_drtg_site_salesec_mix_network",
                                                     "b2c_kaluga_drtg_site_salesec_mix_network",
                                                     "b2c_ryazan_drtg_site_salesec_mix_network",
                                                     "b2c_tula_drtg_site_salesec_mix_network",
                                                     "b2c_bryansk_drtg_site_salesec_mix_network",
                                                     "b2c_kostroma_drtg_site_salesec_mix_network",
                                                     "b2c_ivanovo_drtg_site_salesec_mix_network",
                                                     "b2c_arhangelsk_drtg_site_salesec_mix_network",
                                                     "b2c_vologda_drtg_site_salesec_mix_network",  # рк к заведению
                                                     "b2c_sochi_drtg_site_salesec_mix_network",
        ]},

        {"descr": 'msk_dynprosp_salesec_bdg', "fltrs": ["b2c_(mo|msk)_dynprosp_site_salesec_mix_network", ]},
        {"descr": 'spb_dynprosp_salesec_bdg', "fltrs": ["b2c_spb_dynprosp_site_salesec_mix_network", ]},
        {"descr": 'regs_dynprosp_salesec_bdg', "fltrs": [
                                                      "b2c_kazan_dynprosp_site_salesec_mix_network",
                                                      "b2c_nn_dynprosp_site_salesec_mix_network",
                                                      "b2c_krasnoyarsk_dynprosp_site_salesec_mix_network",
                                                      "b2c_voronezh_dynprosp_site_salesec_mix_network",
                                                      "b2c_chelyabinsk_dynprosp_site_salesec_mix_network",
                                                      "b2c_ekb_dynprosp_site_salesec_mix_network",
                                                      "b2c_irkutsk_dynprosp_site_salesec_mix_network",
                                                      "b2c_kaliningrad_dynprosp_site_salesec_mix_network",
                                                      "b2c_kemerovo_dynprosp_site_salesec_mix_network",
                                                      "b2c_krasnodar_dynprosp_site_salesec_mix_network",
                                                      "b2c_novosibirsk_dynprosp_site_salesec_mix_network",
                                                      "b2c_omsk_dynprosp_site_salesec_mix_network",
                                                      "b2c_perm_dynprosp_site_salesec_mix_network",
                                                      "b2c_rostov_dynprosp_site_salesec_mix_network",
                                                      "b2c_samara_dynprosp_site_salesec_mix_network",
                                                      "b2c_sevastopol_dynprosp_site_salesec_mix_network",  ###############################
                                                      "b2c_stavropol_dynprosp_site_salesec_mix_network",
                                                      "b2c_tyumen_dynprosp_site_salesec_mix_network",
                                                      "b2c_ufa_dynprosp_site_salesec_mix_network",
                                                      "b2c_volgograd_dynprosp_site_salesec_mix_network",
                                                      "b2c_yalta_dynprosp_site_salesec_mix_network",  ###############################
                                                      "b2c_simferopol_dynprosp_site_salesec_mix_network",  # рк к заведению  ###############################
                                                      "b2c_ulyanovsk_dynprosp_site_salesec_mix_network",
                                                      "b2c_tomsk_dynprosp_site_salesec_mix_network",
                                                      "b2c_kaluga_dynprosp_site_salesec_mix_network",
                                                      "b2c_ryazan_dynprosp_site_salesec_mix_network",
                                                      "b2c_tula_dynprosp_site_salesec_mix_network",
                                                      "b2c_bryansk_dynprosp_site_salesec_mix_network",
                                                      "b2c_kostroma_dynprosp_site_salesec_mix_network",
                                                      "b2c_ivanovo_dynprosp_site_salesec_mix_network",
                                                      "b2c_arhangelsk_dynprosp_site_salesec_mix_network",
                                                      "b2c_vologda_dynprosp_site_salesec_mix_network",  # рк к заведению
                                                      "b2c_sochi_dynprosp_site_salesec_mix_network",

        ]},


        ######################################################################################
        # Пакет: DRTG salesub ################################################################
        ######################################################################################
        {"descr": 'msk_drtg_salesub_bdg', "fltrs": ["b2c_(mo|msk)_drtg_site_salesub_mix_network", ]},
        {"descr": 'spb_drtg_salesub_bdg', "fltrs": ["b2c_spb_drtg_site_salesub_mix_network", ]},
        {"descr": 'regs_drtg_salesub_bdg', "fltrs": [
                                                      "b2c_kazan_drtg_site_salesub_mix_network",
                                                      "b2c_nn_drtg_site_salesub_mix_network",
                                                      "b2c_krasnoyarsk_drtg_site_salesub_mix_network",
                                                      "b2c_voronezh_drtg_site_salesub_mix_network",
                                                      "b2c_chelyabinsk_drtg_site_salesub_mix_network",
                                                      "b2c_ekb_drtg_site_salesub_mix_network",
                                                      "b2c_irkutsk_drtg_site_salesub_mix_network",
                                                      "b2c_kaliningrad_drtg_site_salesub_mix_network",
                                                      "b2c_kemerovo_drtg_site_salesub_mix_network",
                                                      "b2c_krasnodar_drtg_site_salesub_mix_network",
                                                      "b2c_novosibirsk_drtg_site_salesub_mix_network",
                                                      "b2c_omsk_drtg_site_salesub_mix_network",
                                                      "b2c_perm_drtg_site_salesub_mix_network",
                                                      "b2c_rostov_drtg_site_salesub_mix_network",
                                                      "b2c_samara_drtg_site_salesub_mix_network",
                                                      "b2c_sevastopol_drtg_site_salesub_mix_network",  ###############################
                                                      "b2c_stavropol_drtg_site_salesub_mix_network",
                                                      "b2c_tyumen_drtg_site_salesub_mix_network",
                                                      "b2c_ufa_drtg_site_salesub_mix_network",
                                                      "b2c_volgograd_drtg_site_salesub_mix_network",
                                                      "b2c_yalta_drtg_site_salesub_mix_network",  ###############################
                                                      "b2c_simferopol_drtg_site_salesub_mix_network",  # рк к заведению  ###############################
                                                      "b2c_ulyanovsk_drtg_site_salesub_mix_network",
                                                      "b2c_tomsk_drtg_site_salesub_mix_network",
                                                      "b2c_kaluga_drtg_site_salesub_mix_network",
                                                      "b2c_ryazan_drtg_site_salesub_mix_network",
                                                      "b2c_tula_drtg_site_salesub_mix_network",
                                                      "b2c_bryansk_drtg_site_salesub_mix_network",
                                                      "b2c_kostroma_drtg_site_salesub_mix_network",
                                                      "b2c_ivanovo_drtg_site_salesub_mix_network",
                                                      "b2c_arhangelsk_drtg_site_salesub_mix_network",
                                                      "b2c_vologda_drtg_site_salesub_mix_network",  # рк к заведению
                                                      "b2c_sochi_drtg_site_salesub_mix_network",

        ]},
        ######################################################################################
        # Пакет: DRTG rentsub ################################################################
        ######################################################################################
        {"descr": 'msk_drtg_rentsub_bdg', "fltrs": ["b2c_(mo|msk)_drtg_site_rentsub_mix_network", ]},
        {"descr": 'spb_drtg_rentsub_bdg', "fltrs": ["b2c_spb_drtg_site_rentsub_mix_network", ]},
        {"descr": 'regs_drtg_rentsub_bdg', "fltrs": [
                                                      "b2c_kazan_drtg_site_rentsub_mix_network",
                                                      "b2c_nn_drtg_site_rentsub_mix_network",
                                                      "b2c_krasnoyarsk_drtg_site_rentsub_mix_network",
                                                      "b2c_voronezh_drtg_site_rentsub_mix_network",
                                                      "b2c_chelyabinsk_drtg_site_rentsub_mix_network",
                                                      "b2c_ekb_drtg_site_rentsub_mix_network",
                                                      "b2c_irkutsk_drtg_site_rentsub_mix_network",
                                                      "b2c_kaliningrad_drtg_site_rentsub_mix_network",
                                                      "b2c_kemerovo_drtg_site_rentsub_mix_network",
                                                      "b2c_krasnodar_drtg_site_rentsub_mix_network",
                                                      "b2c_novosibirsk_drtg_site_rentsub_mix_network",
                                                      "b2c_omsk_drtg_site_rentsub_mix_network",
                                                      "b2c_perm_drtg_site_rentsub_mix_network",
                                                      "b2c_rostov_drtg_site_rentsub_mix_network",
                                                      "b2c_samara_drtg_site_rentsub_mix_network",
                                                      "b2c_sevastopol_drtg_site_rentsub_mix_network",  ###############################
                                                      "b2c_stavropol_drtg_site_rentsub_mix_network",
                                                      "b2c_tyumen_drtg_site_rentsub_mix_network",
                                                      "b2c_ufa_drtg_site_rentsub_mix_network",
                                                      "b2c_volgograd_drtg_site_rentsub_mix_network",
                                                      "b2c_yalta_drtg_site_rentsub_mix_network",  ###############################
                                                      "b2c_simferopol_drtg_site_rentsub_mix_network",  # рк к заведению  ###############################
                                                      "b2c_ulyanovsk_drtg_site_rentsub_mix_network",
                                                      "b2c_tomsk_drtg_site_rentsub_mix_network",
                                                      "b2c_kaluga_drtg_site_rentsub_mix_network",
                                                      "b2c_ryazan_drtg_site_rentsub_mix_network",
                                                      "b2c_tula_drtg_site_rentsub_mix_network",
                                                      "b2c_bryansk_drtg_site_rentsub_mix_network",
                                                      "b2c_kostroma_drtg_site_rentsub_mix_network",
                                                      "b2c_ivanovo_drtg_site_rentsub_mix_network",
                                                      "b2c_arhangelsk_drtg_site_rentsub_mix_network",
                                                      "b2c_vologda_drtg_site_rentsub_mix_network",  # рк к заведению
                                                      "b2c_sochi_drtg_site_rentsub_mix_network",

        ]},

        ######################################################################################
        # Пакет: RTG salesec #########################################################################
        ######################################################################################
        {"descr": 'msk_salesec_rtg_network_bdg', "fltrs": ["b2c_(mo|msk)_rtg_site_salesec_mix_network",
                                                           "b2c_msk_rtg_withoutlead_salesec_mix_network",
                                                           "b2c_msk_rtg_withlead_salesec_mix_network"]},
        {"descr": 'spb_salesec_rtg_network_bdg', "fltrs": ["b2c_spb_rtg_site_salesec_mix_network",
                                                           "b2c_spb_rtg_withoutlead_salesec_mix_network",
                                                           "b2c_spb_rtg_withlead_salesec_mix_network"]},
        ######################################################################################
        # Пакет: RTG rentsec #################################################################
        ######################################################################################
        {"descr": 'msk_rentsec_rtg_network_bdg', "fltrs": ["b2c_(mo|msk)_rtg_site_rentsec_mix_network",
                                                           "b2c_msk_rtg_withoutlead_rentsec_mix_network",
                                                           "b2c_msk_rtg_withlead_rentsec_mix_network"]},
        {"descr": 'spb_rentsec_rtg_network_bdg', "fltrs": ["b2c_spb_rtg_site_rentsec_mix_network",
                                                           "b2c_spb_rtg_withoutlead_rentsec_mix_network",
                                                           "b2c_spb_rtg_withlead_rentsec_mix_network"
                                                           ]},

        {"descr": 'all_other_nov_bdg', "fltrs": ["_nov_",]},
        {"descr": 'all_other_ipoteka_bdg', "fltrs": ["_ipoteka_", ]},
        {"descr": 'all_other_own_bdg', "fltrs": ["_own_", "_rentown_", "_saleown_", ]},
        {"descr": 'all_other_com_bdg', "fltrs": ["com_", ]},

    ]

    def __init__(self):
        for i in self.tags:
            i['fltrs'] = [re.compile(j) for j in i['fltrs']]

    def search(self, item):
        if item:
            for i in self.tags:
                for j in i['fltrs']:
                    if j.search(item):
                        return i['descr']  # поиск до первого совпадения

        return False

    def join_classificator(self, df):
        mapping = []
        for i in set(df[self.filter_column].unique()):
            mapping.append({self.filter_column: i, self.classificator_column_name: self.search(i)})
        df = pd.merge(df, pd.DataFrame(mapping), on=self.filter_column)
        return df


class GroupsRegions:
    filter_column = "campaignname"
    classificator_column_name = "region_class"
    tags = [
        {"descr": 'abroad', "fltrs": ["_abroad_", "_world_"]},
        {"descr": 'msk', "fltrs": ["_msk_", "_mo_", "_dmo_", "_bmo_", "_mskmo_", "_cap_"]},
        {"descr": 'spb', "fltrs": ["_spb_", "_spblo_"]},
        {"descr": 'krasnodar', "fltrs": ["_krasnodar_", "_sochi_"]},
        {"descr": 'neo', "fltrs": ["_ekb_", "_novosibirsk_", "_omsk_", ]},
        {"descr": 'oth', "fltrs": ['_kazan_',
                                   '_nn_',
                                   '_krasnoyarsk_',
                                   '_kaliningrad_',
                                   '_rostov_',
                                   '_sevastopol_',
                                   '_tyumen_',
                                   '_yalta_',
                                   '_simferopol_',
                                   '_krym_',
                                   '_voronezh_',
                                   '_chelyabinsk_',
                                   '_irkutsk_',
                                   '_kemerovo_',
                                   '_perm_',
                                   '_samara_',
                                   '_stavropol_',
                                   '_ufa_',
                                   '_volgograd_',
                                   '_ulyanovsk_',
                                   '_tomsk_',
                                   '_kaluga_',
                                   '_ryazan_',
                                   '_tula_',
                                   '_bryansk_',
                                   '_kostroma_',
                                   '_ivanovo_',
                                   '_arhangelsk_',
                                   '_vologda_',
                                   '_22reg_', '_18reg_', '_p4c_', '_regs_',
                                   '_rf_',
                                   '_astrahan_',
                                   '_barnaul_',
                                   '_belgorod_',
                                   '_cheboksary_',
                                   '_habarovsk_',
                                   '_izhevsk_',
                                   '_kirov_',
                                   '_kurgan_',
                                   '_kursk_',
                                   '_lipetsk_',
                                   '_mahachkala_',
                                   '_novgorod_',
                                   '_orel_',
                                   '_orenburg_',
                                   '_penza_',
                                   '_pskov_',
                                   '_saratov_',
                                   '_smolensk_',
                                   '_surgut_',
                                   '_tambov_',
                                   '_tver_',
                                   '_ulanude_',
                                   '_vladimir_',
                                   '_vladivostok_',
                                   '_yaroslavl_',
                                   '_oth_',
                                   ]},

    ]

    def __init__(self):
        for i in self.tags:
            i['fltrs'] = [re.compile(j) for j in i['fltrs']]

    def search(self, item):
        if item:
            for i in self.tags:
                for j in i['fltrs']:
                    if j.search(item):
                        return i['descr']  # поиск до первого совпадения

        return False

    def join_classificator(self, df):
        mapping = []
        for i in set(df[self.filter_column].unique()):
            mapping.append({self.filter_column: i, self.classificator_column_name: self.search(i)})
        df = pd.merge(df, pd.DataFrame(mapping), on=self.filter_column)
        return df


class GenralGroupsVerticalCommon:
    filter_column = "vertical_class"
    classificator_column_name = "vertical_general_class"
    tags = [
        {"descr": 'other', "fltrs": ["ipoteka", "nov", "own", "commerce", ]},
        {"descr": 'realweb', "fltrs": ["realweb"]},
        {"descr": 'daily', "fltrs": ["daily"]},
        {"descr": 'secondary', "fltrs": ["salesub", "rentsub", "rentsec", "salesec", "brand_cian", "competitors"]},
    ]

    def __init__(self):
        for i in self.tags:
            i['fltrs'] = [re.compile(j) for j in i['fltrs']]

    def search(self, item):
        if item:
            for i in self.tags:
                for j in i['fltrs']:
                    if j.search(item):
                        return i['descr']  # поиск до первого совпадения

        return False

    def join_classificator(self, df):
        mapping = []
        for i in set(df[self.filter_column].unique()):
            mapping.append({self.filter_column: i, self.classificator_column_name: self.search(i)})
        df = pd.merge(df, pd.DataFrame(mapping), on=self.filter_column)
        return df


class GroupsVerticalCommon:
    filter_column = "budget_class"
    classificator_column_name = "vertical_class"
    tags = [
        {"descr": 'ipoteka', "fltrs": ["_ipoteka_"]},
        {"descr": 'nov', "fltrs": ["_nov_"]},
        {"descr": 'own', "fltrs": ["_b2b_own_", "_b2b_compet_", "_ocenka_own_", "_sdaisnimi_", "_findagent_own_", "_own_"]},
        {"descr": 'commerce', "fltrs": ["_com_", "_cwrk_", "_cwrkcom_", "_gbcom_", "_iapcom_", "_rentcom_", "_salecom_"]},
        {"descr": 'daily', "fltrs": ["daily"]},

        {"descr": 'salesub', "fltrs": ["_sub_", "_salesub_",]},
        {"descr": 'rentsub', "fltrs": ["_rentsub_"]},

        {"descr": 'rentsec', "fltrs": ["_rentsec_"]},
        {"descr": 'salesec', "fltrs": ["_salesec_"]},

        {"descr": 'brand_cian', "fltrs": ["_brand_cian"]},
        {"descr": 'competitors', "fltrs": ["competitors", "brand", "compet"]},

        {"descr": 'realweb', "fltrs": ["_realweb_", ]},
    ]

    def __init__(self):
        for i in self.tags:
            i['fltrs'] = [re.compile(j) for j in i['fltrs']]

    def search(self, item):
        if item:
            for i in self.tags:
                for j in i['fltrs']:
                    if j.search(item):
                        return i['descr']  # поиск до первого совпадения

        return False

    def join_classificator(self, df):
        mapping = []
        for i in set(df[self.filter_column].unique()):
            mapping.append({self.filter_column: i, self.classificator_column_name: self.search(i)})
        df = pd.merge(df, pd.DataFrame(mapping), on=self.filter_column)
        return df


class SearchOrNetwork:
    filter_column = "campaignname"
    classificator_column_name = "network_class"
    tags = [
        {"descr": 'mkbyndx_network', "fltrs": ["_mkb_.*search", "_mkb_.*network"]},

        {"descr": 'search', "fltrs": ["_search"]},
        {"descr": 'drtg_network', "fltrs": ["_drtg_", "_rtg_smart"]},
        {"descr": 'mk_network', "fltrs": ["_pmax_", "_mk_.*_network"]},
        {"descr": 'lal_network', "fltrs": ["lal", "_custlal_", "smartlal", "audiencelal"]},

        {"descr": 'simplertg_network', "fltrs": ["_rtg_"]},
        {"descr": 'other_network', "fltrs": ["_network", "_ci_", "discovery"]},
    ]

    def __init__(self):
        for i in self.tags:
            i['fltrs'] = [re.compile(j) for j in i['fltrs']]

    def search(self, item):
        if item:
            for i in self.tags:
                for j in i['fltrs']:
                    if j.search(item):
                        return i['descr']  # поиск до первого совпадения

        return False

    def join_classificator(self, df):
        mapping = []
        for i in set(df[self.filter_column].unique()):
            mapping.append({self.filter_column: i, self.classificator_column_name: self.search(i)})
        df = pd.merge(df, pd.DataFrame(mapping), on=self.filter_column)
        return df


def all_classificators_join(data):
    data = concat_empty_columns(data, ["region"])
    data["region"] = data["campaignname"].str.split("_").str.get(1)

    for classificator in (MP(), GroupsRegions(), GroupsVerticalCommon(), SearchOrNetwork(), GenralGroupsVerticalCommon()):
        data = classificator.join_classificator(data)
    return data


if __name__ == '__main__':
    df = pd.DataFrame([{"campaignname": "qqq_samara_qqq", "vol": 1},
                       {"campaignname": "qqq_nn_qqq", "vol": 2},
                       {"campaignname": "qqq_msk_qqq", "vol": 3},])
    df = all_classificators_join(df)
    print(df)
